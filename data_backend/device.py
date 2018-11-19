


class Device:
    def __init__(self):
        self.__name = ""
        self.__version = ""
        self.__method = ""
        self.__gps = False
        self.__freq_bins = []

        self.__write_access = True

    @property
    def readonly(self):
        return self.__readonly

    @readonly.setter
    def readonly(self, value):


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name)
        if self.__readonly:
            raise Exception("Writing parameter 'name' of device is not allowed in read-only mode")
        else:
            self.__name = name
