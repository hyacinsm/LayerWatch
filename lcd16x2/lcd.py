from mmap import mmap
import time, struct

#LCD COMMANDS
BITMODE_4 = (0x00)
LCD2LINE = (0x08)
LCD_CLEARDISPLAY = (0x01)
LCD_RETURNHOME = (0x02)
LCD_ENTRYMODESET = (0x04)
LCD_DISPLAYCONTROL = (0x08)
LCD_CURSORSHIFT = (0x10)
LCD_FUNCTIONSET = (0x20)

# Shift flags
LCD_SHIFTLEFT = (0x08)
LCD_SHIFTRIGHT = (0x0C)

# Flag bits
LCD_DISPLAYON = (0x04)
LCD_CURSORON = (0x02)
LCD_CURSOROFF = (0x00)
LCD_BLINKON = (0x01)
LCD_BLINKOFF = (0x00)

#GPIO offsets
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190



class lcd:
     
    def __init__(self, RS, E, D7, D6, D5, D4, enable_offset, chip_offset, gpio_size, relay_pin):
        self.RS = RS
        self.E = E #GPIO_2
        self.D4 = D4
        self.D5 = D5
        self.D6 = D6
        self.D7 = D7
        self.dataBits = D4 | D5 | D6 | D7
        
        #Relay Functionality
        self.relay = relay_pin
        self.toggle = 0
        
        #GPIO mmap
        with open("/dev/mem", "r+b" ) as f:
            self.mem1 = mmap(f.fileno(), gpio_size, offset=chip_offset)
            
        with open("/dev/mem", "r+b" ) as g:
            self.mem2 = mmap(g.fileno(), gpio_size, offset=enable_offset)
        
    def delay(self):
        time.sleep(0.02)
    
    def delayx(self, timer):
        time.sleep(timer)
    
    def toggle_enable(self): #Enable Pin on different GPIO chip
        self.delay()
        self.mem2[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", self.E)
        self.delay()
        self.mem2[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.E)
        self.delay()

    def setup_pins(self):
        packed_reg = self.mem1[GPIO_OE:GPIO_OE+4]
        reg_status = struct.unpack("<L", packed_reg)[0]

        reg_status &= ~(self.RS)
        reg_status &= ~(self.D4)
        reg_status &= ~(self.D5)
        reg_status &= ~(self.D6)
        reg_status &= ~(self.D7)
        reg_status &= ~(self.relay)

        #Make all pins GPIO
        self.mem1[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status)

        #Everything set to 0
        self.mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.RS| self.D4| self.D5| self.D6| self.D7| self.relay)

    def setup_pin_enable(self):
        packed_reg = self.mem2[GPIO_OE:GPIO_OE+4]
        reg_status = struct.unpack("<L", packed_reg)[0]

        reg_status &= ~(self.E)
        
        #Make all pins GPIO
        self.mem2[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status)

        #Everything set to 0
        self.mem2[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.E)
        
    def setup_lcd_4bit(self):
        #4 bit mode
        self.mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.RS)
        self.mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.dataBits)
        self.mem1[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", self.D5)
        self.toggle_enable()
    
    def setup_commands(self):
        self.clear_display()
        self.setup_lcd_4bit()
        self.command(LCD_FUNCTIONSET | BITMODE_4 | LCD2LINE)
        self.command(LCD_CLEARDISPLAY)
        self.command(LCD_RETURNHOME)
        self.command(LCD_DISPLAYCONTROL | LCD_CURSORON | LCD_DISPLAYON)

    def command(self, command):
        self.mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.RS)
        #Top half of command first
        self.set_data(command >> 4)
        self.toggle_enable()
        self.set_data(command & 0x0F)
        self.toggle_enable()

    def set_data(self, curByte):
        # Clear all data then check what needs to be set
        self.mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.dataBits)
        for i, pin in enumerate([self.D4, self.D5, self.D6, self.D7]):
            if curByte & (1 << i):
                self.mem1[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", pin)
        
    def write_string(self, message):
        # Clear Display
        self.command(LCD_CLEARDISPLAY)
        self.mem1[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", self.RS)
        print("Writing")
        for char in message:
            asci = ord(char)
            self.set_data(asci >> 4)
            self.toggle_enable()
            
            self.set_data(asci & 0xF)
            self.toggle_enable()
        
    def clear_display(self):
        self.mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.RS)
        self.mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.dataBits)
        self.toggle_enable()
    
    def toggle_relay(self):
        self.toggle = ~self.toggle
        if(self.toggle):
            self.mem1[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", self.relay)
        else:
            self.mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", self.relay)
        
    
    def mem_close(self):
        self.mem1.close()
        self.mem2.close()
    
