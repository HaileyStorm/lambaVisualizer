from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QSlider, QLineEdit, QSpinBox, QPushButton)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer
from core.blc_interpreter import interpret_blc
from core.blc_to_lambda import blc_to_lambda
from core.image_generator import generate_image
from utils.binary_utils import binary_to_decimal, decimal_to_binary

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Binary Lambda Calculus Visualizer")
        self.setGeometry(100, 100, 800, 600)

        self.binary_value = "10110011010"
        self.decimal_value = 1434
        self.binary_digits = 11
        self.z_value = 128

        self.init_ui()
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_visualization)
        self.update_timer.start(100)  # Update every 100ms

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Value slider
        value_layout = QHBoxLayout()
        value_layout.addWidget(QLabel("Adjust value:"))
        self.value_slider = QSlider(Qt.Orientation.Horizontal)
        self.value_slider.setRange(0, 2**self.binary_digits - 1)
        self.value_slider.setValue(self.decimal_value)
        self.value_slider.valueChanged.connect(self.on_value_slider_change)
        value_layout.addWidget(self.value_slider)
        layout.addLayout(value_layout)

        # Binary and Decimal inputs
        input_layout = QHBoxLayout()
        self.binary_input = QLineEdit(self.binary_value)
        self.binary_input.textChanged.connect(self.on_binary_input_change)
        input_layout.addWidget(self.binary_input)
        self.decimal_input = QLineEdit(str(self.decimal_value))
        self.decimal_input.textChanged.connect(self.on_decimal_input_change)
        input_layout.addWidget(self.decimal_input)
        layout.addLayout(input_layout)

        # Binary digits input
        digits_layout = QHBoxLayout()
        digits_layout.addWidget(QLabel("Number of binary digits:"))
        self.digits_spinbox = QSpinBox()
        self.digits_spinbox.setRange(1, 1024)  # Increased max value
        self.digits_spinbox.setValue(self.binary_digits)
        self.digits_spinbox.valueChanged.connect(self.on_digits_change)
        digits_layout.addWidget(self.digits_spinbox)
        layout.addLayout(digits_layout)

        # Z value slider
        z_layout = QHBoxLayout()
        z_layout.addWidget(QLabel("Adjust z value:"))
        self.z_slider = QSlider(Qt.Orientation.Horizontal)
        self.z_slider.setRange(0, 255)
        self.z_slider.setValue(self.z_value)
        self.z_slider.valueChanged.connect(self.on_z_slider_change)
        z_layout.addWidget(self.z_slider)
        self.z_value_label = QLabel(f"z value: {self.z_value}")
        z_layout.addWidget(self.z_value_label)
        layout.addLayout(z_layout)

        # Lambda expression label
        self.lambda_label = QLabel()
        layout.addWidget(self.lambda_label)

        # Image display
        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        # Description
        description = QLabel("This image visualizes the Binary Lambda Calculus expression over a 256x256 grid. "
                             "The color of each pixel is determined by evaluating the BLC expression with x, y, and z as inputs.")
        description.setWordWrap(True)
        layout.addWidget(description)

    def update_visualization(self):
        image = generate_image(self.binary_value, self.z_value)
        qimage = QImage(image.data, 256, 256, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

        lambda_expr = blc_to_lambda(self.binary_value)
        self.lambda_label.setText(f"Lambda: {lambda_expr}")

    def on_value_slider_change(self, value):
        self.decimal_value = value
        self.binary_value = decimal_to_binary(value, self.binary_digits)
        self.binary_input.setText(self.binary_value)
        self.decimal_input.setText(str(self.decimal_value))

    def on_binary_input_change(self, text):
        binary = ''.join(c for c in text if c in '01')
        binary = binary[:self.binary_digits]
        self.binary_value = binary.zfill(self.binary_digits)
        self.decimal_value = binary_to_decimal(self.binary_value)
        self.binary_input.setText(self.binary_value)
        self.decimal_input.setText(str(self.decimal_value))
        self.value_slider.setValue(self.decimal_value)

    def on_decimal_input_change(self, text):
        try:
            value = int(text)
            max_value = 2**self.binary_digits - 1
            self.decimal_value = max(0, min(value, max_value))
            self.binary_value = decimal_to_binary(self.decimal_value, self.binary_digits)
            self.binary_input.setText(self.binary_value)
            self.decimal_input.setText(str(self.decimal_value))
            self.value_slider.setValue(self.decimal_value)
        except ValueError:
            pass

    def on_digits_change(self, value):
        self.binary_digits = value
        max_value = 2**self.binary_digits - 1
        self.value_slider.setRange(0, max_value)
        if self.decimal_value > max_value:
            self.decimal_value = max_value
        self.binary_value = decimal_to_binary(self.decimal_value, self.binary_digits)
        self.binary_input.setText(self.binary_value)
        self.decimal_input.setText(str(self.decimal_value))
        self.value_slider.setValue(self.decimal_value)

    def on_z_slider_change(self, value):
        self.z_value = value
        self.z_value_label.setText(f"z value: {self.z_value}")