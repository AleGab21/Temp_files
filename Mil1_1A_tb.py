import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = r"C:\Users\alex_\OneDrive\Skrivebord\NTNU\Elektro konstruksjon\misc\Elkonst_prosjekt_mile1_1A_text.txt"
data = pd.read_csv(file_path, sep='\s+')

# Convert time from seconds to milliseconds (if needed)
data['time_ms'] = data['time'] * 1000  # Assuming time is in seconds

# Convert voltage to millivolts
data['V(vout)_mV'] = data['V(vout)'] * 1000  # Convert to millivolts

# Filter for the 12 ms to 15 ms range
filtered_data = data[(data['time_ms'] >= 13) & (data['time_ms'] <= 13.005)]

# Find the highest and lowest values in millivolts
max_value = filtered_data['V(vout)_mV'].max()
min_value = filtered_data['V(vout)_mV'].min()
max_time = filtered_data[filtered_data['V(vout)_mV'] == max_value]['time_ms'].values[0]
min_time = filtered_data[filtered_data['V(vout)_mV'] == min_value]['time_ms'].values[0]

# Plot the filtered data
plt.figure(figsize=(10, 6))
plt.plot(filtered_data['time_ms'], filtered_data['V(vout)_mV'], label='Volt')

# Mark the maximum value
plt.axhline(y=max_value, color='red', linestyle='--', label=f'Max: {max_value:.2f} mV')
plt.axvline(x=max_time, color='red', linestyle='--')
plt.text(max_time, max_value, f'{max_value:.2f} mV', color='red', ha='left')

# Mark the minimum value
plt.axhline(y=min_value, color='blue', linestyle='--', label=f'Min: {min_value:.2f} mV')
plt.axvline(x=min_time, color='blue', linestyle='--')
plt.text(min_time, min_value, f'{min_value:.2f} mV', color='blue', ha='left')

# Add labels, legend, and grid
plt.xlabel('Tid (ms)')
plt.ylabel('Volt (mV)')
plt.title('Volt vs Tid (1 ohm) med ekstremverdier')
plt.legend()
plt.grid()
plt.show()

# Print the extreme values
print(f"Maximum Value: {max_value:.2f} mV")
print(f"Minimum Value: {min_value:.2f} mV")
