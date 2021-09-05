module biquad_filter #(
  parameter io_width = 16,
  parameter internal_width = io_width*2-1
  )(
  input clk,
  input reset,

  /* slave axis interface */
  input signed[io_width-1:0] x,
  output signed[io_width-1:0] y,

  input signed [io_width-1:0] b0,
  input signed [io_width-1:0] b1,
  input signed [io_width-1:0] b2,
  input signed [io_width-1:0] a1,
  input signed [io_width-1:0] a2
  );
  wire signed[internal_width-1:0] xin;
  reg signed[internal_width-1:0] w_n, w_n_1, w_n_2;
  reg signed[internal_width-1:0] yout;

  assign xin = x;

  /* tvalid management */
  
  always @(posedge clk, posedge reset)
    if (reset)
      w_n_1 <= 0;
    else
      w_n_1 <= w_n;
      
  always @(posedge clk, posedge reset)
    if (reset)
      w_n_2 <= 0;
    else
      w_n_2 <= w_n_1;
  
  always @(posedge clk, posedge reset)
    if (reset)
      w_n <= 0;
    else
      w_n <= xin - a1*w_n_1 -a2*w_n_2;
      
  always @(posedge clk, posedge reset)
    if (reset)
      yout <= 0;
    else
      yout <= b0*w_n+b1*w_n_1+b2*w_n_2;

   assign y = yout;
   
   `ifdef COCOTB_SIM
		initial begin
			$dumpfile ("biquad_filter.vcd");
			$dumpvars;
			#1;
		end
	`endif
endmodule
