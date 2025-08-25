# Voltage,Current mean, Standard Deviation, Delta I (.csv)

"""
author: @oponcet
date: 2025-02

Ce script permet de lire deux fichiers Excel contenant des données IV (courant-tension) et de tracer les courbes IV
Les fichier sont souf format cvs 
premeire ligne = Voltage,Current mean, Standard Deviation, Delta I (.csv)

"""
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_file(file_path):
    """
    Reads a CSV file and returns arrays for voltage, current mean, and standard deviation of current.
    Assumes data is comma-separated and has no header row.
    """
    # Read CSV without header and assign column names
    df = pd.read_csv(file_path, names=["Voltage", "Current mean", "Standard Deviation", "Delta I"])

    # Skip the first row if necessary
    df = df[1:].astype(float)

    # Extract relevant columns
    tension = df["Voltage"].tolist()
    current = df["Current mean"].tolist()
    std_current = df["Standard Deviation"].tolist()

    # convert the values from A to uA

    current = [i * 1e6 for i in current]
    std_current = [i * 1e6 for i in std_current]

    print(f"First row - tension: {tension[0]}, current: {current[0]}, std_current: {std_current[0]}")

    return tension, current, std_current

def plot_iv_curve(data_list, labels, save_path=None):
    """
    Plots IV curves with error bars for multiple datasets on the same graph.
    
    Parameters:
    - data_list: List of tuples (tension, current, std_current)
    - labels: List of labels corresponding to each dataset
    - save_path: Optional path to save the figure
    """
    plt.figure(figsize=(8, 6))

    colors = ['royalblue', 'darkorange', 'green', 'red', 'purple']  # Different colors for each dataset
    
    for i, (tension, current, std_current) in enumerate(data_list):
        plt.errorbar(tension, current, yerr=std_current, xerr=None,
                     linestyle='', color=colors[i % len(colors)],  marker='.',
                     capsize=5, label=f"T = {labels[i]}°C")

    # Graph details
    plt.title("IV Curve")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (µA)")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    

    # Flip x-axis and y-axis
    plt.xlim(0, -100)
    plt.ylim(0, -1000)  # µA

    # Set major ticks on the x-axis
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(10))

    # Add legend
    plt.legend()

    # Save plot if save_path is provided
    if save_path:
        plt.savefig(f"{save_path}.pdf")
        plt.savefig(f"{save_path}.png")

    # Display the plot
    plt.show()

def main():
    # Define file paths and corresponding temperature labels
    file_paths = [
        "/Users/oponcet/cernbox/test/IV_curve_automated/data/T34.csv",
        "/Users/oponcet/cernbox/test/IV_curve_automated/data/T30.csv",  # Example additional dataset
        "/Users/oponcet/cernbox/test/IV_curve_automated/data/T26.csv",
        "/Users/oponcet/cernbox/test/IV_curve_automated/data/T23.csv"
    ]
    temp_labels = ["[-32.4;-34.4]", "[-30.7,-28.2]", "[-28.7,-25.4]", "[-26.4,-23.1]"]

    # Read data from all files
    data_list = [read_file(path) for path in file_paths]

    # Plot IV curves for all datasets
    plot_iv_curve(data_list, temp_labels, save_path="/Users/oponcet/cernbox/test/IV_curve_automated/output/IV_automated")

if __name__ == "__main__":
    main()
