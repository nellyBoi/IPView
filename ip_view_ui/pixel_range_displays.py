"""
Nelly Kane
12.16.2019
"""
from PyQt5.QtWidgets import QWidget
import PyQt5.QtCore as QtCore

import ipview_ui


########################################################################################################################
class MinimumPixelDisplay(QWidget):

    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        super(MinimumPixelDisplay, self).__init__()
        QWidget.__init__(self)

        self.ui = ui
        self.ui.min_pixel_display.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    ####################################################################################################################
    def set_text(self, value: str) -> None:
        """
        Method to add row of text to display window.
        :param value: int to be set in display window
        """
        self.clear_text()
        self.ui.min_pixel_display.setText(str(value))

        return

    ####################################################################################################################
    def clear_text(self) -> None:
        """
        Method to clear stream display.
        """
        self.ui.min_pixel_display.clear()

        return


########################################################################################################################
class MaximumPixelDisplay(QWidget):

    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        super(MaximumPixelDisplay, self).__init__()
        QWidget.__init__(self)

        self.ui = ui
        self.ui.max_pixel_display.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    ####################################################################################################################
    def set_text(self, value: int) -> None:
        """
        Method to add row of text to display window.
        :param value: int to be set in display window
        """
        self.clear_text()
        self.ui.max_pixel_display.setText(str(value))

        return

    ####################################################################################################################
    def clear_text(self) -> None:
        """
        Method to clear stream display.
        """
        self.ui.max_pixel_display.clear()

        return
