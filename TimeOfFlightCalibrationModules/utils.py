"""
utils module from Time Of Flight Distance Sensor Calibration Module
Authors: Tomás Suárez, Agustín Corazza, Rodrigo Pérez
University: Universidad Nacional de Cuyo
"""

import csv
from datetime import datetime
import serial
import time
from typing import Tuple, Union

import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')
plt.rcParams['font.family'] = 'Times New Roman'

def log_data_from_tof_distance_sensor(
    port: str,
    baud_rate: int,
    t_log: Union[int, float] = 120
) -> str:
    """
    Log distance data in mm from a VL53L0X time of flight distance sensor via UART communication. 
    You will need "VL53L0X_Continuous.ino" code in Arduino UNO and connected as shown in "connections.png",
    you can find both files in "arduino code" folder.
    You must keep your sensor steady on a table, for example, pointing to a fixed distance object 
    in order to get data for signal characterization.

    Args:
        port: Serial port for communication (e.g., 'COM3')
        baud_rate: Baud rate for serial communication (e.g., 38400)
        t_log: Data logging time interval (seconds)

    Returns:
        str: Filename of the generated CSV file containing logged data

    Raises:
        serial.SerialException: If serial communication fails

    Output CSV format:
        - First row: Fs, sampling_frequency (Hz)
        - Second row: Logging time, t_log 
        - Third row: h, temp (column headers)
        - Subsequent rows: [h,temp] (sensor readings)

    Notes:
        - You must reset your Arduino UNO every time you want to use this function
    """
    error_data = 0 # Counter for corrupt data lines.

    def save_line(
        ser: serial.Serial, 
        writer: csv.writer
    ) -> None:
        """
        Read, validate, and save a single line of tof distance data.

        Args:
            ser: Active serial connection
            writer: CSV writer object
        """
        nonlocal error_data
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data = [float(val) for val in line.split(',')]
                if len(data) == 1:
                    writer.writerow(data)   
        except (ValueError, UnicodeDecodeError) as e:
            error_data += 1
            if error_data % 100 == 0: # Only print periodic error to avoid flooding
                print(f"Corrupt data (total errors: {error_data}): {e}")

    # Generate output file with timestamp
    time_stamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    output_file = f"tof_distance_data_{time_stamp}_cal.csv"

    try:
        with serial.Serial(port, baud_rate, timeout=1) as ser, open(output_file, 'w', newline='') as csvfile:
            print(f">>> Connected to {port}.")
            print(">>> Waiting for TOF initialization...")

            # Wait for VL53L0X connection confirmation
            while True:
                response = ser.readline().decode('utf-8').strip()
                if response == "VL53L0X connection succesful":
                    break
                elif response == "VL53L0X connection failed":
                    raise RuntimeError("VL53L0X connection failed")

            # Get sampling frecuency
            while True:
                response = ser.readline().decode('utf-8').strip()
                if response == "Selected sampling frequency:":
                    sampling_freq = ser.readline().decode('utf-8').strip()
                    break

            print(f">>> Sampling frecuency: {sampling_freq} Hz")

            # Initialize CSV file
            writer = csv.writer(csvfile)
            writer.writerow(["Fs", sampling_freq])
            writer.writerow(["Logging time", t_log])
            writer.writerow(["d"])

            print(f">>> In order to logged data for signal characterization, hold the tof distance sensor pointing steady to an object for {t_log} seconds")
            print(">>> Press any letter to start: ")
            input() # Wait for user input
            ser.write(b' ') # Send any byte to start

            # Wait for data collection to start
            while True:
                if ser.readline().decode('utf-8').strip() == "Getting distance data in mm...":
                    break

            print(">>> Data logging process has started")
      
            # Data collection
            t_static_start = time.time()
            while time.time() - t_static_start < t_log:
                save_line(ser, writer)

            print("\n>>> Capture completed")
            print(f"\n>>> Total corrupt data lines: {error_data}")

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
        raise

    return output_file

