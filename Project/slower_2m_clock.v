module slower_2m_clock #(parameter N=25, M=25000000)
(
  input wire clk, reset,
  output wire sclk,
  output wire tick
);

reg[N-1:0] cnt_now = M-2;
reg[N-1:0] cnt_next = M-2;
reg sclk_now;
reg sclk_next;
reg tick_now, tick_next; /*added tick*/

always @(posedge clk, posedge reset) begin    // sequential
  if(reset) begin
    cnt_now <= M-2; /*modified to start clock on high*/
    sclk_now <= 0;
    tick_now <= 0;
  end
  else begin
    cnt_now <= cnt_next;
    sclk_now <= sclk_next;
    tick_now <= tick_next;
  end
end

always @* begin                               // combinational
  if(cnt_now == M-1) begin
    cnt_next = 0;
    sclk_next = ~sclk_now;
    tick_next = 1 & ~sclk_now;
  end
  else begin
    cnt_next = cnt_now + 1;
    sclk_next = sclk_now;
    tick_next = 0;
  end
end

assign tick = tick_now;
assign sclk = sclk_now;

endmodule
