import sys
import numpy as np
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel, QRadioButton, \
    QButtonGroup, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class BeamformingVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("BeamForming.ui", self)
        self.setWindowTitle("Beamforming Visualizer")
        self.setWindowIcon(QIcon("Deliverables/wifi-signal.png"))
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


        # central_widget = QWidget()
        mode_layout = self.findChild(QHBoxLayout, "mode_layout")
        # central_widget.setLayout(layout)
        # self.setCentralWidget(central_widget)

        # visulization
        self.beamforming_layout = self.findChild(QVBoxLayout, "beamforming_layout")
        self.beamprofile_layout = self.findChild(QVBoxLayout, "beamProfile_layout")
        self.beamprofile_widget = self.findChild(QWidget, "beamforming_map_2")
        self.beamforming_widget = self.findChild(QWidget, "widget")

        self.beamprofile_layout.removeWidget(self.beamprofile_widget)
        self.beamforming_layout.removeWidget(self.beamforming_widget)
        self.beamprofile_widget.deleteLater()
        self.beamforming_widget.deleteLater()



        self.beamprofile_figure = Figure()
        self.beamforming_figure = Figure()
        self.beamforming_canvas = FigureCanvas(self.beamforming_figure)
        self.beamforming_layout.addWidget(self.beamforming_canvas)
        self.beamprofile_canvas = FigureCanvas(self.beamprofile_figure)
        self.beamprofile_layout.addWidget(self.beamprofile_canvas)


        self.create_mode_selection(mode_layout)

        # sliders
        self.antenna_slider = self.findChild(QSlider, "Transmitter_slider")
        self.antenna_label = self.findChild(QLabel, "transmitter_label")
        self.antenna_slider.setMinimum(1)
        self.antenna_slider.setMaximum(129)
        self.antenna_slider.setSingleStep(2)
        self.antenna_slider.setValue(self.num_antennas)
        self.antenna_label.setText(str(self.num_antennas))
        self.antenna_slider.valueChanged.connect(lambda value: self.update_num_antennas(self.antenna_label, value))
        self.beam_slider = self.findChild(QSlider, "shift_slider")
        self.beam_label = self.findChild(QLabel, "shift_label")
        self.beam_slider.setMinimum(-90)
        self.beam_slider.setMaximum(90)
        self.beam_slider.setValue(self.beam_direction)
        self.beam_label.setText(str(self.beam_direction))
        self.beam_slider.valueChanged.connect(lambda value: self.update_beam_direction(self.beam_label, value))

        self.frequency_slider = self.findChild(QSlider, "frequency_slider")
        self.frequency_label = self.findChild(QLabel, "frequency_label")
        self.frequency_unit = self.findChild(QLabel, "frequency_unit")
        self.frequency_slider.setMinimum(3)  # Representing 3e8 / 10
        self.frequency_slider.setMaximum(10)  # Representing 4e8 / 10
        self.frequency_slider.setValue(3)
        self.frequency_label.setText("0.3")
        self.frequency_slider.valueChanged.connect(lambda value: self.update_frequency(self.frequency_label, value))

        self.spacing_slider = self.findChild(QSlider, "roc_slider")
        self.spacing_label = self.findChild(QLabel, "roc_label")
        self.spacing_type = self.findChild(QLabel, "label_of_roc")
        scale_factor = 10
        self.spacing_slider.setMinimum(int(0.5 * scale_factor))
        self.spacing_slider.setMaximum(int(2.0 * scale_factor))
        self.spacing_slider.setValue(int((self.spacing / self.wavelength) * scale_factor))
        self.spacing_label.setText(str((self.spacing / self.wavelength)))
        self.spacing_slider.valueChanged.connect(lambda value: self.update_spacing(self.spacing_label, value / scale_factor))

        self.layout_selector = self.findChild(QComboBox, "arraygeometry")
        self.layout_selector.addItems(["Linear", "Curved"])
        self.layout_selector.currentTextChanged.connect(self.update_layout)

        self.update_visualization()

    def create_mode_selection(self, layout):
        self.mode_group = QButtonGroup()
        transmitting_button = self.findChild(QRadioButton, "transmitter_radioButton")
        transmitting_button.setChecked(True)
        receiving_button = self.findChild(QRadioButton, "reciever_radioButton")
        self.mode_group.addButton(transmitting_button)
        self.mode_group.addButton(receiving_button)

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



    def update_num_antennas(self, label, value):
        self.num_antennas = value
        label.setText(f" {value}")
        self.update_visualization()

    def update_beam_direction(self, label, value):
        self.beam_direction = value
        label.setText(f" {value}")
        self.update_visualization()

    def update_frequency(self, label, frequency_value):

        self.frequency = frequency_value * 1e8
        self.wavelength = self.speed_of_light / self.frequency
        self.spacing = self.spacing_slider.value() / 10 * self.wavelength
        label.setText(f" {self.frequency / 1e9}")
        self.update_visualization()

    def update_spacing(self, label, spacing_ratio):

        self.spacing = spacing_ratio * self.wavelength
        label.setText(f" {spacing_ratio}")
        self.update_visualization()

    def update_curvature(self, label, value):
        self.curvature = value
        label.setText(f"{value}")
        self.update_visualization()

    def update_layout(self, layout_type):
        """Update the layout type."""
        self.antenna_layout = layout_type

        if self.antenna_layout == "Linear":
            scale_factor = 10
            self.spacing_type.setText("Distance:")
            self.spacing_slider.setMinimum(int(0.5 * scale_factor))
            self.spacing_slider.setMaximum(int(2.0 * scale_factor))
            self.spacing_slider.setValue(int((self.spacing / self.wavelength) * scale_factor))
            self.spacing_slider.valueChanged.connect(
                lambda value: self.update_spacing(self.spacing_label, value / scale_factor))
            self.spacing_label.setText("0.5")
        else:
            self.spacing_type.setText("Radius:")

            self.spacing_slider.setMinimum(0)
            self.spacing_slider.setMaximum(100)
            self.spacing_slider.setValue(1)
            self.spacing_slider.valueChanged.connect(lambda value: self.update_curvature(self.spacing_label, value))
            self.spacing_label.setText(str(self.curvature))
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
        self.beamforming_figure.clear()
        self.beamprofile_figure.clear()
        ax1 = self.beamprofile_figure.add_subplot(polar=True)
        ax2 = self.beamforming_figure.add_subplot()

        if self.mode == "Transmitting":
            self.plot_beam_profile(ax1)
            self.plot_interference_map(ax2)
        else:
            self.plot_beam_profile(ax1)
            self.plot_receiving(ax2) # this is the field map

        self.beamforming_canvas.draw()
        self.beamprofile_canvas.draw()

    def plot_beam_profile(self, ax):
        d = self.spacing
        k = 2 * np.pi / self.wavelength  # Number of waves
        steering_delay = -k * d * np.sin(np.radians(self.beam_direction))

        # Calculating the array factor
        theta_rad = np.radians(self.theta)
        array_factor = np.abs(np.sum(
            [np.exp(1j * (n - 1) * (k * d * np.sin(theta_rad) + steering_delay)) for n in
             range(1, self.num_antennas + 1)],
            axis=0
        ))

        array_factor_db = 20 * np.log10(array_factor / np.max(array_factor))
        label = "Array Factor (Transmitting)" if self.mode == "Transmitting" else "Array Factor (Receiving)"

        # Set light theme for the plot
        ax.set_facecolor("#FFFFFF")  # White background for axes
        self.beamprofile_figure.patch.set_facecolor("#FFFFFF")  # Match figure background
        ax.tick_params(colors="black")  # Black tick labels
        ax.spines[:].set_color("black")  # Black spines

        # Plot the array factor
        ax.plot(np.radians(self.theta), array_factor_db, label=label, color="blue", linewidth=1.5)

        # Add legend with adjusted colors
        legend = ax.legend(loc='upper right', facecolor="#EEEEEE", edgecolor="black")
        for text in legend.get_texts():
            text.set_color("black")

    def plot_interference_map(self, ax):
        # Generate grid for interference map
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)

        # Calculate transmitter positions
        transmitter_positions = self.generate_antenna_positions(self.num_antennas, self.curvature, self.antenna_layout)

        k = 2 * np.pi / self.wavelength
        steering_delay = -k * self.spacing * np.sin(np.radians(self.beam_direction))

        field_map = np.zeros_like(X, dtype=complex)

        for idx, pos in enumerate(transmitter_positions):
            # Calculate distances from mesh to transmitter
            distances = np.sqrt((X - pos[0]) ** 2 + (Y - pos[1]) ** 2)
            distances[distances == 0] = 1e-6  # Avoid division by zero

            phase_shift = idx * steering_delay
            field_map += np.exp(1j * (k * distances + phase_shift))

        interference_map = np.abs(field_map) ** 2
        interference_map /= np.max(interference_map)  # Normalize

        # Set light theme
        ax.set_facecolor("#FFFFFF")  # White background for axes
        self.beamforming_figure.patch.set_facecolor("#FFFFFF")  # Match figure background
        ax.tick_params(colors="black")  # Black tick labels
        ax.spines[:].set_color("black")  # Black spines

        # Plot the interference map
        im = ax.imshow(interference_map, extent=[-10, 10, -10, 10], origin="lower",
                       cmap="hot", aspect="auto")

        # Add colorbar with adjusted style
        cbar = self.beamforming_figure.colorbar(im, ax=ax)
        cbar.ax.yaxis.set_tick_params(color="black")
        cbar.outline.set_edgecolor("black")
        cbar.set_label("Interference Intensity", color="black")

        # Set axis labels
        ax.set_xlabel("x (meters)", color="black")
        ax.set_ylabel("y (meters)", color="black")

        # Plot transmitter positions
        ax.scatter(transmitter_positions[:, 0], transmitter_positions[:, 1],
                   c='blue', marker='o', label="Transmitters")  # Use blue for transmitters in light mode

        # Add legend with adjusted text color
        legend = ax.legend(facecolor="#EEEEEE", edgecolor="black")
        for text in legend.get_texts():
            text.set_color("black")

    def plot_receiving(self, ax):

        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)

        ax.set_facecolor("#222222")  # Dark gray background for axes
        self.beamforming_figure.patch.set_facecolor("#222222")  # Match figure background
        ax.tick_params(colors="white")  # White tick labels
        ax.spines[:].set_color("white")  # White spines
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
        cbar = self.beamforming_figure.colorbar(im, ax=ax)
        cbar.set_label("Field Intensity", color = "white")
        cbar.ax.yaxis.set_tick_params(color="white")
        cbar.outline.set_edgecolor("white")

        # vis for transmitter as point
        ax.scatter(transmitter_position[0], transmitter_position[1], color="blue", label="Transmitter", s=100,
                   marker="o")
        # vis for receivers as x
        for receiver in receiver_positions:
            ax.scatter(receiver[0], receiver[1], color="black",
                       label="Receiver" if receiver is receiver_positions[0] else "", s=100, marker="x")
        ax.set_xlabel("x (meters)", color="white")
        ax.set_ylabel("y (meters)", color="white")

        ax.legend()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    visualizer = BeamformingVisualizer()
    visualizer.show()
    sys.exit(app.exec_())
