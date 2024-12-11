import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel, QRadioButton, QButtonGroup, QComboBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class BeamformingVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beamforming Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        self.num_antennas = 3
        self.angle_resolution = 1
        self.frequency = 3e8
        self.speed_of_light = 3e8
        self.wavelength = self.speed_of_light / self.frequency
        self.spacing = self.wavelength / 2
        self.theta = np.linspace(0, 360, 360 // self.angle_resolution + 1)
        self.beam_direction = 0
        self.mode = "Transmitting"
        self.curvature = 1
        self.antenna_layout = "Linear"


        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # visulization
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)


        self.create_mode_selection(layout)

        # sliders
        self.antenna_slider = self.create_num_antennas_slider(layout)
        self.beam_slider = self.create_beam_direction_slider(layout)
        self.frequency_slider = self.create_frequency_slider(layout)
        self.spacing_slider = self.create_spacing_slider(layout)
        self.curvature_slider = self.create_curvature_slider(layout)
        self.layout_selector = self.create_layout_selector(layout)

        self.update_visualization()

    def create_mode_selection(self, layout):
        label = QLabel("Select Mode:")
        layout.addWidget(label)
        self.mode_group = QButtonGroup()
        transmitting_button = QRadioButton("Transmitting")
        transmitting_button.setChecked(True)
        receiving_button = QRadioButton("Receiving")
        self.mode_group.addButton(transmitting_button)
        self.mode_group.addButton(receiving_button)

        layout.addWidget(transmitting_button)
        layout.addWidget(receiving_button)
        transmitting_button.toggled.connect(lambda: self.update_mode("Transmitting"))
        receiving_button.toggled.connect(lambda: self.update_mode("Receiving"))

    def update_mode(self, mode):
        self.mode = mode
        self.reset_parameters()
        self.update_visualization()

    def reset_parameters(self):
        self.num_antennas = 3 if self.mode == "Transmitting" else 5
        self.beam_direction = 0
        self.frequency = 3e8
        self.wavelength = self.speed_of_light / self.frequency
        self.spacing = self.wavelength / 2
        self.curvature = 1
        self.antenna_slider.setValue(self.num_antennas)
        self.beam_slider.setValue(self.beam_direction)
        self.frequency_slider.setValue(3)
        self.spacing_slider.setValue(int((self.spacing / self.wavelength) * 10))
        self.curvature_slider.setValue(0)

    def create_num_antennas_slider(self, layout):
        label = QLabel(f"Number of Antennas: {self.num_antennas}")
        layout.addWidget(label)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(129)
        slider.setSingleStep(2)
        slider.setValue(self.num_antennas)
        slider.valueChanged.connect(lambda value: self.update_num_antennas(label, value))
        layout.addWidget(slider)
        return slider

    def create_beam_direction_slider(self, layout):
        label = QLabel(f"Beam Steering Angle (\u00b0): {self.beam_direction}")
        layout.addWidget(label)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(-90)
        slider.setMaximum(90)
        slider.setValue(self.beam_direction)
        slider.valueChanged.connect(lambda value: self.update_beam_direction(label, value))
        layout.addWidget(slider)
        return slider

    def create_frequency_slider(self, layout):
        label = QLabel(f"Frequency (Hz): {self.frequency:.2e}")
        layout.addWidget(label)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(3)  # Representing 3e8 / 10
        slider.setMaximum(10)  # Representing 4e8 / 10
        slider.setValue(3)
        slider.valueChanged.connect(lambda value: self.update_frequency(label, value))
        layout.addWidget(slider)
        return slider

    def create_spacing_slider(self, layout):

        label = QLabel(f"Antenna Spacing (\u03bb): {self.spacing / self.wavelength:.2f}")
        layout.addWidget(label)

        scale_factor = 10
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(int(0.5 * scale_factor))
        slider.setMaximum(int(2.0 * scale_factor))
        slider.setValue(int((self.spacing / self.wavelength) * scale_factor))
        slider.valueChanged.connect(lambda value: self.update_spacing(label, value / scale_factor))
        layout.addWidget(slider)
        return slider

    def create_curvature_slider(self, layout):

        label = QLabel(f"Curvature: {self.curvature}")
        layout.addWidget(label)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(self.curvature)
        slider.valueChanged.connect(lambda value: self.update_curvature(label, value))
        layout.addWidget(slider)
        return slider

    def create_layout_selector(self, layout):
        label = QLabel("Antenna Layout:")
        layout.addWidget(label)

        combo = QComboBox()
        combo.addItems(["Linear", "Curved"])
        combo.currentTextChanged.connect(self.update_layout)
        layout.addWidget(combo)
        return combo

    def update_num_antennas(self, label, value):
        self.num_antennas = value
        label.setText(f"Number of Antennas: {value}")
        self.update_visualization()

    def update_beam_direction(self, label, value):
        self.beam_direction = value
        label.setText(f"Beam Steering Angle (\u00b0): {value}")
        self.update_visualization()

    def update_frequency(self, label, frequency_value):

        self.frequency = frequency_value * 1e8
        self.wavelength = self.speed_of_light / self.frequency
        self.spacing = self.spacing_slider.value() / 10 * self.wavelength
        label.setText(f"Frequency (Hz): {self.frequency:.2e}")
        self.update_visualization()

    def update_spacing(self, label, spacing_ratio):

        self.spacing = spacing_ratio * self.wavelength
        label.setText(f"Antenna Spacing (\u03bb): {spacing_ratio:.2f}")
        self.update_visualization()

    def update_curvature(self, label, value):
        self.curvature = value
        label.setText(f"Curvature: {value}")
        self.update_visualization()

    def update_layout(self, layout_type):
        """Update the layout type."""
        self.antenna_layout = layout_type
        self.update_visualization()

    def generate_antenna_positions(self, num_antennas, curvature, layout_type='Linear'):
       # by default it's linear
        if layout_type == 'Linear':
            return  np.array([
             [n * self.spacing, 0] for n in range(-(self.num_antennas - 1) // 2, (self.num_antennas + 1) // 2)
         ])
        elif layout_type == 'Curved':
            angle_step = 2 * np.pi / num_antennas
            return np.array([
                [curvature * np.cos(n * angle_step), curvature * np.sin(n * angle_step)]
                for n in range(num_antennas)
            ])

    def update_visualization(self):
        self.figure.clear()
        ax1 = self.figure.add_subplot(121, polar=True)
        ax2 = self.figure.add_subplot(122)

        if self.mode == "Transmitting":
            self.plot_beam_profile(ax1)
            self.plot_interference_map(ax2)
        else:
            self.plot_beam_profile(ax1)
            self.plot_receiving(ax2) # this is the field map

        self.canvas.draw()

    def plot_beam_profile(self, ax):
        d = self.spacing
        k = 2 * np.pi / self.wavelength # num of waves
        steering_delay = -k * d * np.sin(np.radians(self.beam_direction))

       # caluculting the array factor
        theta_rad = np.radians(self.theta)
        array_factor = np.abs(np.sum(
            [np.exp(1j * (n - 1) * (k * d * np.sin(theta_rad) + steering_delay)) for n in
             range(1, self.num_antennas + 1)],
            axis=0
        ))

        array_factor_db = 20 * np.log10(array_factor / np.max(array_factor))
        label = "Array Factor (Transmitting)" if self.mode == "Transmitting" else "Array Factor (Receiving)"
        ax.plot(np.radians(self.theta), array_factor_db, label=label)
        ax.set_title("Beam Profile", va='bottom')
        ax.legend()

    def plot_interference_map(self, ax):
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)


        # transmitter_positions = np.array([
        #     [n * self.spacing, 0] for n in range(-(self.num_antennas - 1) // 2, (self.num_antennas + 1) // 2)
        # ])
        transmitter_positions = self.generate_antenna_positions(self.num_antennas, self.curvature, self.antenna_layout)

        k = 2 * np.pi / self.wavelength
        steering_delay = -k * self.spacing * np.sin(np.radians(self.beam_direction))


        field_map = np.zeros_like(X, dtype=complex)

        for idx, pos in enumerate(transmitter_positions):
            # calculate distances from mesh to trasnmitter
            distances = np.sqrt((X - pos[0]) ** 2 + (Y - pos[1]) ** 2)
            distances[distances == 0] = 1e-6  # Avoid division by zero

            phase_shift = idx * steering_delay
            field_map += np.exp(1j * (k * distances + phase_shift))

        interference_map = np.abs(field_map) ** 2
        interference_map /= np.max(interference_map)  # Normalize

        im = ax.imshow(interference_map, extent=[-10, 10, -10, 10], origin="lower", cmap="hot", aspect="auto")
        cbar = self.figure.colorbar(im, ax=ax)
        cbar.set_label("Interference Intensity")
        ax.set_title("Interference Map with Steering")
        ax.set_xlabel("x (meters)")
        ax.set_ylabel("y (meters)")

        ax.scatter(transmitter_positions[:, 0], transmitter_positions[:, 1], c='blue', marker='o', label="Transmitters")
        ax.legend()

    def plot_receiving(self, ax):

        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)

        # transmitter fixed at position
        transmitter_position = np.array([0, 10])

        # receiver_positions = np.array([
        #     [n * self.spacing, 0] for n in range(-(self.num_antennas - 1) // 2, (self.num_antennas + 1) // 2)
        # ])
        receiver_positions = self.generate_antenna_positions(self.num_antennas, self.curvature, self.antenna_layout)

        # wavenumber
        k = 2 * np.pi / self.wavelength

        distances_tx = np.sqrt((X - transmitter_position[0]) ** 2 + (Y - transmitter_position[1]) ** 2)
        distances_tx[distances_tx == 0] = 1e-6  # avoid division by zero
        field_map = np.cos(k * distances_tx)  # field strength at each point

        # normalize the field map
        field_map = np.abs(field_map)
        field_map /= np.max(field_map)


        im = ax.imshow(field_map, extent=[-10, 10, -10, 10], origin="lower", cmap="hot", aspect="auto")
        # color bar
        cbar = self.figure.colorbar(im, ax=ax)
        cbar.set_label("Field Intensity")
        # vis for transmitter as point
        ax.scatter(transmitter_position[0], transmitter_position[1], color="blue", label="Transmitter", s=100,
                   marker="o")
        # vis for receivers as x
        for receiver in receiver_positions:
            ax.scatter(receiver[0], receiver[1], color="black",
                       label="Receiver" if receiver is receiver_positions[0] else "", s=100, marker="x")
        ax.set_title("Receiving Mode Field Map")
        ax.set_xlabel("x (meters)")
        ax.set_ylabel("y (meters)")
        ax.legend()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    visualizer = BeamformingVisualizer()
    visualizer.show()
    sys.exit(app.exec_())
