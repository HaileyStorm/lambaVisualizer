from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from core.image_logic import ImageLogic
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Binary Lambda Calculus Visualizer")
        self.setGeometry(100, 100, 600, 400)

        self.image_logic = ImageLogic()
        self.init_ui()
        self.update_images()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.image_labels = [QLabel(), QLabel()]
        image_layout = QHBoxLayout()
        for label in self.image_labels:
            label.setFixedSize(256, 256)
            label.mousePressEvent = lambda event, index=self.image_labels.index(label): self.on_image_click(index)
            image_layout.addWidget(label)

        main_layout.addLayout(image_layout)

    def update_images(self):
        for i, image in enumerate(self.image_logic.images):
            if image is not None and isinstance(image, np.ndarray) and image.shape[2] == 3:
                height, width, channel = image.shape
                bytes_per_line = 3 * width

                # Convert numpy array to bytes
                image_bytes = image.astype(np.uint8).tobytes()

                q_image = QImage(image_bytes, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                scaled_pixmap = pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                self.image_labels[i].setPixmap(scaled_pixmap)
            else:
                self.image_labels[i].setText("Invalid Image")

    def on_image_click(self, index):
        self.image_logic.select_image(index)
        self.update_images()