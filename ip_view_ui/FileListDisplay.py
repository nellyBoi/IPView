"""
Nelly Kane
11.02.2019

A class to control the 'text_list_display' of IPView.
"""
from PyQt5 import QtWidgets
import ipview_ui


########################################################################################################################
class FileListDisplay(QtWidgets.QTextEdit):
    """

    """
    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        """
        """
        super(FileListDisplay, self).__init__()

        self.ui = ui

    ####################################################################################################################
    def load_directory_button_pushed(self) -> None:
        """
        Slot method for loading directory upon load push button.
        """
        directory = self.ui.directory_input.toPlainText()
        files_for_display = self.ui.app_data.load_directory(directory=directory)
        if len(files_for_display) == 0:
            self.ui.text_list_display.setText('No Compatible Images')
        else:
            string = '\n'.join(map(str, files_for_display))
            self.ui.text_list_display.setText(string)

        return
