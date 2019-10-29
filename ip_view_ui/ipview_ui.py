"""
File to import auto-formatted *base.py file.
"""
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene

from eventdata import EventData
from ipview_ui_base import Ui_MainWindow  # importing our generated file


########################################################################################################################
class MyWindow(QtWidgets.QMainWindow):

    ####################################################################################################################
    def __init__(self):

        # instantiate events that holds and handles non-ui related data
        self.events = EventData()

        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("IP View")

        # set color of main window background
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # modify text directory input box
        self.__modify_directory_input()

        # connecting signals to slop methods
        self.ui.directory_load_push.clicked.connect(self.load_directory_button_pushed)
        self.ui.clear_push_button.clicked.connect(self.clear_button_pushed)
        self.ui.next_button.clicked.connect(self.next_button_pushed)

    ####################################################################################################################
    def __display_image(self) -> None:
        """
        """
        x = self.ui.image_display.x()
        y = self.ui.image_display.y()
        w = self.ui.image_display.width()
        h = self.ui.image_display.height()
        scene = QGraphicsScene()

        im = self.events.get_next_image()
        if im is not None:

            im = im.scaled(w, h, Qt.KeepAspectRatio, Qt.FastTransformation)
            scene.addPixmap(QPixmap.fromImage(im))
            self.ui.image_display.setScene(scene)
            self.ui.image_display.show()

    ####################################################################################################################
    def __modify_directory_input(self) -> None:
        """
        """
        self.ui.directory_input.setText(r"C:\Nelly\IPView\image_containers\data\images")
        self.ui.directory_input.setFont(QtGui.QFont('SansSerif', 12))
        self.ui.directory_input.setStyleSheet("color: rgb(28, 43, 255);")  # change text color

    ####################################################################################################################
    def load_directory_button_pushed(self) -> None:
        """
        Slot method for loading directory upon load push button.
        """
        directory = self.ui.directory_input.toPlainText()
        files_for_display = self.events.load_directory(directory=directory)
        if len(files_for_display) == 0:
            self.ui.text_list_display.setText('No Compatible Images')
        else:
            string = '\n'.join(map(str, files_for_display))
            self.ui.text_list_display.setText(string)

        return

    ####################################################################################################################
    def next_button_pushed(self) -> None:
        """
        Slot method for a signal from the next push button.
        """
        self.__display_image()

    ####################################################################################################################
    def clear_button_pushed(self) -> None:
        """
        Slot method for clearing all data from the UI and from memory.
        """
        self.events.clear_data()
        self.ui.text_list_display.setText('')

        return


