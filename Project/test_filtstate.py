# test_dff.py

import numpy as np
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
#import numpy as np

######## tb arguments ########
coef = [0x63, 0x6F, 0x65, 0x66]
coef_list = [0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01]
#coef_list = [0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x65, 0x43, 0x32, 0x10, 0x12]

data = [0x64, 0x61, 0x74, 0x61]
data_list = [0xff, 0xf6, 0xff, 0xf7, 0xff, 0xf8, 0xff, 0xf9,
    0xff, 0xfa, 0xff, 0xfb, 0xff, 0xfc, 0xff, 0xfd, 0xff, 0xfe,
    0xff, 0xff, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x03,
    0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x08,
    0x00, 0x09]

done = [0x64, 0x6F, 0x6E, 0x65]
######## tb arguments ########

async def reset_dut(reset, duration_ns):
    reset <= 1
    await Timer(duration_ns, units="ns")
    reset <= 0
    #reset._log.debug("Reset complete")

@cocotb.test()
async def test_filtstate(dut):
    """ Test that d propagates to q """
    clock = Clock(dut.clk, 20, units="ns")  # Create a 10us period clock on port clk
    cocotb.fork(clock.start())  # Start the clock
    #dut.reset<=1
    #await Timer(time=1, unit='us')
    reset = dut.reset
    cocotb.fork(reset_dut(reset, duration_ns=40))
    dut.r_data <= 0 # Initialize r_data
    await Timer(40, units="ns")
    
    print("{:d}".format(dut.filt.y.value.signed_integer))
    
    
    for c in coef:
        await RisingEdge(dut.clk)
        dut.r_data <= c
        
    for c in coef_list:
        await RisingEdge(dut.clk)
        dut.r_data <= c

    #for d in data:
    #    await RisingEdge(dut.clk)
    #    dut.r_data <= d

    for d in data_list:
        await RisingEdge(dut.clk)
        dut.r_data <= d
        print("{:d}".format(dut.filt.y.value.signed_integer))

    for n in done:
        await RisingEdge(dut.clk)
        dut.r_data <= n
