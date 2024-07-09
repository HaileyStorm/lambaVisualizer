from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                             QSlider, QLineEdit, QSpinBox, QComboBox, QCheckBox)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer
from core.blc_interpreter import interpret_blc
from core.blc_to_lambda import blc_to_lambda
from core.image_generator import (generate_full_image, select_quadrant, flip_image,
                                  rotate_image, combine_images)
from utils.binary_utils import binary_to_decimal, decimal_to_binary

class LambdaControl(QWidget):
    def __init__(self, parent, initial_value, initial_z):
        super().__init__(parent)
        self.parent = parent
        self.decimal_value = initial_value
        self.z_value = initial_z
        self.quadrant = 0
        self.flip = False
        self.rotation = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Value slider and inputs
        value_layout = QHBoxLayout()
        self.value_slider = QSlider(Qt.Orientation.Horizontal)
        self.value_slider.setRange(0, 2**self.parent.binary_digits - 1)
        self.value_slider.setValue(self.decimal_value)
        self.value_slider.valueChanged.connect(self.on_value_change)
        value_layout.addWidget(self.value_slider)

        self.binary_input = QLineEdit(decimal_to_binary(self.decimal_value, self.parent.binary_digits))
        self.binary_input.textChanged.connect(self.on_binary_input_change)
        value_layout.addWidget(self.binary_input)

        self.decimal_input = QLineEdit(str(self.decimal_value))
        self.decimal_input.textChanged.connect(self.on_decimal_input_change)
        value_layout.addWidget(self.decimal_input)

        layout.addLayout(value_layout)

        # Z value slider
        z_layout = QHBoxLayout()
        z_layout.addWidget(QLabel("Z value:"))
        self.z_slider = QSlider(Qt.Orientation.Horizontal)
        self.z_slider.setRange(0, 255)
        self.z_slider.setValue(self.z_value)
        self.z_slider.valueChanged.connect(self.on_z_change)
        z_layout.addWidget(self.z_slider)
        layout.addLayout(z_layout)

        # Quadrant selection
        quadrant_layout = QHBoxLayout()
        quadrant_layout.addWidget(QLabel("Quadrant:"))
        self.quadrant_combo = QComboBox()
        self.quadrant_combo.addItems(["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"])
        self.quadrant_combo.currentIndexChanged.connect(self.on_quadrant_change)
        quadrant_layout.addWidget(self.quadrant_combo)
        layout.addLayout(quadrant_layout)

        # Flip and rotation controls
        transform_layout = QHBoxLayout()
        self.flip_check = QCheckBox("Flip")
        self.flip_check.stateChanged.connect(self.on_flip_change)
        transform_layout.addWidget(self.flip_check)

        self.rotation_combo = QComboBox()
        self.rotation_combo.addItems(["0°", "90°", "270°"])
        self.rotation_combo.currentIndexChanged.connect(self.on_rotation_change)
        transform_layout.addWidget(self.rotation_combo)
        layout.addLayout(transform_layout)

        # Image display
        self.image_label = QLabel()
        layout.addWidget(self.image_label)

    def on_value_change(self, value):
        self.decimal_value = value
        self.binary_input.setText(decimal_to_binary(value, self.parent.binary_digits))
        self.decimal_input.setText(str(value))
        self.parent.update_visualization()

    def on_binary_input_change(self, text):
        binary = ''.join(c for c in text if c in '01')
        binary = binary[:self.parent.binary_digits].zfill(self.parent.binary_digits)
        self.decimal_value = binary_to_decimal(binary)
        self.value_slider.setValue(self.decimal_value)
        self.decimal_input.setText(str(self.decimal_value))
        self.parent.update_visualization()

    def on_decimal_input_change(self, text):
        try:
            value = int(text)
            max_value = 2**self.parent.binary_digits - 1
            self.decimal_value = max(0, min(value, max_value))
            self.value_slider.setValue(self.decimal_value)
            self.binary_input.setText(decimal_to_binary(self.decimal_value, self.parent.binary_digits))
            self.parent.update_visualization()
        except ValueError:
            pass

    def on_z_change(self, value):
        self.z_value = value
        self.parent.update_visualization()

    def on_quadrant_change(self, index):
        self.quadrant = index
        self.parent.update_visualization()

    def on_flip_change(self, state):
        self.flip = state == Qt.CheckState.Checked
        self.parent.update_visualization()

    def on_rotation_change(self, index):
        self.rotation = index * 90
        self.parent.update_visualization()

    def update_image(self, image):
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Binary Lambda Calculus Visualizer")
        self.setGeometry(100, 100, 1200, 800)

        self.binary_digits = 11
        self.lambda_controls = []
        self.combination_ops = ['xor', 'xor', 'or']
        self.update_combined = False

        self.init_ui()
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_visualization)
        self.update_timer.start(100)  # Update every 100ms

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Global controls
        global_controls = QHBoxLayout()
        global_controls.addWidget(QLabel("Binary digits:"))
        self.digits_spinbox = QSpinBox()
        self.digits_spinbox.setRange(1, 53)
        self.digits_spinbox.setValue(self.binary_digits)
        self.digits_spinbox.valueChanged.connect(self.on_digits_change)
        global_controls.addWidget(self.digits_spinbox)
        main_layout.addLayout(global_controls)

        # Lambda controls
        lambda_layout = QHBoxLayout()
        for i, initial_value in enumerate([1434, 307, 1579, 742]):
            control = LambdaControl(self, initial_value, 128)
            lambda_layout.addWidget(control)
            self.lambda_controls.append(control)
        main_layout.addLayout(lambda_layout)

        # Combination controls
        combination_layout = QVBoxLayout()
        self.update_combined_check = QCheckBox("Update combined images")
        self.update_combined_check.stateChanged.connect(self.on_update_combined_change)
        combination_layout.addWidget(self.update_combined_check)

        for i, op in enumerate(self.combination_ops):
            op_layout = QHBoxLayout()
            op_layout.addWidget(QLabel(f"Operation {i+1}:"))
            op_combo = QComboBox()
            op_combo.addItems(['xor', 'or', 'and'])
            op_combo.setCurrentText(op)
            op_combo.currentTextChanged.connect(lambda text, index=i: self.on_op_change(index, text))
            op_layout.addWidget(op_combo)
            combination_layout.addLayout(op_layout)
        main_layout.addLayout(combination_layout)

        # Combined visualization area
        combined_layout = QHBoxLayout()
        self.intermediate_labels = [QLabel(), QLabel()]
        self.final_label = QLabel()
        for label in self.intermediate_labels + [self.final_label]:
            combined_layout.addWidget(label)
        main_layout.addLayout(combined_layout)

    def update_visualization(self):
        for control in self.lambda_controls:
            image = generate_full_image(decimal_to_binary(control.decimal_value, self.binary_digits), control.z_value)
            control.update_image(image)

        if self.update_combined:
            self.update_combined_images()

    def update_combined_images(self):
        images = []
        for control in self.lambda_controls:
            image = generate_full_image(decimal_to_binary(control.decimal_value, self.binary_digits), control.z_value)
            image = select_quadrant(image, control.quadrant)
            if control.flip:
                image = flip_image(image)
            image = rotate_image(image, control.rotation)
            images.append(image)

        intermediate1 = combine_images(images[:2], [self.combination_ops[0]])
        intermediate2 = combine_images(images[2:], [self.combination_ops[1]])
        final = combine_images([intermediate1, intermediate2], [self.combination_ops[2]])

        for i, img in enumerate([intermediate1, intermediate2, final]):
            qimage = QImage(img.data, img.shape[1], img.shape[0], QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            if i < 2:
                self.intermediate_labels[i].setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.final_label.setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio))

    def on_digits_change(self, value):
        self.binary_digits = value
        for control in self.lambda_controls:
            control.value_slider.setRange(0, 2**self.binary_digits - 1)
            if control.decimal_value >= 2**self.binary_digits:
                control.decimal_value = 2**self.binary_digits - 1
                control.value_slider.setValue(control.decimal_value)
        self.update_visualization()

    def on_op_change(self, index, operation):
        self.combination_ops[index] = operation
        if self.update_combined:
            self.update_combined_images()

    def on_update_combined_change(self, state):
        self.update_combined = state == Qt.CheckState.Checked
        if self.update_combined:
            self.update_combined_images()