"""
File to run the ui.
"""
import sys
from ipview_ui import MyWindow
from PyQt5 import QtWidgets


########################################################################################################################
class IPViewer:
    """

    """

    ####################################################################################################################
    def __init__(self):
        """

        """
        self.app = QtWidgets.QApplication([])
        self.application = MyWindow()

    ####################################################################################################################
    def launch(self) -> None:
        """
        :return: None
        """
        self.application.show()
        try:
            sys.exit(self.app.exec())
        except:
            print('Exiting')

        return


########################################################################################################################
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)




########################################################################################################################
if __name__ == '__main__':
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

    viewer = IPViewer()
    viewer.launch()

