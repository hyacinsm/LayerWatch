# Authors:
Jailen Hobbs 
Sean Hyacinthe

# LayerWatch
An open source, afforable way to monitor and stop 3D print failures before they happen.

## Flask Server
On the server you will find status photos from the USB Camera. In the bottom left of the photo you will find relevant data pertaining to the time of day the image was taken. As well as an stop print button. This button will power off your device and effectively stop the print.

# Installation Instructions
git clone git@github.com:hyacinsm/LayerWatch.git

    1. cd ~/LayerWatch
    2. sudo ./setup.sh
    3. sudo ./install.sh
    4. sudo ./LayerWatch.sh
    5. sudo reboot or sudo website/app.py
    (The application runs on startup but you can run app.py found in website directory)

# Pins for hardware on BeagleBone Black (BBB)

## PowerSwitch Tail:
|Relay Wire| BBB Pin| |
|-|-| -|
|Yellow Wire| P9_23 |
|Black Wire| GND|
|Red Wire | 3.3V|

Circuit can  be seen at https://www.hackster.io/jailen/layerwatch-139a25#schematics

## LCD 16x2
|LCD Pin| BBB Pin| |
|----| ----| -|
|RS |P8_26|
|E |P8_18| 
|D4 |P8_11|
|D5 |P8_12|
|D6 |P8_15|
|D7 |P8_16|

## USB Camera
Plug into USB port on BeagleBoneBlack

# !!WARNING!! IF ALTERING PINS
The enable pin (P8_18) is on GPIO2 whereas the other 5 pins connected to the LCD16x2 display are on GPIO1. The reasoning behind there being two mmap function calls.

