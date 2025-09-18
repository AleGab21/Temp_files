library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity registered_adder is  
end entity;


architecture testbench of registered_adder_tb is
	signal clk: std_logic := '1';
	signal a, b: std_logic_vector(2 downto 0) := "000";
	signal sum, sum_reg: std_logic_vector(3 downto 0);
begin

	duv: entity work.registered_adder
		port map (clk, a, b, sum, sum_reg);
		
	clk <= not clk after 40 ns;
	a <= "101" after 40 ns;
	b <= "010" after 40 ns, "100" after 120 ns, "111" after 200 ns;

end architecture