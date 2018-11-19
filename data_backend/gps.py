
# A plain dataclass (to mimic a c-like struct)
class GPS:
    def __init__(self, lat, lon, ele=None, accuracy=None, speed=None):
        self.lat      = lat
        self.lon      = lon
        self.ele      = ele
        self.accuracy = accuracy
        self.speed    = speed
