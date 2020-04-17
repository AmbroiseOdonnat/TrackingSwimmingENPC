from pathlib import Path
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QTextEdit, QGridLayout, QMainWindow
from PyQt5.QtGui import QPainter, QPixmap, QImage, QWindow
from PyQt5.QtWidgets import QMessageBox, QLayout, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
import cv2
from src.utils.point_selection.information_points.information_points import InformationPoints
from src.utils.point_selection.image_selection.image_selection import ImageSelection


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(True)

    """def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space:
            super().close()
            self.close()"""


def array_to_qpixmap(image):
    height, width, channel = image.shape
    bytes_per_line = 3 * width

    # If the format is not good : put Format_RGB888
    qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888)

    return QPixmap.fromImage(qimage)


def perspective_selection(image):
    # Set the points
    points_image = []
    colors = [Qt.black, Qt.red, Qt.darkYellow, Qt.darkGray]
    points_real = np.zeros((len(colors), 2))

    # Set application, window and layout
    app = QApplication([])
    window = MainWidget()
    layout = QHBoxLayout()

    # Get the sizes
    screen_size = QDesktopWidget().screenGeometry()
    screen_ration = 4 / 5
    image_size = QSize(screen_size.width() * screen_ration - 115, screen_size.height() - 150)
    point_size = QSize(screen_size.width() * (1 - screen_ration) - 115, screen_size.height() - 150)

    # Set the image selection and the editable text
    pix_map = array_to_qpixmap(image)
    image_selection = ImageSelection(pix_map, image_size, points_image, colors)
    information_points = InformationPoints(point_size, colors, points_real)

    # Add widgets to layout
    layout.addWidget(image_selection)
    layout.addLayout(information_points)

    # Add layout to window and show the window
    window.setLayout(layout)
    window.showMaximized()
    app.exec_()

    print("Points image", points_image)
    print("Points real", points_real)


if __name__ == "__main__":
    # Get the array
    ROOT_IMAGE = Path('../../../data/images/raw_images/vid0_frame126.jpg')
    IMAGE = cv2.imread(str(ROOT_IMAGE))

    # Select the points
    perspective_selection(IMAGE)
