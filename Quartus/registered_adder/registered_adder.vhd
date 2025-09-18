library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity registered_adder is  -- beskrivelse av grensesnittet til systemet
	port (
		clk: in std_logic; -- definerer klokkesignal
		a, b: in std_logic_vector(2 downto 0); -- definerer 2 variabler/inngang på 3 bits
		sum, sum_reg: out std_logic_vector(3 downto 0)); -- definerer en sum/utgang som skal kunne være 4 bit (for carry)
end entity;



architecture rtl of registered_adder is --kode logikken
begin 
	-- kombinatorisk addiasjon
	sum <= std_logic_vector(('0' & unsigned(a)) + unsigned(b)); -- forlenger a til 4 bits og legger a+b som sum
	
	process(clk) -- sekvensiell bit som styrer klokken
		begin
		if rising_edge(clk) then
			sum_reg <= sum; -- lagrer sum som sum_reg bare på klokkes økende side
		end if;
	end process;
end architecture;