from spectrum import Spectrum
from gps import GPS
import numpy as np

class Sample:
    def __init__(self, time, spectrum, gps=None):

        # Type checks:
        if (gps != None) and not isinstance(gps, GPS):
            raise Exception("Argument 'gps' must be an instance of class 'GPS'")
        if not isinstance(spectrum, Spectrum):
            raise Exception("Argument 'spectrum' must be an instance of class 'Spectrum'")

        # Assign to local variables:
        self.__time = np.datetime64(time)
        self.__spectrum = spectrum
        self.__gps = gps

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

    @property
    def has_gps(self):
        return self.__gps != None

    @property
    def gps(self):
        return self.__gps

    @property
    def spectrum(self):
        return self.__spectrum


# Test area:
if __name__ == '__main__':
    spectrum1 = Spectrum([1,2,3], [1,2,3])
    gps1      = GPS(8.3, 42.8)
    sample1   = Sample(np.datetime64("now"), spectrum1, gps=gps1)
