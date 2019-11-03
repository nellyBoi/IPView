"""
Nelly Kane
11.03.2019

signals_and_slots.py

IPView signals, slots and connections.
"""
from ipview_ui import IPViewWindow

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt

########################################################################################################################
class Signals:
    """
    """
    def __init__(self, ui: IPViewWindow):
        """
        Instantiation must be the last thing the GUI does.
        :param ui: IPViewWindow object
        """
        self.ui = ui
        self.directory_load_pushed = ui.directory_load_push.clicked
        self.clear_pushed = ui.clear_push_button.clicked
        self.next_button_pushed = ui.next_button.clicked


########################################################################################################################
class Slots:
    """
    """
    def __init__(self, ui: IPViewWindow):
        """
        Instantiation must be the last thing the GUI does.
        :param ui: IPViewWindow object
        """
        self.ui = ui

    ####################################################################################################################
    def load_directory_button_pushed(self) -> None:
        """
        Slot method for loading directory upon load push button.
        """
        directory = self.ui.directory_input.toPlainText()
        files_for_display = self.ui.events.load_directory(directory=directory)
        if len(files_for_display) == 0:
            self.ui.text_list_display.setText('No Compatible Images')
        else:
            string = '\n'.join(map(str, files_for_display))
            self.ui.text_list_display.setText(string)

        return

########################################################################################################################
    def clear_button_pushed(self) -> None:
        """
        Slot method for clearing all data from the UI and from memory.
        """
        self.ui.events.clear_data()
        self.ui.text_list_display.setText('')

        return

########################################################################################################################
    def next_button_pushed(self) -> None:
        """
        Slot method for a signal from the next push button.
        """
        self.__display_image()
        return

########################################################################################################################
    def __display_image(self) -> None:
        """
        """
        x = self.ui.image_display.x()
        y = self.ui.image_display.y()
        w = self.ui.image_display.width()
        h = self.ui.image_display.height()
        scene = QGraphicsScene()

        im = self.ui.events.get_next_image()
        if im is not None:

            im = im.scaled(w, h, Qt.KeepAspectRatio, Qt.FastTransformation)
            scene.addPixmap(QPixmap.fromImage(im))
            self.ui.image_display.setScene(scene)
            self.ui.image_display.show()


########################################################################################################################
class Connections:
    """
    """
    def __init__(self, ui: IPViewWindow):
        """
        Instantiation must be the last thing the GUI does.
        :param ui: IPViewWindow object
        """
        self.ui = ui
        self.__signals = Signals(ui=self.ui)
        self.__slots = Slots(ui=self.ui)

        # connect signals and slots
        self.__signals.directory_load_pushed.connect(self.__slots.load_directory_button_pushed)
        self.__signals.clear_pushed.connect(self.__slots.clear_button_pushed)
        self.__signals.next_button_pushed.connect(self.__slots.next_button_pushed)

