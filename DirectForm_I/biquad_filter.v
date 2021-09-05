module biquad_filter #(
  parameter io_width = 16,
  parameter internal_width = io_width*2
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
  
  reg signed[io_width-1:0] xin;
  reg signed[io_width-1:0] x_n1, x_n2;
  reg signed[io_width-1:0] y_n1, y_n2;
  wire signed[internal_width-1:0] pb0, pb1, pb2;
  wire signed[internal_width-1:0] pa1, pa2;
 
  wire [5:0] l;
  //wire signed[15:0] pd_check0, pd_check1, pd_check2, pd_check3, pd_check4, pd_check5;
  
  assign pb0 = b0*xin;
  assign pb1 = b1*x_n1;
  assign pb2 = b2*x_n2;
  assign pa1 = a1*y_n1;
  assign pa2 = a2*y_n2;
  
  always @(posedge clk, posedge reset) begin
    if (reset)
      xin <= 0;
    else begin
		if (en) xin <= x;
	end
  end
  
  always @(posedge clk, posedge reset) begin
    if (reset)
      x_n1 <= 0;
    else begin
		if (en) x_n1 <= xin;
	end
  end
  
  always @(posedge clk, posedge reset) begin
    if (reset)
      x_n2 <= 0;
    else begin
		if (en) x_n2 <= x_n1;
	end
  end
  
  assign y = (pb0+pb1+pb2-pa1-pa2) >>> q[3:0] ;
  
  always @(posedge clk, posedge reset) begin
    if (reset)
      y_n1 <= 0;
    else begin
		if (en) y_n1 <= y;
	end
  end
  
  always @(posedge clk, posedge reset) begin
    if (reset)
      y_n2 <= 0;
    else begin
		if (en) y_n2 <= y_n1;
	end
  end
  
/*    `ifdef COCOTB_SIM
		initial begin
			$dumpfile ("biquad.vcd");
			$dumpvars(0);
			#1;
		end
  `endif
 */ 
endmodule
