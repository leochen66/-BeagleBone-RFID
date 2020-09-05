# BeagleBone RFID 結帳系統
# BeagleBone RFID Accounting System

## Introduction
This project intends to build a modern Accounting System, replacing conventional barcode by rfid tags, which is able to read and write products and members information.

RFID module communicate with BeagleBone through SPI, this is implemented by [Python RC522 library](https://github.com/ondryaso/pi-rc522 "Title").

Also using [Adafruit Beaglebone GPIO](https://github.com/adafruit/adafruit-beaglebone-io-python "Title") to control buzzer.

Python Tkinter is used to develope a surface to achieve tasks such as adding a new product/member or reading datas from RFID tags(for more details please check demo video).

## Material You Need
* BeagleBone Black
* RC522 RFID module
* Buzzer
* A few wires

###### How to connect Beaglebone with RC522?
<table>
    <tr>
        <td>RC522</td>
        <td>BeagleBone</td>
    </tr>
    <tr>
        <td>SDA</td>
        <td>P9_17</td>
    </tr>
    <tr>
        <td>SCK</td>
        <td>P9_22</td>
    </tr>
    <tr>
        <td>MOSI</td>
        <td>P9_18</td>
    </tr>
    <tr>
        <td>MISO</td>
        <td>P9_21</td>
    </tr>
    <tr>
        <td>IRQ</td>
        <td>P9_15</td>
    </tr>
    <tr>
        <td>GND</td>
        <td>GND</td>
    </tr>
    <tr>
        <td>RST</td>
        <td>P9_23</td>
    </tr>
    <tr>
        <td>3.3V</td>
        <td>VCC</td>
    </tr>
</table>

## Demo
Please watch demo video =>
https://www.youtube.com/watch?v=vuAf-18pbaY

## Usage
```
python surface.py
```
