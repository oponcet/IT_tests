import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Function to read value (temperature or humidity) and calculate duration from start time
def read_value_duration(csv_files):
    dfs = []
    for csv_file in csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3, skipfooter=1, engine='python')

        # Convert the _start column to datetime
        df['_start'] = pd.to_datetime(df['_start'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')

        # Convert the _time column to datetime
        df['_time'] = pd.to_datetime(df['_time'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')

        # Calculate the duration by subtracting the start time from each time
        df['duration'] = df['_time'] - df['_start']

        # Convert duration to seconds
        df['duration'] = df['duration'].dt.total_seconds()

        # Append the DataFrame to the list
        dfs.append(df)

    return dfs

def calculate_dew_point(temperature, humidity):
    humidity_relative = humidity / 100.  # Convert percentage to fraction
    # Initialize an empty array to store dew point values
    dew_point = np.empty_like(temperature)

    for i in range(len(temperature)):
        # Calculate f(T)
        f_T = np.log(humidity_relative[i]) + (18.678 - temperature[i] / 234.5) * (temperature[i] / (257.14 + temperature[i]))
        
        # Calculate g(T)
        g_T = 257.14 * f_T / (18.678 - f_T)

        # Store the dew point value in the array
        dew_point[i] = g_T

    return dew_point


def plot_temperature_dewpoint_humidity(df_temp, df_humi):
    sensor_temp = 'sensors/disco40/tempSCD'
    sensor_humi = 'sensors/disco40/humiSCD'

    filtered_df_temp = df_temp[df_temp['topic'] == sensor_temp]
    filtered_df_humi = df_humi[df_humi['topic'] == sensor_humi]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot temperature
    ax1.plot(filtered_df_temp['duration'], filtered_df_temp['_value'], label='Temp', color='royalblue')

    # Plot dew point
    dew_point = calculate_dew_point(filtered_df_temp['_value'].values, filtered_df_humi['_value'].values)
    ax1.plot(filtered_df_temp['duration'], dew_point, label='Dew Point', linestyle='--', color='mediumorchid')

    ax1.set_xlabel('Duration (seconds)')
    ax1.set_ylabel('Temperature (°C) / Dew Point (°C)')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # Create a secondary y-axis sharing the same x-axis
    ax2.plot(filtered_df_humi['duration'], filtered_df_humi['_value'].values, label='Relative Humidity (%)', color='crimson')
    ax2.set_ylabel('Relative Humidity (%)')
    ax2.tick_params(axis='y')

    fig.tight_layout()
    plt.title('Temperature, Dew Point, and Humidity vs. Duration')
    fig.legend(loc='upper right')

    plt.grid(True, which='major', linestyle=':', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(True, which='minor', linestyle=':', alpha=0.2)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('temperature_dewpoint_humidity.png')
    plt.show()


# Read temperature and humidity data for one test
csv_file_temp = './../18_04_24/test7/2024-04-18_09_19_influxdb_data_temp.csv'
csv_file_humi = './../18_04_24/test7/2024-04-18_09_20_influxdb_data_humi.csv'

df_temp = read_value_duration([csv_file_temp])[0]
df_humi = read_value_duration([csv_file_humi])[0]

# Plot temperature, dew point, and humidity
plot_temperature_dewpoint_humidity(df_temp, df_humi)
