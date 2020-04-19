from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QTextEdit, QGridLayout, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPainter, QPixmap, QImage, QWindow, QTextCursor
from PyQt5.QtWidgets import QMessageBox, QLayout
from PyQt5.QtCore import Qt, QPoint, QRect, QSize


class EditPoint(QTextEdit):
    def __init__(self, size, color, points, index_point, meter_or_line):
        super().__init__()
        self.setTabChangesFocus(True)
        self.setFixedSize(size)
        self.setTextColor(color)
        self.points = points
        self.index_point = index_point
        self.meter_or_line = meter_or_line

    def focusOutEvent(self, event):
        if self.toPlainText() != "":
            if self.toPlainText()[-1] == " ":
                self.textCursor().deletePreviousChar()
            if not self.toPlainText().isnumeric():
                while self.toPlainText() != "":
                    self.textCursor().deletePreviousChar()
            else:
                self.points[self.index_point, self.meter_or_line] = float(self.toPlainText())
                if self.meter_or_line == 1:
                    self.points[self.index_point, self.meter_or_line] *= 2.5
