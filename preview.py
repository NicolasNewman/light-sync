import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QHBoxLayout, QVBoxLayout, QSizePolicy, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QSize, QRect
from PyQt5.QtGui import QImage, QPixmap
import cv2
import threading
import numpy

# Subclass QMainWindow to customise your application's main window

visualizer = None
thread = None


def convert_image(image, out_w, out_h):
    format = QImage.Format_RGBA8888 if image.shape[2] == 4 else QImage.Format_RGB888
    h, w, ch = image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QImage(image.data, w, h, bytes_per_line, format)
    p = convert_to_qt_format.scaled(out_w, out_h)
    return QPixmap.fromImage(p)


class Visualizer(QMainWindow):
    width = 640
    height = 360
    
    
    def __init__(self, *args, **kwargs):
        super(Visualizer, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")
        self.resize(self.width, self.height + self.height / 2)
        self.setMinimumSize(QSize(self.width, self.height + self.height / 2))
        self.setMaximumSize(QSize(self.width, self.height + self.height / 2))
        self.centralwidget = QWidget(self)
        self.centralwidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(self.width, self.height + self.height / 2))
        self.centralwidget.setMaximumSize(QSize(self.width, self.height + self.height / 2))
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QWidget(self.centralwidget)
        # self.widget.setGeometry(QRect(0, 0, 324, 274))
        self.widget.setObjectName("widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mask = QLabel(self.widget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mask.sizePolicy().hasHeightForWidth())
        self.mask.setSizePolicy(sizePolicy)
        self.mask.setMinimumSize(QSize(self.width / 2, self.height / 2))
        self.mask.setMaximumSize(QSize(self.width / 2, self.height / 2))
        self.mask.setObjectName("mask")
        self.horizontalLayout.addWidget(self.mask)
        self.shrink = QLabel(self.widget)
        self.shrink.setMinimumSize(QSize(self.width / 2, self.height / 2))
        self.shrink.setMaximumSize(QSize(self.width / 2, self.height / 2))
        self.shrink.setObjectName("shrink")
        self.horizontalLayout.addWidget(self.shrink)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.palette = QLabel(self.widget)
        self.palette.setMinimumSize(QSize(self.width, self.height))
        self.palette.setMaximumSize(QSize(self.width, self.height))
        self.palette.setObjectName("palette")
        self.verticalLayout.addWidget(self.palette)
        self.setCentralWidget(self.centralwidget)

    def update_palette(self, image):
        self.palette.setPixmap(convert_image(image, self.width, self.height))

    def update_shrink(self, image):
        self.shrink.setPixmap(convert_image(image, self.width / 2, self.height / 2))

    def update_mask(self, image):
        self.mask.setPixmap(convert_image(image, self.width / 2, self.height / 2))


def run_gui():
    global visualizer
    app = QApplication(sys.argv)

    visualizer = Visualizer()
    visualizer.show()

    app.exec_()


def start_visualizer():
    global thread
    thread = threading.Thread(target=run_gui)
    thread.start()


def update_visualizer_palette(image):
    global visualizer, thread
    if visualizer is not None and thread is not None:
        if thread.is_alive():
            visualizer.update_palette(image)
    return None


def update_visualizer_shrink(image):
    global visualizer, thread
    if visualizer is not None and thread is not None:
        if thread.is_alive():
            visualizer.update_shrink(image)
    return None


def update_visualizer_mask(image):
    global visualizer, thread
    if visualizer is not None and thread is not None:
        if thread.is_alive():
            visualizer.update_mask(image)
    return None


if __name__ == "__main__":
    start_visualizer()
