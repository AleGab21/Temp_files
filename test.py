import pandas as pd
import matplotlib.pyplot as plt

# Load the first dataset
file_path1 = r"C:\Users\alex_\OneDrive\Skrivebord\NTNU\Elektro konstruksjon\misc\Elkonst_prosjekt_mile1_10mA_text.txt"
data1 = pd.read_csv(file_path1, sep='\s+')
data1['time_ms'] = data1['time'] * 1000  # Convert time to milliseconds
data1['V(vout)_mV'] = data1['V(vout)'] * 1000  # Convert voltage to millivolts

# Load the second dataset
file_path2 = r"C:\Users\alex_\OneDrive\Skrivebord\NTNU\Elektro konstruksjon\misc\Elkonst_prosjekt_mile1_100mA_text.txt"
data2 = pd.read_csv(file_path2, sep='\s+')
data2['time_ms'] = data2['time'] * 1000  # Convert time to milliseconds
data2['V(vout)_mV'] = data2['V(vout)'] * 1000  # Convert voltage to millivolts

# Load the thrid dataset
file_path3 = r"C:\Users\alex_\OneDrive\Skrivebord\NTNU\Elektro Konstruksjon\misc\Elkonst_prosjekt_mile1_1A_text.txt"
data3 = pd.read_csv(file_path3, sep='\s+')
data3['time_ms'] = data3['time'] * 1000  # Convert time to milliseconds
data3['V(vout)_mV'] = data3['V(vout)'] * 1000  # Convert voltage to millivolts

# Load the fourth dataset
file_path4 = r"C:\Users\alex_\OneDrive\Skrivebord\NTNU\Elektro konstruksjon\misc\Elkonst_prosjekt_mile1_2A_text.txt"
data4 = pd.read_csv(file_path4, sep='\s+')
data4['time_ms'] = data4['time'] * 1000  # Convert time to milliseconds
data4['V(vout)_mV'] = data4['V(vout)'] * 1000  # Convert voltage to millivolts

# Filter for the 12 ms to 15 ms range in both datasets
filtered_data1 = data1[(data1['time_ms'] >= 13) & (data1['time_ms'] <= 13.1)]
filtered_data2 = data2[(data2['time_ms'] >= 13) & (data2['time_ms'] <= 13.1)]
filtered_data3 = data3[(data3['time_ms'] >= 13) & (data3['time_ms'] <= 13.1)]
filtered_data4 = data4[(data4['time_ms'] >= 13) & (data4['time_ms'] <= 13.1)]

# Plot the data from the first file
plt.figure(figsize=(10, 6))
plt.plot(filtered_data1['time_ms'], filtered_data1['V(vout)_mV'], label='10mA: V(vout)', color='red')

# Plot the data from the second file
plt.plot(filtered_data2['time_ms'], filtered_data2['V(vout)_mV'], label='100mA: V(vout)', color='blue')

# Plot the data from the second file
plt.plot(filtered_data3['time_ms'], filtered_data3['V(vout)_mV'], label='1A: V(vout)', color='black')

# Plot the data from the second file
plt.plot(filtered_data4['time_ms'], filtered_data4['V(vout)_mV'], label='2A: V(vout)', color='green')

# Add labels, legend, and grid
plt.xlabel('Tid (ms)')
plt.ylabel('Volt (mV)')
plt.title('Sammenligning av rippel-spenning fra 4 forskjellige laster')
plt.legend()
plt.grid()
plt.show()
