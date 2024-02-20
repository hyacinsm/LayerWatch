#!/usr/bin/env python3
# From: https://graycat.io/tutorials/beaglebone-io-using-python-mmap/
from mmap import mmap
import time, struct

# Modified by Jailen Hobbs

# Mapping the entire /dev/mem file would require that over a gigabyte be
# allocated in Python's heap, so the offset address and size variables are
# used to keep the mmap as small as possible, in this case just the GPIO1 register.
# These values are straight out of the memory map in section 2.1 of the
# Technical Reference Manual. the GPIO_OE, GPIO_SETDATAOUT and GPIO_CLEARDATAOUT
# addresses are found in section 25.4, which shows the address offsets of each
# register within the GPIO modules, starting from the base module address.
# Chapter 25 explains how to use the GPIO registers.
# All we need to do is set a pin as an output, then set and clear its output state.
# To do the first, we need the 'output enable' register (GPIO_OE above).
# Then the GPIO_SETDATAOUT and GPIO_CLEARDATAOUT registers will do the rest.
# Each one of these registers is 32 bits long, each bit of which corresponding
# to one of 32 GPIO pins, so for pin 24 we need bit 24, or 1 shifted left 24 places.

GPIO1_offset = 0x4804c000
GPIO1_size = 0x4804cfff-GPIO1_offset
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
P9_23 = 1 << 17
toggle = 0

# Next we need to make the mmap, using the desired size and offset:
with open("/dev/mem", "r+b" ) as f:
  mem = mmap(f.fileno(), GPIO1_size, offset=GPIO1_offset)

packed_reg = mem[GPIO_OE:GPIO_OE+4]

reg_status = struct.unpack("<L", packed_reg)[0]

reg_status &= ~(P9_23)

mem[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status)

try:
  while(True):
    toggle = ~toggle
    if(toggle):
      mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", P9_23)
    else:
      mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", P9_23)

    time.sleep(3)

except KeyboardInterrupt:
  mem.close()
