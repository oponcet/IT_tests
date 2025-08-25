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
        # df['duration'] = df['duration'].dt.total_seconds()
        df['duration'] = df['duration'].dt.total_seconds() / 3600.

        # Append the DataFrame to the list
        dfs.append(df)

    return dfs

def plot_temperature_and_dewpoint(df_temps, df_humis):
    sensors_temp = ['sensors/disco40/tempSCD']
    sensors_humi = ['sensors/disco40/humiSCD']
    tests = ['resistor: 3.6W', 'resistor: 9.3W']
    colors = ['orange', 'red']

    plt.figure(figsize=(10, 6))
    for df_temp, df_humi, color, test in zip(df_temps, df_humis, colors, tests):
        for sensor_temp, sensor_humi in zip(sensors_temp, sensors_humi):
            filtered_df_temp = df_temp[df_temp['topic'] == sensor_temp]
            filtered_df_humi = df_humi[df_humi['topic'] == sensor_humi]

            plt.plot(filtered_df_temp['duration'], filtered_df_temp['_value'], label=test + ' Temp', color=color)
            dew_point = calculate_dew_point(filtered_df_temp['_value'].values, filtered_df_humi['_value'].values)
            plt.plot(filtered_df_temp['duration'], dew_point, label=test + ' Dew Point', linestyle='--', color=color)

    # plt.xlabel('Duration (seconds)')
    plt.xlabel('Duration (hours)')
    plt.ylabel('Temperature (°C) / Dew Point (°C)')
    plt.title('Temperature and Dew Point vs. Duration for different values of the power resistor')
    plt.legend()

    plt.grid(True, which='major', linestyle=':', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(True, which='minor', linestyle=':', alpha=0.2)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('./plots_dp_ice/temperature_and_dewpoint_resistor_normal.png')
    plt.savefig('./plots_dp_ice/temperature_and_dewpoint_resistor_normal.pdf')

    # plt.show()

def calculate_dew_point(temperature, humidity):
    humidity_relative = humidity / 100.
    dew_point = np.empty_like(temperature)

    for i in range(len(temperature)):
        # f_T = np.log(humidity_relative[i]) + (18.678 - temperature[i] / 234.5) * (temperature[i] / (257.14 + temperature[i]))
        f_T = np.log(humidity_relative[i]) + (23.036 - temperature[i] / 333.7) * (temperature[i] / (279.82 + temperature[i]))
        # g_T = 257.14 * f_T / (18.678 - f_T)
        g_T = 279.82 * f_T / (23.036 - f_T)
        dew_point[i] = g_T

    return dew_point

def plot_humidity(df_humis):
    sensors_humi = 'sensors/disco40/humiSCD'
    tests = ['resistor: 3.6W', 'resistor: 9.3W']
    colors = ['orange', 'red']

    plt.figure(figsize=(10, 6))
    for df_humi, color, test in zip(df_humis, colors, tests):
        filtered_df_humi = df_humi[df_humi['topic'] == sensors_humi]

        plt.plot(filtered_df_humi['duration'], filtered_df_humi['_value'], label=test + ' Humidity', color=color)

    # plt.xlabel('Duration (seconds)')
    plt.xlabel('Duration (hours)')
    plt.ylabel('Humidity (%)')
    plt.title('Humidity vs. Duration for different values of the power resistor')
    plt.legend()

    plt.grid(True, which='major', linestyle=':', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(True, which='minor', linestyle=':', alpha=0.2)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('./plots_dp_ice/humidity_resistor_normal.png')
    plt.savefig('./plots_dp_ice/humidity_resistor_normal.pdf')
    # plt.show()

#### 
csv_files_temp = ['./../15_04_24/test6/2024-04-18_09_49_influxdb_data_temp.csv',
                  './../18_04_24/test7/2024-04-18_09_19_influxdb_data_temp.csv']
csv_files_humi = ['./../15_04_24/test6/2024-04-18_09_50_influxdb_data_humi.csv',
                  './../18_04_24/test7/2024-04-18_09_20_influxdb_data_humi.csv']


df_humis = read_value_duration(csv_files_humi)

plot_humidity(df_humis)

df_temps = read_value_duration(csv_files_temp)
df_humis = read_value_duration(csv_files_humi)

plot_temperature_and_dewpoint(df_temps, df_humis)
