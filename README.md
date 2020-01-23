## Projekt leírása

Raspberry Pi 3 segítségével létrehozni egy hő- és páramérőt, ami valós időben érzékel és menti le az adatokat, majd egy grafikonon vizualizálja azt.

## Összeszerelés

A DHT22 szenzort választottam a hő- és páratartalom mérésére, ami a tranzisztoros hőmérséklet mérés elvén alapul. Ezeknek a szenzoroknak az ára kedvező, a pontosságuk növelhető, ha DHT11 szenzort vesszük meg.

![](https://camo.githubusercontent.com/b4096b079514cae6c9f3d97720927ef6a993892d/68747470733a2f2f636f6d706f6e656e74733130312e636f6d2f73697465732f64656661756c742f66696c65732f636f6d706f6e656e745f70696e2f444854313125453225383025393354656d70657261747572652d53656e736f722d50696e6f75742e6a7067)

![](https://camo.githubusercontent.com/b4ad1301d9e356c9dc3a926950aecc3427a1e28d/68747470733a2f2f696f7464657369676e70726f2e636f6d2f73697465732f64656661756c742f66696c65732f696e6c696e652d696d616765732f436972637569742d4469616772616d2d666f722d53656e64696e672d44485431312d53656e736f722d446174612d746f2d49424d2d576174736f6e2d436c6f75642d506c6174666f726d2d7573696e672d5261737062657272792d50692e706e67)

A másik szenzor I2C képes 2004 LCD kijelző ( ez azt jelenti, hogy 20 karaktert tud kiírni 4 db sorban, másik változata a 1602)

* Címe: 3F - I2C címe

![](https://cdn.instructables.com/FS7/X2Z3/JRKYXUL4/FS7X2Z3JRKYXUL4.LARGE.jpg?auto=webp&width=1024&height=1024&fit=bounds)

![](https://camo.githubusercontent.com/33ef203d69ab468446d5ac003d330970719e9a15/68747470733a2f2f7777772e6a616d65636f2e636f6d2f4a616d65636f2f776f726b73686f702f636972637569746e6f7465732f7261737062657272795f70695f636972637569745f6e6f74655f666967322e6a7067)

A bekötés az SDA és SCL pinek összekötésével történik.


## I2C kommunikáció

I2C kommunikáció: az I2C egy 7 bites bus, ez azt jelenti, hogy legfeljebb 127 eszközt/modult tud címezni.

![](https://camo.githubusercontent.com/18f73873d102b186ec71f00fb96d598a807c2fe5/68747470733a2f2f696d6167652e6a696d63646e2e636f6d2f6170702f636d732f696d6167652f7472616e73662f64696d656e73696f6e3d3732397831303030303a666f726d61743d706e672f706174682f73393034343930346365386234336335632f696d6167652f69626265383031656130653662386162352f76657273696f6e2f313530353732313730392f696d6167652e706e67)

A raspberry-n a i2cdetect parancsal térképezhetjük fel az ezközöket.

![](https://camo.githubusercontent.com/c1bf5736bf5a4f1a4a02e5449d75e176cdcbe5ea/68747470733a2f2f692e696d6775722e636f6d2f4745706473324e2e706e67)
