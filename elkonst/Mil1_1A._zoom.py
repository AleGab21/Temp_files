import pandas as pd
import matplotlib.pyplot as plt

# Load the data 
file_path = r"C:\Users\alex_\OneDrive\Skrivebord\NTNU\Elektro konstruksjon\misc\Elkonst_prosjekt_mile1_1A_text.txt"
data = pd.read_csv(file_path, sep='\s+')

# Convert time from seconds to milliseconds (if needed)
data['time_ms'] = data['time'] * 1000  # Assuming time is in seconds

# Filter for the 12 ms to 15 ms range
filtered_data = data[(data['time_ms'] >= 12.2) & (data['time_ms'] <= 12.3)]

# Plot the filtered data
plt.figure(figsize=(10, 6))
plt.plot(filtered_data['time_ms'], filtered_data['V(vout)'], label='Volt (ved 12.20-12.30 ms)')
plt.xlabel('Tid (ms)')
plt.ylabel('Volt (V)')
plt.title('Volt vs Tid 1 ohm')
plt.legend()
plt.grid()
plt.show()
