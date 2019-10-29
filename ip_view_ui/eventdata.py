"""

"""
from image_containers import image_directory as im_dir
from image_containers import image as im

BUFFER_SIZE = 3


########################################################################################################################
class EventData:
    """

    """

    ####################################################################################################################
    def __init__(self) -> str:

        self.__directory = ""
        self.__image_directory = None
        self.__allowable_files = None

    ####################################################################################################################
    def load_directory(self, directory: str) -> str:
        """
        """
        self.__directory = directory
        self.__image_directory = im_dir.ImageDirectory(path_directory=directory, buffer_size=BUFFER_SIZE)
        self.__image_directory.begin_read()
        self.__allowable_files = self.__image_directory.get_list_of_allowable_files()

        return self.__allowable_files

    ####################################################################################################################
    def get_next_image(self) -> im.Image:
        """
        """
        if self.__image_directory.has_next():
            return self.__image_directory.next_image()
        else:
            return None

    ####################################################################################################################
    def clear_data(self) -> str:
        """
        """
        self.__image_directory.clear_memory()