def extract_tof_distance_data(
    file_name: str
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract tof distance sensor data and parameters from a CSV log file.

    Args:
        file_name: Path to the CSV file containing logged tof distance sensor data.

    Returns:
        A tuple containing:
        - params: Array of parameters:
            [fs, t_log]
        - data: Array of shape (N, 1) containing tof distance sensor measurements (distance in mm):
            [d]

    Raises:
        ValueError: If the file format is invalid
        FileNotFoundError: If the file doesn't exist

    Notes:
        - First 2 rows must contain metadata:
          1. fs: sampling frequency
          2. t_log: logging time  
        - Subsequent rows contain tof distance measured data
    """

    try:
        # Read and parse metadata in one pass
        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            metadata = [next(reader) for _ in range(2)]
            
        # Convert metadata with proper error handling
        fs = float(metadata[0][1])
        t_log = int(metadata[1][1])
        
        params = [fs, t_log]

        # Load data efficiently with numpy
        data = np.loadtxt(file_name, delimiter=',', skiprows=3, dtype=np.float32)

        return np.array(params, dtype=np.float32), data

    except (IndexError, ValueError) as e:
        raise ValueError(f"Invalid file format in {file_name}") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_name}") from e
    
def show_loglog_data(
    x_data: np.ndarray,
    y_data: np.ndarray, 
    fs: Union[int,float],
    legend: str,
    xlabel: str,
    ylabel: str,
    title: str,
    spanish: bool=False
) -> None:
    """
    Show data plot in double logaritmic axes.

    Args:
        x_data: Data array of shape (N,M) where N is number of samples and M the numer of curves.
        y_data: Data array of shape (N,M) where N is number of samples and M the numer of curves.
        fs: Sampling rate in Hz.
        legend: Data legend.
        xlabel: X axis label.
        ylabel: Y axis label.
        title: Figure title.
        spanish: Spanish comments.

    Returns:
        None
    """

    # Visualization
    _, ax1 = plt.subplots(figsize=(14, 7))

    def tau_to_samples(tau):
        return tau * fs

    def samples_to_tau(N):
        return N / fs

    lines = ax1.loglog(x_data, y_data, linewidth=0.8)
    for line, label in zip(lines, legend):
        line.set_label(label)
    ax1.grid(True, which='major', linestyle='-', linewidth=0.8)
    ax1.grid(True, which='minor', linestyle='--', linewidth=0.5, alpha=0.7)
    ax1.set_xlabel(xlabel, fontsize=14)
    ax1.set_ylabel(ylabel, fontsize=14)
    ax1.set_title(title, fontsize=18, fontweight='bold', pad=15)
    secax = ax1.secondary_xaxis(
        'top',
        functions=(tau_to_samples, samples_to_tau)
    )

    if spanish:
        secax_label = "Número de muestras"
    else:
        secax_label = "Number of Samples"
    secax.set_xlabel(secax_label, fontsize=14)
    handles, _ = ax1.get_legend_handles_labels()
    ax1.legend(
        handles=handles,
        fontsize=14,
        loc="best",
        frameon=True,        
        fancybox=False,     
        framealpha=1.0,      
        edgecolor='black',  
        facecolor='white'   
    )
    secax.tick_params(
        axis='x',
        which='major',
        direction='in',
        length=6,
        width=1.2,
        labelsize=14
    )
    ax1.tick_params(
        axis='both',
        which='major',
        direction='in',
        length=6,
        width=1.2,
        labelsize=14
    )
    plt.tight_layout()
    plt.show()

def show_time_data(
    data: np.ndarray, 
    fs: Union[int,float], 
    legend: list,
    xlabel: str="Time [s]",
    ylabel: str="Sensor measurement data [u]",
    title: str="Sensor data"
) -> None:
    """
    Show sensor data as a function of time.

    Args:
        data: Data array of shape (N,) where N is number of samples.
        fs: Sampling rate in Hz.
        legend: Plot legend.
        xlabel: X axis label.
        ylabel: Y axis label.
        title: Figure title.

    Returns:
        None
    """
    n_samples = data.shape[0]

    # Time vector
    time_vector = np.arange(0, n_samples, 1) / fs

    _, ax1 = plt.subplots(figsize=(12, 7))
    lines = ax1.plot(time_vector, data, linewidth=1)
    for line, label in zip(lines, legend):
        line.set_label(label)
    ax1.grid(True)
    ax1.set_xlabel(xlabel, fontsize=14)
    ax1.set_xlim(time_vector[0], time_vector[-1])
    ax1.set_ylabel(ylabel, fontsize=14)
    ax1.set_title(title, fontsize=18, fontweight='bold', pad=15)
    handles, _ = ax1.get_legend_handles_labels()
    ax1.legend(
        handles=handles,
        fontsize=12,
        loc="best",
        frameon=True,        
        fancybox=False,     
        framealpha=1.0,      
        edgecolor='black',  
        facecolor='white'   
    )
    ax1.tick_params(
        axis='both',
        which='major',
        direction='in',
        length=6,
        width=1.2,
        labelsize=14
    )

    plt.show()