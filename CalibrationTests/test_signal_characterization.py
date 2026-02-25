"""
Time Of Flight distance sensor signal characterization test
Authors: Tomás Suárez, Agustín Corazza, Rodrigo Pérez
University: Universidad Nacional de Cuyo
"""

import numpy as np
from TimeOfFlightCalibrationModules import tof_distance_calibration as tof
from TimeOfFlightCalibrationModules.utils import extract_tof_distance_data, show_time_data

spanish = True

# Use synthetic data
synthetic = False

# Save data flag
save = True

# Read data
if not synthetic:
    file_name = "characterization data/static_tof_dist_data_1_h.csv" 
    params, tof_data = extract_tof_distance_data(file_name)
    sampling_freq, t_init = params
else:
    R_real = 0.001
    q_real = 0.00001
    sampling_freq = 80
    tof_data = tof.simulate_sensor_data(60000,sampling_freq, R_real, q_real)
tof_data = np.hstack([tof_data, tof_data])
n_samples = tof_data.shape[0]

time_vector = np.arange(0, n_samples, 1) / sampling_freq

# Compute Allan Variance
tau, avar = tof.compute_allan_variance(tof_data, sampling_freq, m_steps='exponential')
dist_a_dev = np.sqrt(avar).reshape(-1)

# Estimate R and q values
if spanish:
    plot_title = "Desviación de Allan del sensor de tiempo de vuelo"
else:
    plot_title = "Allan Deviation of Time of Flight sensor"
R, q, tauwn, taurw = tof.auto_estimate_R_q_from_allan(tau, dist_a_dev, sampling_freq, plot=True, u='mm', title=plot_title, spanish=spanish)

# Show results
if spanish:
    print(f">>> Número de muestras en el archivo: {n_samples}")
    print(f">>> Varianza del ruido blanco gaussiano de medición del sensor [mm²]: {R}")
    print(f">>> Intensidad de la caminata aleatoria del sesgo del sensor [mm²/s]: {q}")
else:
    print(f">>> Number of samples in the file: {n_samples}")
    print(f">>> TOF distance sensor white measurement–noise variance [mm²]: {R}")
    print(f">>> TOF distance sensor bias random–walk intensity [mm²/s]: {q}")

# Save data if required
if save:
    np.savetxt("characterization result data/R_q_bar_alt.csv", (R, q), delimiter=',')

# Show time data and simulated data.
sim_data = tof.simulate_sensor_data(n_samples, sampling_freq, R, q, np.mean(tof_data))
if spanish:
    plot_title_1 = "Comparación de señales sensor de tiempo de vuelo"
    plot_xlabel = "Tiempo [s]"
    plot_ylabel = "[mm]"
    plot_legend = ["Señal medida", "Señal simulada"]
else:
    plot_title_1 = "Time of Flight Sensor signal comparison"
    plot_xlabel = "Time [s]"
    plot_ylabel = "[mm]"
    plot_legend = ["Logged Signal", "Simulated Signal"]

show_time_data(np.vstack([tof_data, sim_data]).T[:4000,:], sampling_freq, legend=plot_legend, 
               title=plot_title_1, xlabel=plot_xlabel, ylabel=plot_ylabel)


