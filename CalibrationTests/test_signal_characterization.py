"""
Time Of Flight distance sensor signal characterization test
Authors: Tomás Suárez, Agustín Corazza, Rodrigo Pérez
University: Universidad Nacional de Cuyo
"""

import numpy as np
from TimeOfFlightCalibrationModules import tof_distance_calibration as tof
from TimeOfFlightCalibrationModules.utils import extract_tof_distance_data, show_time_data

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
print(f"Number of samples in the file: {n_samples}")


# Recorded data
show_time_data(tof_data, sampling_freq, ["Distance [mm]"])

time_vector = np.arange(0, n_samples, 1) / sampling_freq

# Compute Allan Variance
tau, avar = tof.compute_allan_variance(tof_data, sampling_freq, m_steps='exponential')
dist_a_dev = np.sqrt(avar).reshape(-1)

# Estimate R and q values
R, q, tauwn, taurw = tof.auto_estimate_R_q_from_allan(tau, dist_a_dev, sampling_freq, plot=True)

# Show results
print(f"TOF distance sensor white measurement–noise variance [mm²]: {R}")
print(f"TOF distance sensor bias random–walk intensity [mm²/s]: {q}")

# Save data if required
if save:
    np.savetxt("characterization result data/R_q_bar_alt.csv", (R, q), delimiter=',')

# Show time data and simulated data.
sim_data = tof.simulate_sensor_data(n_samples, sampling_freq, R, q, np.mean(tof_data))
show_time_data(np.vstack([tof_data, sim_data]).T, sampling_freq, ["Logged Signal", "Simulated Signal"])


