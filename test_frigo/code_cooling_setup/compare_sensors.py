import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Function to read value (temperature or humidity) and time from csv file
def read_value_time(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file, skiprows=3, skipfooter=1, engine='python')

    # Convert the _time column to datetime
    df['_time'] = pd.to_datetime(df['_time'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
    df['_value'] = pd.to_numeric(df['_value'], errors='coerce')

    # Convert the _start column to datetime
    df['_start'] = pd.to_datetime(df['_start'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')


    df['duration'] = df['_time'] - df['_start']
    df['duration'] = df['duration'].dt.total_seconds() / 3600.

    return df

def plot_temperature(df_temp, df_humi):
    # Filter the data for the specified sensors
    # sensors_temp = ['sensors/disco3A/tempDS', 'sensors/disco3A/tempSCD', 
    #                 'sensors/disco3C/tempDS', 'sensors/disco3C/tempSCD', 
    #                 'sensors/disco40/tempDS', 'sensors/disco40/tempSCD']
    
    # sensors_temp = ['sensors/disco3A/tempDS', 'sensors/disco3A/tempSCD',
    #                 'sensors/disco3C/tempDS', 'sensors/disco3C/tempSCD',
    #                 'sensors/disco40/tempDS', 'sensors/disco40/tempSCD']
    sensors_temp = ['sensors/disco3A/tempSCD', 
                    'sensors/disco3C/tempSCD', 
                    'sensors/disco40/tempSCD']
                    
    filtered_df_temp = df_temp[df_temp['topic'].isin(sensors_temp)]

    sensors_humi = ['sensors/disco3A/humiSCD', 
                    'sensors/disco3C/humiSCD', 
                    'sensors/disco40/humiSCD']
    # 
    filtered_df_temp = df_temp[df_temp['topic'].isin(sensors_temp)]
    filtered_df_humi = df_humi[df_humi['topic'].isin(sensors_humi)]

#     sensors = ['disco3A/DS', 'disco3A/SCD', 
#               'disco3C/DS', 'disco3C/SCD', 
#               'disco40/DS', 'disco40/SCD']
# # 
    # sensors = ['disco3A/SCD', 
    #           'disco3C/SCD', 
    #           'disco40/SCD']

    sensors = ['sensor1', 
              'sensor2', 
              'sensor3']
    
    colors = ['orchid', 'green', 'royalblue']


    # Plot temperature against time for each sensor
    plt.figure(figsize=(10, 6))
    for sensor_temp, sensor_humi, sensor, color in zip(sensors_temp, sensors_humi, sensors, colors):
        dew_point = []
        sensor_data_temp = filtered_df_temp[filtered_df_temp['topic'] == sensor_temp]
        sensor_data_humi = filtered_df_humi[filtered_df_humi['topic'] == sensor_humi]
        print(f"Sensor: {sensor}, Temp Length: {len(sensor_data_temp['_value'])}, Humidity Length: {len(sensor_data_humi['_value'])}")  # Add this line for debugging

        plt.plot(sensor_data_temp['duration'], sensor_data_temp['_value'], label=sensor + ' Temp', color=color)
        # print("sensor_data_temp: ", sensor_data_temp['_value'])
        # Calculate dew point for temperature and humidity data
        dew_point = calculate_dew_point(sensor_data_temp['_value'].values, sensor_data_humi['_value'].values)
        print(f"Sensor: {sensor}, Dew Point Length: {len(dew_point)}")  # Add this line for debugging

        # print("dew_point: ", dew_point)
        plt.plot(sensor_data_temp['duration'], dew_point, label=sensor + ' Dew Point', linestyle='--', color=color)

    # plt.xlabel('Time (HH:MM:SS)')
    plt.xlabel('Duration (hours)')
    plt.ylabel('Temparture (°C) / Dew Point (°C)')
    plt.title('Temperature and Dew Point vs. Time for Different Sensors')
    plt.legend()
 



    # Add grid with finer lines
    plt.grid(True, which='major', linestyle=':', linewidth=0.5)  # Major grid lines
    plt.minorticks_on()  # Enable minor ticks
    plt.grid(True, which='minor', linestyle=':', alpha=0.2)  # Minor grid lines


    # # Increase the number of ticks and the frequency for the time axis
    # plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=30))  # Show ticks every 10 minutes
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # Format time

    # Rotate x-axis labels for better readability (optional)
    plt.xticks(rotation=45)

    plt.tight_layout()  # Adjust layout to prevent clipping of labels

    plt.savefig('./plots_dp_ice/temperature_and_dew_point_plot_15_04_24_test6.pdf')
    plt.savefig('./plots_dp_ice/temperature_and_dew_point_plot_15_04_24_test6.png')
    plt.show()


def calculate_dew_point(temperature, humidity):
    humidity_relative = humidity / 100.  # Convert percentage to fraction

    # Initialize an empty array to store dew point values
    dew_point = np.empty_like(temperature)

    for i in range(len(temperature)):
        # Calculate f(T)
        # f_T = np.log(humidity_relative[i]) + (18.678 - temperature[i] / 234.5) * (temperature[i] / (257.14 + temperature[i]))
        f_T = np.log(humidity_relative[i]) + (23.036 - temperature[i] / 333.7) * (temperature[i] / (279.82 + temperature[i]))

        # Calculate g(T)
        # g_T = 257.14 * f_T / (18.678 - f_T)
        g_T = 279.82 * f_T / (23.036 - f_T)


        # Store the dew point value in the array
        dew_point[i] = g_T

    return dew_point

# Example usage

csv_file_temp = './../15_04_24/test6/2024-04-18_09_49_influxdb_data_temp.csv' 
csv_file_humi = './../15_04_24/test6/2024-04-18_09_50_influxdb_data_humi.csv'
df_temp = read_value_time(csv_file_temp)
df_humi = read_value_time(csv_file_humi)

plot_temperature(df_temp, df_humi)


# Frigo 1 : Potentiellement comparer test 6 et 7 aves les puissances de resistance différentes pour le frigo 1.
#  Peut etre qu’il faudrait utiliser aussi test 4 meme si les capteurs n’etaient pas posés sur la grille  

    
    

