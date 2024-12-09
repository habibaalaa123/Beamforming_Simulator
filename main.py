import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QComboBox, QPushButton, QWidget
)
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class BeamformingSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Beamforming Simulator")
        self.setGeometry(100, 100, 1200, 800)

        # Layouts
        self.main_layout = QHBoxLayout()
        self.control_layout = QVBoxLayout()
        self.visualization_layout = QVBoxLayout()

        # Main widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout(central_widget)
        central_layout.addLayout(self.control_layout, 1)
        central_layout.addLayout(self.visualization_layout, 3)

        self.num_tx_label = QLabel("Number of Transmitters:")
        self.num_tx_spinbox = QSpinBox()
        self.num_tx_spinbox.setRange(1, 50)
        self.num_tx_spinbox.setValue(10)

        self.num_rx_label = QLabel("Number of Receivers:")
        self.num_rx_spinbox = QSpinBox()
        self.num_rx_spinbox.setRange(1, 50)
        self.num_rx_spinbox.setValue(10)

        self.geometry_label = QLabel("Array Geometry:")
        self.geometry_combobox = QComboBox()
        self.geometry_combobox.addItems(["Linear", "Curved"])

        self.curvature_label = QLabel("Curvature (for Curved Array):")
        self.curvature_spinbox = QSpinBox()
        self.curvature_spinbox.setRange(1, 100)
        self.curvature_spinbox.setValue(1)

        self.frequency_label = QLabel("Frequency (e8 Hz):")
        self.frequency_spinbox = QSpinBox()
        self.frequency_spinbox.setRange(int(1), int(10))
        self.frequency_spinbox.setSingleStep(int(1))
        self.frequency_spinbox.setValue(int(3))

 # start and end
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
# controls : num of tx and rx and freq and geometry and selected curve
        self.control_layout.addWidget(self.num_tx_label)
        self.control_layout.addWidget(self.num_tx_spinbox)
        self.control_layout.addWidget(self.num_rx_label)
        self.control_layout.addWidget(self.num_rx_spinbox)
        self.control_layout.addWidget(self.geometry_label)
        self.control_layout.addWidget(self.geometry_combobox)
        self.control_layout.addWidget(self.curvature_label)
        self.control_layout.addWidget(self.curvature_spinbox)
        self.control_layout.addWidget(self.frequency_label)
        self.control_layout.addWidget(self.frequency_spinbox)
        self.control_layout.addWidget(self.start_button)
        self.control_layout.addWidget(self.stop_button)

# beam map
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.visualization_layout.addWidget(self.canvas)
# beam profile , not done yet
        self.figure_profile, self.ax_profile = plt.subplots()
        self.canvas_profile = FigureCanvas(self.figure_profile)
        self.visualization_layout.addWidget(self.canvas_profile)


 # update each time step , we need to make if every signal is detected else
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visualization)

        # Signals
        self.start_button.clicked.connect(self.start_simulation)
        self.stop_button.clicked.connect(self.stop_simulation)

# phased array "geometry"
        self.array_geometry = None
        self.beam_map = None

    def start_simulation(self):
        self.timer.start(100)  # Update every 100ms
        self.generate_array_geometry()

    def stop_simulation(self):
        self.timer.stop()

    def generate_array_geometry(self):
        num_tx = self.num_tx_spinbox.value()
        geometry = self.geometry_combobox.currentText()
        curvature = self.curvature_spinbox.value()

        if geometry == "Linear":
            self.array_geometry = self.linear_array(num_tx, spacing=1)
        elif geometry == "Curved":
            self.array_geometry = self.curved_array(num_tx, radius=curvature)

    def linear_array(self, num_elements, spacing):
        # Elements along the x-axis
        return np.array([(0, -i * spacing) for i in range(num_elements)])
    # i want them to be in x axis
    # the position of linear transmitter

    def curved_array(self, num_elements, radius):
        angles = np.linspace(0, 2* np.pi , num_elements)
        return np.array([(radius * np.sin(angle), radius * np.cos(angle)) for angle in angles])
# the position of curved position
    def calculate_beam_map(self, array_geometry, frequency):
        (grid_x,grid_y) = np.meshgrid(np.linspace(-10, 10, 200), np.linspace(0, 10, 200))
        beam_map = np.zeros_like(grid_x)
        wavelength = 3e8 / (frequency* 10**8)

        for element in array_geometry:
            distance = np.sqrt((grid_x - element[0]) ** 2 + (grid_y - element[1]) ** 2)
            phase_shift = 2 * np.pi * distance / wavelength
            beam_map += np.cos(phase_shift)

        return beam_map

    def update_visualization(self):
        frequency = self.frequency_spinbox.value()

        if self.array_geometry is not None:

            self.beam_map = self.calculate_beam_map(self.array_geometry, frequency)


            self.ax.clear()

            # Plot the beam map
            self.ax.imshow(
                self.beam_map,
                extent=(-10, 10, -10, 10),
                origin="lower",
                cmap="hot",
            )
            self.ax.set_title("Beamforming Map")
            self.ax.set_xlabel("X-Axis")
            self.ax.set_ylabel("Y-Axis")


            # array_y = self.array_geometry[:, 0]  # X-coordinates of the array
            # array_x = self.array_geometry[:, 1]  # Y-coordinates of the array
            # self.ax.scatter(array_x, array_y, color='blue', label="Transmitters")
            # self.ax.legend()
            #
            # self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeamformingSimulator()
    window.show()
    sys.exit(app.exec_())
