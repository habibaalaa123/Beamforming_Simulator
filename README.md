# 2D Beamforming Simulator 🎯

This **2D Beamforming Simulator** is an interactive tool designed to visualize the principles of beamforming, including **constructive and destructive interference**. It simulates real-world scenarios using configurable parameters such as delays, phase shifts, and array geometry, making it ideal for learning, research, and development in applications like **5G communications**, **ultrasound imaging**, and **tumor ablation**.

---

## Features 🛠️

1. **Interactive Parameter Customization:**
   - Adjust system parameters in real time:
      - Number of transmitters/receivers.
      - Applied delays or phase shifts.
      - Operating frequencies and their values.

   - Configure the geometry of the phased array:
     - Linear or Curved layouts.
     - Adjustable curvature parameters.

2. **Parameter Control:**
   - Adjust:
     - Number of antennas/transceivers.
     - Frequencies and delays/phase shifts.
     - Array geometry (linear or curved).
   - Dynamically steer the beam direction.

3. **Scenario Support:**
   - Preloaded configurations for:
     - **5G Beamforming.**
     - **Medical Ultrasound.**
     - **Focused Energy Tumor Ablation.**

4. **Custom Array Layouts:**
   - Supports both **linear** and **curved arrays** with adjustable curvature.

5. **Multi-Array Systems:**
   - Add multiple phased array units with independent configurations.

---

## System Requirements

- Python 3.7 or higher.
- Libraries:
  - `numpy`
  - `matplotlib`
  - `PyQt5`

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/2D-Beamforming-Simulator.git
   cd 2D-Beamforming-Simulator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the simulator:
   ```bash
   python main.py
   ```

---

## How to Use

### GUI Overview

- **Control Panel:**
  - Adjust the number of antennas, frequency, spacing, and beam direction.
- **Array Layout:**
  - Select between linear and curved geometries.
- **Visualization Windows:**
  - View beamforming patterns and interference maps in real time.

### Steps to Run:
1. Launch the application using the `main.py` script.
2. Configure parameters using sliders and input fields.
3. Choose a scenario or customize parameters manually.
4. Visualize results and save configurations as needed.

---

## Example Scenarios

### 1. **5G Beamforming**
   - Simulates high-frequency operation with a linear array for cellular networks.

### 2. **Medical Ultrasound**
   - Uses a curved array to focus sound waves for precise imaging.

### 3. **Tumor Ablation**
   - Demonstrates focused energy delivery using multi-array configurations.

---

## File Structure

```
2D-Beamforming-Simulator/
├── main.py             # Entry point of the simulator
├── beamforming.py      # Core beamforming computations
├── utils.py            # Utility functions for visualization and math
├── scenarios/          # Predefined configuration files
├── data/               # Sample data for testing
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation
```

---

## Screenshots

### Beamforming Interference Map
![Beamforming Map](path/to/interference_map.png)

### Beam Profile Visualization
![Beam Profile](path/to/beam_profile.png)

---

## Future Enhancements

- Add support for **3D phased array visualization**.
- Include more preconfigured scenarios (e.g., radar, sonar).
- Implement optimization algorithms for automatic beam steering.

---


