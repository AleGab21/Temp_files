import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = r"C:\Users\alex_\OneDrive\Skrivebord\NTNU\Elektro konstruksjon\misc\Elkonst_prosjekt_mile1_1A_text.txt"
data = pd.read_csv(file_path, sep='\s+')

# Inspect column names
print(data.columns)  # Verify column names

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data['time'], data['V(vout)'], label='Volt')  # Use actual column names
plt.xlabel('Tid (s)')
plt.ylabel('Volt (V)')
plt.title('LTSpice Sim 1 Ohm')
plt.legend()
plt.grid()
plt.show()
