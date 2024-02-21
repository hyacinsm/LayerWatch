#!/usr/bin/env python3
import lcd as lcd16
# from mmap import mmap
# import time, struct

## Set up GPIO for memmap
GPIO1_offset = 0x4804c000
GPIO2_offset = 0x481AC000
GPIO1_size = 0x4804cfff-GPIO1_offset
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
#Pins connected to LCD
P8_26 = 1 << 29
P8_18 = 1 << 1 #GPIO_2
P8_11 = 1 << 13
P8_12 = 1 << 12
P8_15 = 1 << 15
P8_16 = 1 << 14
P9_23 = 1 << 17

RS = P8_26
E = P8_18 #GPIO_2
D4 = P8_11
D5 = P8_12
D6 = P8_15
D7 = P8_16

try:
    lcd = lcd16.lcd(RS=RS, E=E, D4=D4, D5=D5, D6=D6, D7=D7, enable_offset= GPIO2_offset, chip_offset = GPIO1_offset, gpio_size = GPIO1_size, relay_pin= P9_23)

    lcd.setup_pins()
    lcd.setup_pin_enable()
    lcd.setup_commands()

    lcd.write_string("http://172.22.166.50:5051")
    lcd.toggle_relay()
    
    while(True):
        lcd.command(lcd.LCD_CURSORSHIFT | lcd.LCD_SHIFTLEFT)
        lcd.delay(0.5)
    
except KeyboardInterrupt:
  lcd.mem_close()