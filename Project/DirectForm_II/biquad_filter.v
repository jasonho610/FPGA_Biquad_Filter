module biquad_filter #(
  parameter io_width = 16,
  parameter internal_width = io_width*2-1
  )(
  input wire clk,
  input wire reset,
  input wire en,

  input wire signed [io_width-1:0] b0,
  input wire signed [io_width-1:0] b1,
  input wire signed [io_width-1:0] b2,
  input wire signed [io_width-1:0] q,
  input wire signed [io_width-1:0] a1,
  input wire signed [io_width-1:0] a2,
  
  input wire signed [io_width-1:0] x,
  output wire signed [io_width-1:0] y
  );
  
  localparam signed [io_width-1:0] a0 = 16384;
  reg signed[io_width-1:0] xin;
  wire signed[io_width-1:0] w_n; 
  reg signed[io_width-1:0] w_n1, w_n2;
  wire signed[internal_width-1:0] pd0, pd1, pd2, pd3, pd4, pd5;
  //wire signed[15:0] pd_check0, pd_check1, pd_check2, pd_check3, pd_check4, pd_check5;
  
  assign pd0 = a0*xin;
  assign pd1 = a1*w_n1;
  assign pd2 = a2*w_n2;
  
  always @(posedge clk, posedge reset) begin
    if (reset)
      xin <= 0;
    else begin
		if (en) xin <= x;
	end
  end

  assign w_n = (pd0 - pd1 - pd2) >>> q[3:0];


  always @(posedge clk, posedge reset) begin
    if (reset)
      w_n1 <= 0;
    else begin
		if (en) w_n1 <= w_n;
	end
  end

  always @(posedge clk, posedge reset) begin
    if (reset)
      w_n2 <= 0;
    else begin
		if (en) w_n2 <= w_n1;
	end
  end
    
  assign pd3 = b0*w_n;
  assign pd4 = b1*w_n1;
  assign pd5 = b2*w_n2;
  
  assign y = ((pd3 + pd4 + pd5) >>> (2*q[3:0]-io_width));
   
    `ifdef COCOTB_SIM
		initial begin
			$dumpfile ("biquad.vcd");
			$dumpvars(0);
			#1;
		end
  `endif
  
endmodule
