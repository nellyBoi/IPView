"""
File to import auto-formatted *base.py file.
"""
import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from applicationdata import ApplicationData
from ipview_ui_base import Ui_MainWindow  # importing our generated file


########################################################################################################################
class IPViewWindow(Ui_MainWindow): # QtWidgets.QMainWindow

    ####################################################################################################################
    def __init__(self):

        # import member modules. Must be done inside __init__ to avoid circular imports
        import signals_and_slots

        super(IPViewWindow, self).__init__()

        app = QtWidgets.QApplication(sys.argv)
        app.processEvents()

        # instantiate events that holds and handles non-ui related data
        self.events = ApplicationData()

        main_window = QtWidgets.QMainWindow()
        # main_window.setWindowTitle("IPView")

        # set color of main window background
        main_window.setAutoFillBackground(True)
        p = main_window.palette()
        p.setColor(main_window.backgroundRole(), Qt.black)
        main_window.setPalette(p)

        self.setupUi(main_window)

        # modify text directory input box
        self.__modify_directory_input()

        # connect all signals and slots
        self.__signal_and_slot_connections = signals_and_slots.Connections(self)

        main_window.show()
        sys.exit(app.exec_())

    ####################################################################################################################
    def __modify_directory_input(self) -> None:
        """
        """
        self.directory_input.setText(r"C:\Nelly\IPView\image_containers\data\images")
        self.directory_input.setFont(QtGui.QFont('SansSerif', 12))
        self.directory_input.setStyleSheet("color: rgb(28, 43, 255);")  # change text color






