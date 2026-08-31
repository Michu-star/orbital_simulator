import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from plotting import *


class MainWindow(QMainWindow):
    def __init__(self, simulation, solution, t, rel_energy_err, momentum, x, rel_angular_momentum_err):
        super().__init__()
        self.setWindowTitle("Orbital Simulator")
        self.setGeometry(0, 0, 800, 600)

        self.sim = simulation
        self.sol = solution

        self.t = t
        self.rel_energy_err = rel_energy_err
        self.momentum = momentum
        self.x = x
        self.rel_ang_momentum_err = rel_angular_momentum_err

        self.frame = 0
        self.first_draw = True

        self.view_mode = "solar_system"

        self.create_plot()
        self.create_controls()
        self.create_layout()

        self.update_plot()

    def create_plot(self):
        self.figure = Figure()

        gs = self.figure.add_gridspec(
            3, 2,
            width_ratios=[2, 1]
        )

        self.ax_orbit = self.figure.add_subplot(gs[:, 0])
        self.ax_energy = self.figure.add_subplot(gs[0, 1])
        self.ax_momentum = self.figure.add_subplot(gs[1, 1])
        self.ax_ang_momentum = self.figure.add_subplot(gs[2, 1])

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

    def create_controls(self):
        self.time_slider = QSlider(Qt.Orientation.Horizontal)

        self.time_slider.setRange(0, len(self.sol) - 1)
        self.time_slider.setSingleStep(1)

        self.time_slider.setValue(0)

        self.time_slider.valueChanged.connect(
            self.frame_changed
        )

        self.view_button = QPushButton("Earth–Moon view")
        self.view_button.clicked.connect(self.toggle_view)

    def create_layout(self):
        central_widget = QWidget()

        layout = QVBoxLayout()
        controls_layout = QHBoxLayout()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        controls_layout.addWidget(self.time_slider)
        controls_layout.addWidget(self.view_button)
        layout.addLayout(controls_layout)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def update_plot(self, keep_zoom=True):
        if keep_zoom and not self.first_draw and self.view_mode == "solar_system":
            xlim = self.ax_orbit.get_xlim()
            ylim = self.ax_orbit.get_ylim()

        draw_scene(self.ax_orbit, self.sol, self.frame, self.view_mode)
        draw_energy_plot(self.ax_energy, self.t, self.rel_energy_err, self.frame)
        draw_momentum_plot(self.ax_momentum, self.t, self.momentum, self.x, self.frame)
        draw_ang_momentum_plot(self.ax_ang_momentum, self.t, self.rel_ang_momentum_err, self.frame)

        if keep_zoom and not self.first_draw and self.view_mode == "solar_system":
            self.ax_orbit.set_xlim(xlim)
            self.ax_orbit.set_ylim(ylim)

        self.canvas.draw()
        self.first_draw = False

    def frame_changed(self):
        self.frame = self.time_slider.value()
        self.update_plot()

    def toggle_view(self):
        if self.view_mode == "solar_system":
            self.view_mode = "earth_moon"
            self.view_button.setText("Solar system view")
        else:
            self.view_mode = "solar_system"
            self.view_button.setText("Earth Moon view")

        self.update_plot(keep_zoom=False)

def draw_window(simulation, solution, t, energy, momentum, x, angular_momentum):
    app = QApplication(sys.argv)
    window = MainWindow(simulation, solution, t, energy, momentum, x, angular_momentum)
    window.show()
    sys.exit(app.exec())