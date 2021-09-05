# test_dff.py

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random
import scipy.signal as ss
coef_list = [0x48, 0xF6, 0x51, 0xea, 0x49, 0xee, 0x61, 0xcd, 0x97, 0x8e]
#data_list = [random.randint(-32768, 32767) for i in range(1000)]
data_list = range(-10,10)

a = [16384.0, -11153.0, 4173.0]
b = [6105.0, 0.0, -6105.0]
y = ss.lfilter(b, a, data_list)
print(y)
#data_list = np.arange(-10, 10).astype(np.int16)


print(data_list)
async def reset_dut(reset, duration_ns):
    reset <= 1
    await Timer(duration_ns, units="ns")
    reset <= 0
    #reset._log.debug("Reset complete")

@cocotb.test()
async def test_biquad(dut):
	print(type(dut.x))
	""" Test that d propagates to q """
	clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
	cocotb.fork(clock.start())  # Start the clock
	#dut.reset<=1
	#await Timer(time=1, unit='us')
	reset = dut.reset
	dut.x <= 0
	dut.en <=1
	cocotb.fork(reset_dut(reset, duration_ns=500))
	
	dut.b0<=6105 # 32767/32767
	dut.b1<=0 # 32767/32767
	dut.b2<=-6105 # 32767/32767
	dut.q<=14 # 1/32567
	dut.a1<=-11153 # 1/32567
	dut.a2<=4173 # 1/32767
	
	for x in data_list:
		await RisingEdge(dut.clk)
		dut.x <= x  # Assign the random value val to the input port d
#        await FallingEdge(dut.clk)
#        assert dut.y.value = , "output q was incorrect on the {}th cycle".format(i)

	for x in range(4):
		await RisingEdge(dut.clk)
