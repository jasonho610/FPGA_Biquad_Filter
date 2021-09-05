# Makefile

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/top.v $(PWD)/uart.v $(PWD)/baud_gen.v $(PWD)/uart_rx.v $(PWD)/uart_tx.v $(PWD)/fifo_reg.v $(PWD)/state.v $(PWD)/biquad_filter.v
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = top

# MODULE is the basename of the Python test file
MODULE = test_top

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
