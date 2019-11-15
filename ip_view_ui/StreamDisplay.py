"""
Nelly Kane
11.13.2019

Controlling the streaming feature in IPView.
"""
from PyQt5.QtWidgets import QWidget

import ipview_ui


########################################################################################################################
class Singleton:
    """
    A class to emulate a singleton. This class does not operate like a true singleton, which has one and only one
    instance. Instead, each object shares a common data-state which has an identical effect.
    """
    _shared_state = {}

    ####################################################################################################################
    def __init__(self):
        self.__dict__ = self._shared_state


########################################################################################################################
class StreamDisplay(Singleton, QWidget):
    """
    A singleton-like class to control the behavior of the stream display.
    """
    def __init__(self, **kwarg):
        Singleton.__init__(self)
        self.kwargs = kwarg

    ####################################################################################################################
    def append_row(self, text_rows: str) -> None:
        """
        Method to add row of text to display window.
        :param text_rows: str to be appended to display window
        """

    ####################################################################################################################
    def clear_text(self) -> None:
        pass

    ####################################################################################################################
    def __maintain_scroll_pos(self) -> None:
        pass
