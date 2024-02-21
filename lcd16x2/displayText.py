#!/usr/bin/env python3
# From: https://graycat.io/tutorials/beaglebone-io-using-python-mmap/
from mmap import mmap
import time, struct
import lcd

def toggle_enable(memi):
    lcd.delay()
    memi[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", E)
    lcd.delay()
    memi[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", E)
    lcd.delay()

def setup_pins(memi):
    packed_reg = memi[GPIO_OE:GPIO_OE+4]
    reg_status = struct.unpack("<L", packed_reg)[0]

    reg_status &= ~(RS)
    #reg_status &= ~(E)
    reg_status &= ~(D4)
    reg_status &= ~(D5)
    reg_status &= ~(D6)
    reg_status &= ~(D7)
    reg_status &= ~(P9_23)

    #Make all pins GPIO
    memi[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status)

    #Everything set to 0
    memi[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", RS|D4|D5|D6|D7|P9_23)

def setup_pin_enable(memi):
    packed_reg = mem[GPIO_OE:GPIO_OE+4]
    reg_status = struct.unpack("<L", packed_reg)[0]

    reg_status &= ~(E)
    
    #Make all pins GPIO
    memi[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status)

    #Everything set to 0
    memi[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", E)
    
def setup_lcd_4bit(memi):
    #4 bit mode
    memi[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", RS)
    memi[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", dataBits)
    memi[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", D5)
    time.sleep(5)
    toggle_enable(mem2)

def command(memi, command):
    memi[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", RS)
    #Top half of command first
    set_data(memi, command >> 4)
    toggle_enable(mem2)
    set_data(memi, command & 0x0F)
    toggle_enable(mem2)

def set_data(memi, curByte):
    # Clear all data then check what needs to be set
    memi[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", dataBits)
    for i, pin in enumerate([D4, D5, D6, D7]):
        if curByte & (1 << i):
            memi[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", pin)
    print("x")        
    # time.sleep(5)
    

def write_string(memi, message):
     memi[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", RS)
     print("RS")
    #  set_data(memi, 0x4)
    #  toggle_enable(mem2)
    #  set_data(memi, 0x8)
    #  toggle_enable(mem2)
     
     for char in message:
         asci = ord(char)
         set_data(memi,asci >> 4)
         toggle_enable(mem2)
         
         set_data(memi, asci & 0xF)
         toggle_enable(mem2)
    

def clear_display(mem):
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", RS)
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", dataBits)
    toggle_enable(mem2)


#LCD COMMANDS
BITMODE_4 = (0x00)
LCD2LINE = (0x08)
LCD_CLEARDISPLAY = (0x01)
LCD_RETURNHOME = (0x02)
LCD_ENTRYMODESET = (0x04)
LCD_DISPLAYCONTROL = (0x08)
LCD_CURSORSHIFT = (0x10)
LCD_FUNCTIONSET = (0x20)


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

dataBits= D4 | D5 | D6 | D7
toggle = 0

# Next we need to make the mmap, using the desired size and offset:
with open("/dev/mem", "r+b" ) as f:
  mem = mmap(f.fileno(), GPIO1_size, offset=GPIO1_offset)
  
with open("/dev/mem", "r+b" ) as g:
  mem2 = mmap(g.fileno(), GPIO1_size, offset=GPIO2_offset)

setup_pins(mem)
setup_pin_enable(mem2)
lcd.delay()
clear_display(mem)
print("4 bit")
setup_lcd_4bit(mem)

# print("blink")
# command(mem, LCD_BLINKON)
command(mem, LCD_FUNCTIONSET | BITMODE_4 | LCD2LINE)

print("clear")
command(mem, 0x01)

print("return home")
command(mem, 0x02)

print("Display On")
command(mem, 0x0C)

command(mem, LCD_CURSORON)

# lcd.delay()

print("write")
write_string(mem, "192.168.7.2:8081")

command(mem, LCD_CURSORON)

print("end")
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
  mem2.close()




