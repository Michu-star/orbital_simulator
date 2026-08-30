import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from plotting import draw_scene


class MainWindow(QMainWindow):
    def __init__(self, simulation, solution):
        super().__init__()
        self.setWindowTitle("Orbital Simulator")
        self.setGeometry(0, 0, 800, 600)

        self.sim = simulation
        self.sol = solution
        self.frame = 0
        self.first_draw = True

        self.view_mode = "solar_system"

        self.create_plot()
        self.create_controls()
        self.create_layout()

        self.update_plot()

    def create_plot(self):
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.subplots()

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
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

        self.ax.clear()

        draw_scene(self.ax, self.sol, self.frame, self.view_mode)

        if keep_zoom and not self.first_draw and self.view_mode == "solar_system":
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)

        self.ax.set_aspect('equal')
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

def draw_window(simulation, solution):
    app = QApplication(sys.argv)
    window = MainWindow(simulation, solution)
    window.show()
    sys.exit(app.exec())