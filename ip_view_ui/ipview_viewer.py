"""
Nelly Kane
11.02.2019

ipview_viewer.py

File to open and run IPView.
"""
import sys
from ipview_ui import IPViewWindow


########################################################################################################################
def launch() -> IPViewWindow:
    """
    :return: None
    """
    return IPViewWindow()

########################################################################################################################
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

########################################################################################################################
if __name__ == '__main__':

    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

    viewer = launch()

