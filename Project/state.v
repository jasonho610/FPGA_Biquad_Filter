module state
(
	input wire clk, reset,
	input wire rx_empty, rx_full, tx_empty, tx_full,
	input wire [7:0] r_data,
	output wire rd_uart, 
	output reg wr_uart,
	output wire [7:0] w_data,
	output wire [1:0] s
);

  localparam coef = 32'h636F6566, s_coef = 2'b00,
             data = 32'h64617461, s_data = 2'b01,
			    done = 32'h646F6E65, s_done = 2'b10;
  reg [31:0] cmd_reg, cmd_next;
  reg [1:0] state_reg, state_next;
  reg [3:0] ptr_reg, ptr_next;
  reg [15:0] b0_reg, b1_reg, b2_reg, a1_reg, a2_reg;
  reg [15:0] b0_next, b1_next, b2_next, a1_next, a2_next;
  reg [15:0] q_next, q_reg;
  reg [15:0] x_reg, x_next;
  wire [15:0] y;
  reg clk_2, clk_2_prev;
  reg en;
 
  always @(negedge rd_uart, posedge reset) begin
    if (reset)
	  clk_2 <= 1'b0;
	else
	  clk_2 <= ~clk_2;
  end
   
  always @(negedge clk, posedge reset) begin
    if (reset) begin
	  cmd_reg <= 0;
	  state_reg <= s_done;
	  ptr_reg <= 0;
	  b0_reg <= 0;
	  b1_reg <= 0;
	  b2_reg <= 0;
	  q_reg <= 0;
	  a1_reg <= 0;
	  a2_reg <= 0;
	  x_reg <= 0;
    end
    else begin
      if (rd_uart) begin
			cmd_reg <= cmd_next;
			state_reg <= state_next;
			ptr_reg <= ptr_next;
			b0_reg <= b0_next;
			b1_reg <= b1_next;
			b2_reg <= b2_next;
			q_reg <= q_next;
			a1_reg <= a1_next;
			a2_reg <= a2_next;
			x_reg <= x_next;
		end
    end
  end
	  
  biquad_filter filt(.clk(clk_2), .reset(reset), .en(en),
	 .b0(b0_reg), .b1(b1_reg), .b2(b2_reg), .q(q_reg), .a1(a1_reg), .a2(a2_reg),
	  .x(x_reg), .y(y));
  
  always @* begin
	state_next = state_reg;
	ptr_next = ptr_reg;
	case(state_reg)
	  s_coef: begin
	    ptr_next = ptr_reg + 1;
	    en = 0;
	    if (ptr_reg<=1) begin
		   b0_next = {b0_reg[7:0], cmd_reg[7:0]};
		end
		else if (ptr_reg<=3) begin
			b1_next = {b1_reg[7:0], cmd_reg[7:0]};
		end
		else if (ptr_reg<=5) begin
			b2_next = {b2_reg[7:0], cmd_reg[7:0]};
		end
		else if (ptr_reg<=7) begin
			q_next = {q_reg[7:0], cmd_reg[7:0]};
		end
		else if (ptr_reg<=9) begin
			a1_next = {a1_reg[7:0], cmd_reg[7:0]};
		end
		else if (ptr_reg<=11) begin
			a2_next = {a2_reg[7:0], cmd_reg[7:0]};
		end
		
		if (ptr_reg==11) begin
			ptr_next = 0;
			state_next = s_data;
		end
	  end
		 
	  s_data: begin
		ptr_next = ptr_reg + 1;
		en = 1;
	    if (ptr_reg<=1) begin
		   x_next = {x_reg[7:0], cmd_reg[7:0]};
		   ptr_next = ptr_reg + 1;
		end
		
		if (ptr_reg==1) begin
			ptr_next = 0;
		end
	  end
		 
	  s_done: begin
		en = 0;
		ptr_next = 0;
	    b0_next = 0;
	    b1_next = 0;
	    b2_next = 0;
		 q_next = 0;
	    a1_next = 0;
	    a2_next = 0;
	    x_next = 0;
	  end
	  
	  default: begin
		en = 0;
	    b0_next = b0_reg;
	    b1_next = b1_reg;
	    b2_next = b2_reg;
		 q_next = q_reg;
	    a1_next = a1_reg;
	    a2_next = a2_reg;
	    x_next = x_reg;
	  end
    endcase
    
    cmd_next = {cmd_reg[23:0], r_data};
    case(cmd_reg)
      coef: state_next = s_coef;
      data: state_next = s_data;
      done: state_next = s_done;
    endcase
  end

  assign w_data = (~clk_2)?y[15:8]:y[7:0];
  
  assign rd_uart = ~rx_empty & ~tx_full;
  
  always @(negedge clk, posedge reset) begin
    if (reset)
	  wr_uart <= 1'b0;
    else begin
	   wr_uart <= 1'b0;
      //if ((en==1))
      if (~tx_full && (en==1) && ((clk_2==0 && clk_2_prev == 1) || (clk_2==1 && clk_2_prev == 0)))
		 wr_uart <= 1'b1;
	  clk_2_prev <= clk_2;
    end
  end
  
  assign s = state_reg;
  /*
  `ifdef COCOTB_SIM
		initial begin
			$dumpfile ("filtstate.vcd");
			$dumpvars(0);
			#1;
		end
  `endif*/
endmodule
