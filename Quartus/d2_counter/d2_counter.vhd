library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity d2_counter is
	generic(
		F_CNT : natural := 500; --50_000_000/10; -- 0.1 s timer
		NUM_BITS : natural := 10
		);
	port (
		clk, rst, ena, cnt_sel: in std_logic;
		count: out std_logic_vector(NUM_BITS-1 downto 0)
		);
end entity d2_counter;

architecture rtl of d2_counter is

	signal tick : std_logic := '0';
	
	
-------tick counter oppsett----------


begin 
	p_clk_div: process(rst, clk)
	
		variable clk_cnt : natural range 0 to F_CNT-1;
		
	begin 
		if (rst='0') then
			clk_cnt:= 0;
			tick <= '0';
			
		elsif rising_edge(clk) then
			
			if clk_cnt=F_CNT-1 then
				clk_cnt := 0;
				tick <= '1';
			else
			clk_cnt := clk_cnt +1;
			tick <= '0';
			end if;
			
		end if;
		
	end process p_clk_div;
	
----- system ------------

	p_seq : process (rst, clk) is
		variable bin_q : unsigned(NUM_BITS-1 downto 0);
		variable lfsr_q: std_logic_vector(NUM_BITS-1 downto 0);
		variable fb		: std_logic;
		
	begin
		if rst = '0' then
			bin_q := (others => '0');
			lfsr_q := (others => '0'); 
			lfsr_q(0) := '1';
			count <= (others => '0');
		
		elsif rising_edge(clk) then
			if (ena = '1') and (tick = '1') then
			
			bin_q := bin_q + 1;
			
				if NUM_BITS = 10 then
					fb		:= lfsr_q(9) xor lfsr_q(6);
					lfsr_q:= lfsr_q(NUM_BITS-2 downto 0) & fb;
				else
					lfsr_q:= std_logic_vector(unsigned(lfsr_q)+1);
				end if;
			end if;
			
			if cnt_sel = '0' then
				count <= std_logic_vector(bin_q);
			else
				count <= lfsr_q;
			end if;
		end if;
		
	end process p_seq;

end architecture rtl;
