
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QApplication, QGridLayout


class Window(QMainWindow):
    """
    Simple application window to render the environment into
    """

    def __init__(self):
        super().__init__()
        # Image label to display the rendering
        self.imgLabel = QLabel()

        # Create a main widget for the window
        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)

        layout = QGridLayout(mainWidget)
        layout.addWidget(self.imgLabel)

        # Show the application window
#        self.show()
        self.setFocus()

"""
rgb_array = 'im.png'    # my image
height, width, _ = rgb_array.shape
bytes_per_line = 3 * width
qt_img = QImage(rgb_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
pixmap = QPixmap.fromImage(qt_img)
window = Window()
window.setPixmap(pixmap)
"""

if __name__ == '__main__':
    import sys

    our_image = QImage()
    our_image.load(r'C:\Nelly\IPView\image_containers\data\images\bunny.jpg')

    app = QApplication(sys.argv)

    w = Window()
    w.imgLabel.setPixmap(QPixmap.fromImage(our_image))

    w.show()
    sys.exit(app.exec_())