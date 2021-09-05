# test_dff.py

import numpy as np
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
#import numpy as np

######## tb arguments ########
coef = [0x63, 0x6F, 0x65, 0x66]
coef_list = [0x17, 0xd9, 0x00, 0x00, 0xe8, 0x27, 0x00, 0x0e, 0xd4, 0x6f, 0x10, 0x4d]
#coef_list = [0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x65, 0x43, 0x32, 0x10, 0x12]

#data = [0x64, 0x61, 0x74, 0x61]
data_list = [0xff, 0xf6, 0xff, 0xf7, 0xff, 0xf8, 0xff, 0xf9,
    0xff, 0xfa, 0xff, 0xfb, 0xff, 0xfc, 0xff, 0xfd, 0xff, 0xfe,
    0xff, 0xff, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x03,
    0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x08,
    0x00, 0x09]

done = [0x64, 0x6F, 0x6E, 0x65]

baud = 3906 # 1e9//384000
startbit = 0
stopbit = 1

######## tb arguments ########

async def reset_dut(reset, duration_ns):
    reset <= 1
    await Timer(duration_ns, units="ns")
    reset <= 0
    #reset._log.debug("Reset complete")
    
async def uart_tx(tx, data):
    d = bin(data); d = d[2:]; d = d.zfill(8); d = d[::-1]
    tx <= startbit
    await Timer(baud, units="ns")
    for i in d:
        tx <= int(i)
        await Timer(baud, units="ns")
    tx <= stopbit
    await Timer(baud, units="ns")

@cocotb.test()
async def test_top(dut):
    """dut.input"""
    clock = Clock(dut.CLK_50M, 20, units="ns")  # Create a 10us period clock on port clk
    reset = dut.BTN_NORTH
    tx = dut.RS232_DCE_RXD; tx <= 1
    """dut.output"""
    rx = dut.RS232_DCE_TXD;
    led = dut.LED
    #print(count.binstr)
    
    cocotb.fork(clock.start())  # Start the clock
    await reset_dut(reset, 40)  # Reset
    
    await Timer(20000, units="ns")
    
    for c in coef:
        await uart_tx(tx, c)
    
    for c in coef_list:
        await uart_tx(tx, c)

    for d in data_list:
        await uart_tx(tx, d)
        #print("{:d}".format(dut.filt.y.value.signed_integer))
        
    for n in done:
        await uart_tx(tx, n)
    
    await Timer(40000, units="ns")
    
