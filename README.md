# 📏 Time of Flight Distance Sensor Calibration (VL53L0X / VL53L0X/1XV2)

This repository provides tools to **characterize and analyze the noise of time of flight distance sensors** using Allan Deviation analysis.
It is based on the **VL53L0X sensor**.

The goal is to model and understand the sensor’s noise processes (white noise, bias random walk) and prepare the ground for future **automatic calibration** methods.

---

## ⚙️ How It Works

The repository implements a workflow to record, process, and analyze TOF distance data:

1. **Raw Data Acquisition**

   * Data is collected from an VL53L0X sensor.
   * Measurements are logged at a fixed sampling rate (default: about 50 Hz ).

2. **Allan Deviation Analysis**

   * From the altitude time series, Allan deviation (ADEV) is computed across multiple averaging times (τ).
   * This reveals how different noise sources dominate at different time scales:

     * **White noise (σ ∝ 1/√τ)**
     * **Random walk bias (σ ∝ √τ)**

3. **Noise Parameter Estimation**

   * The slopes of the Allan deviation curve are fitted to extract:

     * **R** → Measurement noise variance (white noise level).
     * **q** → Random walk bias intensity.

For a complete mathematical background derivation, refer to the theory folder.

## ✨ Features

* 📊 Allan deviation analysis of time of flight distance sensor data
* 🔎 Automatic estimation of **white noise variance (R)** and **random walk intensity (q)**
* 📈 Visualization tools for ADEV curves and slope fitting
* 🧩 Modular Python implementation
* 🔌 Includes Arduino sketch for raw data acquisition via I2C/UART

---

## 👨‍💻 Authors

**Tomás Suárez, Agustín Corazza, Rodrigo Pérez**  
Mechatronics Engineering Students 
Universidad Nacional de Cuyo  
📧 suareztomasm@gmail.com
📧 corazzaagustin@gmail.com
📧 rodrigoperez2110@gmail.com

---

## 📁 Project Structure

```text
TimeOfFlightCalibration/
├── arduino code/                    # Arduino interface for VL53L0X
│   ├── connection.png               # Wiring diagram (Arduino UNO ↔ VL53L0X/1XV2)
│   ├── VL53L0X/                     # Arduino library (C++ .h/.cpp)
│   ├── VL53L0X_Continuous.ino       # Arduino sketch for UART streaming
│   └── VL53L0X.pdf                  # Sensor datasheet
├── TimeOfFlightCalibration/         # Core Python modules
│   ├── tof_distance_calibration.py  # Main calibration logic
│   └── utils.py                     # Helpers and data loaders
├── CalibrationTests/                # Example test scripts
├── characterization data/           # Example CSV datasets
├── characterization result images/  # Sample plots (simulated vs real)
├── characterization result data/    # CSV of computed signal characterization parameters
├── LICENSE                          # MIT License
├── README.md                        # This file
└── requirements.txt                 # Python dependencies
```

---

## 🚀 Quick Start

### 1. 📥 Clone the Repository

```bash
git clone https://github.com/tomisuarez2/TimeOfFlightCalibration
cd TimeOfFlightCalibration
```

### 2. 📦 Install Requirements

```bash
pip install -r requirements.txt
```

### 3. ▶️ Run Example Analysis

```bash
python -m CalibrationTests.test_signal_characerization
```

---

## 📊 Example Output

* **Allan deviation curve** with fitted slopes
* Estimated noise parameters:

 ```bash
 TOF distance sensor white measurement–noise variance [mm²]: 4.838151315541122
 TOF distance sensor bias random–walk intensity [mm²/s]: nan
 ```
* Visualization of white noise (−½ slope) and random walk (+½ slope) regions

![Allan Deviation Plot](characterization%20result%20images/allan_dev_plot.png)

![Real vs Simulated data](characterization%20result%20images/real_vs_sim.png)

It can be seen from above pictures that there is no apreciable random bias walk sensor noise, at least in these recorded data.

---

## 📈 Input Data Format

CSV with measured distance values:
```bash
d
```

- d: VL53L0X readings
- Consistent sampling rate recommended (default Arduino code: about 50 Hz)

---

## 📟 Arduino Data Logger

The repository includes an Arduino sketch (VL53L0X_Continuous.ino) to acquire data:
- Configurable sampling frequency by means of budget time (see sensor libraries)
- I2C communication (Wire.h)
- Data-ready timer based interruption
- UART output:
```bash
d

```

👉 Install the included **VL53L0X Arduino library** by copying the folder to your Arduino libraries/ directory.

### 👏 Acknowledgements

This Arduino library for sensor comunnication is based on the excellent open-source library provided by [**pololu**](https://github.com/pololu/vl53l0x-arduino).

---

## 🔮 Future Work

* Compare **Allan deviation vs Kalman ML identification** methods
* Provide **real-time tools** for UAV baro-sensor integration

---

## 🤝 Contributing

Contributions are welcome!
Fork, improve, and open a pull request 🚀

(Also check out our other related projects: [ImuCalibration](https://github.com/tomisuarez2/ImuCalibration), [MagnetometerCalibration](https://github.com/tomisuarez2/MagnetometerCalibration) and [BarometricAltimeterCalibration](https://github.com/tomisuarez2/BarometricAltimeterCalibration))


---

## 🛰️ Contact

If you have questions or want to collaborate, feel free to reach out:
**Tomás Suárez**
Mechatronics Engineering Student
📧 [suareztomasm@gmail.com](mailto:suareztomasm@gmail.com)

