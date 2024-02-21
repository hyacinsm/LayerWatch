#!/usr/bin/env python3
# From: https://graycat.io/tutorials/beaglebone-io-using-python-mmap/
from mmap import mmap
import time, struct
import lcd

def set_bits(D7,D6,D5,D4):
    return (D7 | D6 | D5 | D4)

def toggle_enable(mem):
    mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", E)
    lcd.delay()
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", E)
    lcd.delay()

def setup_pins(mem):
    packed_reg = mem[GPIO_OE:GPIO_OE+4]
    reg_status = struct.unpack("<L", packed_reg)[0]

    reg_status &= ~(RS)
    reg_status &= ~(E)
    reg_status &= ~(D4)
    reg_status &= ~(D5)
    reg_status &= ~(D6)
    reg_status &= ~(D7)
    reg_status &= ~(P9_23)
    
    #Make all pins GPIO 
    mem[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status)
    
    #Everything set to 0
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", reg_status)

def setup_lcd_4bit(mem):
    #4 bit mode
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", RS)
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", dataBits)
    toggle_enable(mem)
    
def command(mem, command):
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", RS)
    #Top half of command first
    set_data(mem, command >> 4)
    toggle_enable(mem)
    set_data(mem, command & 0x0F)
    toggle_enable(mem)

def set_data(mem, curByte):
    # Clear all data then check what needs to be set
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", dataBits)
    for i, pin in enumerate([D4, D5, D6, D7]):
        if curByte & (1 << i):
            mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", pin)
            
def write_data(mem, message):
     mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", RS)
     
     for char in message:
         asci = ord(char)
         set_data(mem,asci << 4)
         toggle_enable(mem)
         set_data(mem, asci & 0x0F)
         toggle_enable(mem)

def clear_display(mem):
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", RS)
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", dataBits)
    toggle_enable(mem)
    
        
#LCD COMMANDS
BITMODE_4 = (0x00)
LCD2LINE = (0x08)
LCD_CLEARDISPLAY = (0x01)
LCD_RETURNHOME = (0x02)
LCD_ENTRYMODESET = (0x04)
LCD_DISPLAYCONTROL = (0x08)
LCD_CURSORSHIFT = (0x10)
LCD_FUNCTIONSET = (0x20)
LCD_SETCGRAMADDR = (0x40)
LCD_SETDDRAMADDR = (0x80)

# Entry flags
LCD_ENTRYLEFT = (0x02)
LCD_ENTRYSHIFTDECREMENT = (0x00)

# Control flags
LCD_DISPLAYON = (0x04)
LCD_CURSORON = (0x02)
LCD_CURSOROFF = (0x00)
LCD_BLINKON = (0x01)
LCD_BLINKOFF = (0x00) 

## Set up GPIO for memmap
GPIO1_offset = 0x4804c000
GPIO1_size = 0x4804cfff-GPIO1_offset
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
#Pins connected to LCD
P9_12 = 1 << 28
P9_15 = 1 << 16
P8_11 = 1 << 13
P8_12 = 1 << 12
P8_15 = 1 << 15
P8_16 = 1 << 14
P9_23 = 1 << 17

RS = P9_12
E = P9_15
D4 = P8_11
D5 = P8_12
D6 = P8_15
D7 = P8_16

dataBits= D4 | D5 | D6 | D7
toggle = 0

# Next we need to make the mmap, using the desired size and offset:
with open("/dev/mem", "r+b" ) as f:
  mem = mmap(f.fileno(), GPIO1_size, offset=GPIO1_offset)

setup_pins(mem)
lcd.delay()
# clear_display(mem)


command(mem, LCD_FUNCTIONSET | BITMODE_4 | LCD2LINE)
command(mem, LCD_CLEARDISPLAY)
command(mem, LCD_RETURNHOME)
command(mem, LCD_DISPLAYON)
command(mem, LCD_CURSORON)


mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", P9_23)
mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", D4)
mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", E)

lcd.delay(0.5)


write_data(mem, "H")
print("here")

try:
  while(True):
    toggle = ~toggle
    if(toggle):
      mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", P9_23)
    else:
      mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", P9_23)

    lcd.delay()

except KeyboardInterrupt:
  mem.close()
  


    