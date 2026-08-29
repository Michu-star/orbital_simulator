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

    def create_layout(self):
        central_widget = QWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.time_slider)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def update_plot(self):
        self.ax.clear()

        draw_scene(self.ax, self.sol, self.frame)

        self.ax.set_aspect('equal')
        self.canvas.draw()

    def frame_changed(self):
        self.frame = self.time_slider.value()
        self.update_plot()

def draw_window(simulation, solution):
    app = QApplication(sys.argv)
    window = MainWindow(simulation, solution)
    window.show()
    sys.exit(app.exec())