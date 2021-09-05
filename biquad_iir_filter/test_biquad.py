# test_dff.py

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
x_list = [1,100, 1000, 3000, -100, -500, -3000]

async def reset_dut(reset, duration_ns):
    reset <= 1
    await Timer(duration_ns, units="ns")
    reset <= 0
    #reset._log.debug("Reset complete")

@cocotb.test()
async def test_biquad(dut):
	""" Test that d propagates to q """
	clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
	cocotb.fork(clock.start())  # Start the clock
	#dut.reset<=1
	#await Timer(time=1, unit='us')
	reset = dut.reset
	dut.x <= 0
	cocotb.fork(reset_dut(reset, duration_ns=500))
	
	dut.b0<=0
	dut.b1<=0
	dut.b2<=1
	dut.a1<=2
	dut.a2<=1
	
	for x in x_list:
		await FallingEdge(dut.clk)
		dut.x <= x  # Assign the random value val to the input port d
#        await FallingEdge(dut.clk)
#        assert dut.y.value = , "output q was incorrect on the {}th cycle".format(i)

	for x in range(4):
		await FallingEdge(dut.clk)
