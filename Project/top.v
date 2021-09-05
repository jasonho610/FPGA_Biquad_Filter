/*
`include "uart.v"
`include "baud_gen.v"
`include "uart_rx.v"
`include "uart_tx.v"
`include "fifo_reg.v"
`include "state.v"
`include "biquad_filter.v"
`include "slower_2m_clock.v"*/

module top
   (
    input wire CLK_50M, BTN_NORTH,
    input wire RS232_DCE_RXD,
    output wire RS232_DCE_TXD,
    output wire [7:0] LED
   );
   
   // signal declaration
   wire tx_full, tx_empty, rx_full, rx_empty;
   wire [7:0] rec_data, filt_data; 
   wire tx_write;
   wire rx_read;
	// debug
	wire [1:0] s;
	reg CLK_25M = 0;
	reg CLK_12M = 0;
	
	always @(posedge CLK_50M, posedge BTN_NORTH) begin
		if (BTN_NORTH) CLK_25M <= 0;
		else CLK_25M <= ~CLK_25M;
	end
	
	always @(posedge CLK_25M, posedge BTN_NORTH) begin
		if (BTN_NORTH) CLK_12M <= 0;
		else CLK_12M <= ~CLK_12M;
	end
	
   // body
   // instantiate uart
   uart uart_unit
      ( // input
	   .clk(CLK_12M), .reset(BTN_NORTH), .rd_uart(rx_read), .wr_uart(tx_write),
	   .rx(RS232_DCE_RXD), .w_data(filt_data), 
	    // output
       .tx_full(tx_full), .tx_empty(tx_empty), .tx(RS232_DCE_TXD),
       .rx_full(rx_full), .rx_empty(rx_empty),		 
       .r_data(rec_data));
	
   state filtstate
     ( // input 
	  .clk(CLK_12M), .reset(BTN_NORTH),
	  .rx_empty(rx_empty), .rx_full(rx_full), .tx_empty(tx_empty), .tx_full(tx_full),
	   // output
	  .r_data(rec_data), .rd_uart(rx_read), .wr_uart(tx_write), .w_data(filt_data),
	   // debug
	  .s(s));
	  
   // LED display
   assign LED = {s, RS232_DCE_TXD, RS232_DCE_RXD, tx_full, tx_empty, rx_full, rx_empty};
   
	
  `ifdef COCOTB_SIM
		initial begin
			$dumpfile ("top.vcd");
			$dumpvars(0);
			#1;
		end
  `endif
endmodule
