import os
import threading
import time
from datetime import datetime

from flask import Response
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

import I2C_LCD_driver
import Adafruit_DHT

import RPi.GPIO as GPIO  # import RPi.GPIO module
import sqlite3
from sqlite3 import Error
#canvasjs- virtualizált grafikon

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def select_task(conn, sql, params):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute(sql, params)

    rows = cur.fetchall()

    return rows


def select_tasks(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()

    return rows


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(temp,hum,date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


database = "kiss.db"

sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                temp integer NOT NULL,
                                hum integer NOT NULL,
                                date text NOT NULL
                            );"""

# create a database connection
conn = create_connection(database)

# create tables
if conn is not None:
    # create tasks table
    create_table(conn, sql_create_tasks_table)
else:
    print("Error! cannot create the database connection.")
conn.close()

RED = 20
GREEN = 16
BLUE = 21
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
GPIO.setup(RED, GPIO.OUT)  # set a port/pin as an output
GPIO.setup(GREEN, GPIO.OUT)  # set a port/pin as an output
GPIO.setup(BLUE, GPIO.OUT)  # set a port/pin as an output

# hőmérséklet
temp = 0
col_temp = 0
avg_temp = 0  # átlagos hőmérséklet
max_temp = 0  # maximális mért érték
min_temp = -100  # minimális mért érték
req_temp = 0  # hőmérséklet mérések száma

# páratartalom
hum = 0
col_hum = 0
avg_hum = 0  # átlagos páratartalom
max_hum = 0  # maximális mért érték
min_hum = -100  # minimális mért érték
req_hum = 0  # páratartalom mérések száma


def red():
    GPIO.output(RED, 1)
    GPIO.output(GREEN, 0)
    GPIO.output(BLUE, 0)


def green():
    GPIO.output(RED, 0)
    GPIO.output(GREEN, 1)
    GPIO.output(BLUE, 0)


def blue():
    GPIO.output(RED, 0)
    GPIO.output(GREEN, 0)
    GPIO.output(BLUE, 1)


def DHT11_read():
    # Érzékelő típusának beállítása : DHT11,DHT22 vagy AM2302
    # A szenzorunk a következő GPIO-ra van kötve:
    global temp, hum, max_hum, max_temp, min_temp, min_hum, avg_hum, avg_temp, col_temp, col_hum, req_temp, req_hum, req_temp, req_temp
    gpio = 17

    # Ha a read_retry eljárást használjuk. Akkor akár 15x is megpróbálja kiolvasni az érzékelőből az adatot (és minden olvasás előtt 2 másodpercet vár).
    # humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, gpio)
    humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT11, gpio)
    # A DHT11 kiolvasása nagyon érzékeny az időzítésre és a Pi alkalmanként
    # nem tud helyes értéket kiolvasni. Ezért megnézzük, hogy helyesek-e a kiolvasott értékek.
    if humidity is not None and temperature is not None:
        temp = temperature
        hum = humidity

        if temp < min_temp or min_temp == -100:
            min_temp = temp
        if temp > max_temp:
            max_temp = temp

        col_temp += int(temp)
        req_temp += 1
        avg_temp = int(col_temp / req_temp)

        if hum < min_hum or min_hum == -100:
            min_hum = hum
        if hum > max_hum:
            max_hum = hum

        col_hum += int(hum)
        req_hum += 1
        avg_hum = int(col_hum / req_hum)

    else:
        return "", ""


def save_data(filename, tempp, hump):
    con = None
    con = create_connection(database)
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    create_task(con, (temp, hum, st))
    con.commit()
    con.close()

    '''
    if type(data) == list:
        data = [str(x) for x in data]
        data = ', '.join(data)
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    with open(filename, "a") as f:
        f.write(str(st) + str(data) + "\n")
    '''


class myDHTSensor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.board = 1

    def run(self):
        while True:
            DHT11_read()
            time.sleep(10)
            save_data("DHT", temp, hum)
            ip_address = os.popen("ifconfig | grep \"inet \" | grep -v \"127.0.0.1\" | awk '{print $2;}'").read()
            print("ip adress :", ip_address)
            mylcd.lcd_clear()
            mylcd.lcd_display_string("IP : " + str(ip_address).strip(), 1)

            mylcd.lcd_display_string(" jel,  min, max, avg", 2)
            mylcd.lcd_display_string("P:" + str(hum) + " " + str(min_hum) + " " + str(max_hum) + " " + str(avg_hum), 3)
            mylcd.lcd_display_string("H:" + str(temp) + " " + str(min_temp) + " " + str(max_temp) + " " + str(avg_temp),
                                     4)
            if hum < 20:
                blue()
            elif hum < 23:
                green()
            else:
                red()

        pass


dht_sensor = myDHTSensor()
mylcd = I2C_LCD_driver.lcd()

# kiescapelt kéréssel stringet készítek az ip címről
# kiveszem a sorvéget a strip() funkcióval.

ip_address = os.popen("ifconfig | grep \"inet \" | grep -v \"127.0.0.1\" | awk '{print $2;}'").read()
print("ip adress :", ip_address)
mylcd.lcd_display_string("IP:" + str(ip_address).strip(), 1)

mylcd.lcd_display_string("P:" + str(hum), 2)
mylcd.lcd_display_string("H:" + str(temp), 2, 14)

# mylcd.lcd_clear()

app = Flask(__name__)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route("/")
def index():
    # visszaadja a render sablont - ez a főoldal.
    return render_template("index.html")


@app.route("/stat")
def stat():
    # visszaadom a html kódot.
    content = ""

    content += "<h4>Átlagos Hőmérséklet : " + str(avg_temp) + "</h4>"
    content += "<h4>Jelenlegi Hőmérséklet : " + str(temp) + "</h4>"

    content += "<h4>Átlagos Páratartalom : " + str(avg_hum) + "</h4>"
    content += "<h4>Jelenlegi Páratartalom : " + str(hum) + "</h4>"

    mimetype = "text/html"

    return Response(content, mimetype=mimetype)


@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


@app.route('/summary', methods=['GET', 'POST'])
def summary():
    data = request.form['date']  # data is empty
    print(data + "%")
    c = create_connection("kiss.db")
    d = select_task(c, "SELECT * FROM tasks WHERE date like ?", (data + '%',))
    # d = select_tasks(c)
    c.close()
    print(d)
    return jsonify(d)


@app.route('/summarys', methods=['GET', 'POST'])
def summarys():
    c = create_connection(database)
    d = select_tasks(c)
    c.close()
    print(d)
    return jsonify(d)


# ellenőrizzük, hogy fő szálban fut e a program - python sajátosság
if __name__ == '__main__':
    dht_sensor.start()

    # flask alkalmazás indítása  - ez a webszerver.

    app.run(host="0.0.0.0", port="9999", debug=True,
            threaded=True, use_reloader=False)
