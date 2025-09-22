"""
Time Of Flight Distance Sensor Calibration Module
Authors: Tomás Suárez, Agustín Corazza, Rodrigo Pérez
University: Universidad Nacional de Cuyo
For this example we use an arduino UNO connected with a VL53L0/1XV2 module, containing a VL53L0X sensor, as indicated in "connection.png" with 
"VL53L0X_Continuous.ino" code, both found in "arduiono code" folder.
"""

from TimeOfFlightCalibrationModules.utils import log_data_from_tof_distance_sensor

file_name = log_data_from_tof_distance_sensor('COM7', 38400, t_log=60*60*5) # Signal characterization data log
print(f"\nData has been saved in the following file: {file_name}")

