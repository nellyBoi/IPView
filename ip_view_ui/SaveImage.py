"""
Nelly Kane
11.10.2019

A class to same an image in the current display to a file.
"""
from PyQt5.QtWidgets import QWidget, QFileDialog

import ipview_ui


########################################################################################################################
class SaveImage(QWidget):
    """
    """

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        """
        """
        self.ui = ui
        super(SaveImage, self).__init__()
        self.file_name = None

        # Store a local handle to the scene's current image pixmap.
        self.__pixmap_handle = None

    ####################################################################################################################
    def save_button_pressed(self) -> None:
        """
        Method to pull up a save-as dialog box and allow the user to save the file in the current image_display.
        """
        current_image = self.ui.image_display.grab(self.ui.image_display.sceneRect().toRect())
        image_size = current_image.size()
        self.__save_file_dialog()

        if self.file_name is not None:
            current_image.save(self.file_name)

    ####################################################################################################################
    def __save_file_dialog(self):
        options = QFileDialog.Options()
        self.file_name, _ = QFileDialog.getSaveFileName(self, "Save image as", "",
                                                        "All Files (*);;Text Files (*.txt)", options=options)
        if self.file_name:
            print('Saving: ' + str(self.file_name))

    ####################################################################################################################
    def has_image(self):
        """ Returns whether or not the scene contains an image pixmap.
        """
        return self._pixmapHandle is not None
