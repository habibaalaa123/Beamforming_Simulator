# 2D Beamforming Simulator 🎯

This **2D Beamforming Simulator** is an interactive tool designed to visualize the principles of beamforming, including **constructive and destructive interference**. It simulates real-world scenarios using configurable parameters such as delays, phase shifts, and array geometry, making it ideal for learning, research, and development in applications like **5G communications**, **ultrasound imaging**, and **tumor ablation**.

---

## Features 🛠️

1. **Interactive Parameter Customization:**
   - Adjust system parameters in real time :
      - Number of transmitters/receivers.
      - Applied delays or phase shifts.
      - Operating frequencies and their values.

   - Configure the geometry of the phased array :
     - Linear or Curved layouts.
     - Adjustable curvature parameters.
   - Dynamically steer the beam direction.

2. **Visualization:**
   - View the constructive/destructive interference map.
   - Analyze the beam profile in synchronized viewers.

3. **Scenario Support:**
   - Includes three parameter configuration buttons inspired by real-world applications:
     - **5G Beamforming:** Simulates high-frequency operation with a linear array for cellular networks in Recieveing mode.
     - **Medical Ultrasound:** Uses a curved array to focus sound waves for precise imaging in Transmitting mode.
     - **Focused Energy Tumor Ablation:**:Demonstrates focused energy delivery using multi-array configurations in Transmitting mode.

4. **Custom Array Layouts:**
   - Supports both **linear** and **curved arrays** with adjustable curvature.

5. **Multi-Array Systems:**
   - Add multiple phased array units with independent configurations.

---
## Demo 📸
"https://raw.githubusercontent.com/habibaalaa123/Beamforming_Simulator/main/BeamForming_updtated
## System Requirements ⚙️

- Python 3.7 or higher.
- Libraries:
  - `numpy`
  - `matplotlib`
  - `PyQt5`

---


## Installation 📥

1. Clone this repository:
   ```bash
   git clone https://github.com/habibaalaa123/Beamforming_Simulator.git
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

## How to Use 🚀

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

## File Structure

```
2D-Beamforming-Simulator/
├── beamforming.py      # Core beamforming computations
├── BeamForming.ui      # ui viusalization 
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation
```

---



## Acknowledgments :
This project was supervised by Dr. Tamer Basha & Eng. Omar, who provided invaluable guidance and expertise throughout its development as a part of the Digital Signal Processing course at Cairo University Faculty of Engineering.



---

## Team Members
<div align="center">
  <table style="border-collapse: collapse; border: none;">
    <tr>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/e8713727-6257-4c16-b9bd-8f6cb509cf1c" alt="Enjy Ashraf" width="150" height="150"><br>
        <a href="https://github.com/enjyashraf18"><b>Enjy Ashraf</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/5de3e403-7fce-4000-95d2-e9f07e0d78cf" alt="Nada Khaled" width="150" height="150"><br>
        <a href="https://github.com/NadaKhaled157"><b>Nada Khaled</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/4b1f5180-2250-49ae-869f-4d00fb89447a" alt="Habiba Alaa" width="150" height="150"><br>
        <a href="https://github.com/habibaalaa123"><b>Habiba Alaa</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/567fd220-acc8-4094-bfe0-5939a0048ca9" alt="Shahd Ahmed" width="150" height="150"><br>
        <a href="https://github.com/Shahd-A-Mahmoud"><b>Shahd Ahmed</b></a>
      </td>
    </tr>
  </table>
</div>




---


