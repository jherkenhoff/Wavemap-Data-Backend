class Spectrum:
    def __init__(self, freq, mag):
        # TODO: Type checks
        self.__freq = freq
        self.__mag = mag

    @property
    def freq(self):
        return self.__freq

    @property
    def mag(self):
        return self.__mag
