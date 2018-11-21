import os.path
import h5py
import numpy as np

# Local modules
from sample import Sample


class Dataset:

    FILE_EXTENSION = ".hdf"

    def __init__(self, directory, name, write_access=True):

        self.__directory = directory
        self.__name = name

        # Open HDF5 file
        self.__path = os.path.join(directory, name + Dataset.FILE_EXTENSION)
        self.__file = h5py.File(self.__path, "a")

        # Initialize Device subclass
        self.__device = Dataset.Device(self.__file)

        # Initialize Samples subclass
        self.__samples = Dataset.Samples(self.__file)

    class Device:
        def __init__(self, file):
            self.__file = file

        @property
        def name(self):
            if "device_name" in self.__file.attrs:
                return self.__file.attrs["device_name"]
            else:
                return None

        @name.setter
        def name(self, name):
            if isinstance(name, str):
                self.__file.attrs["device_name"] = name
            else:
                raise Exception("Device name must be a string")

        @property
        def version(self):
            if "device_version" in self.__file.attrs:
                return self.__file.attrs["device_version"]
            else:
                return None

        @version.setter
        def version(self, version):
            if isinstance(version, str):
                self.__file.attrs["device_version"] = version
            else:
                raise Exception("Device version must be a string")

    class Samples:
        def __init__(self, file):
            self.__file = file

        def __len__(self):
            return 8

        def __getitem__(self, i):
            print(i)

        def append(self, sample):
            if not isinstance(sample, Sample):
                raise Exception("Can only append instances of type 'Sample' to dataset")

    class Subset:
        def __init__(self, hd5_dataset):
            self.__hd5_dataset = hd5_dataset

    def create_subset(self, name, freq_bins, gps_support):
        if name in self.__file:
            raise Exception("Subset %s already exists" % name)
        if gps_support:
            dtype = np.dtype([("time", np.uint64),
                          ("gps_lat", np.float64),
                          ("gps_lon", np.float64),
                          ("gps_alt", np.float64),
                          ("gps_speed", np.float64),
                          ("gps_sats", np.uint8),
                          ("gps_accuracy", np.float32),
                          ("spectrum", np.float64, len(device_info["frequency_bins"]))])
        else:
            dtype = np.dtype([("time", np.uint64),
                      ("spectrum", np.float64, freq_bins)])

        self.__file.create_dataset(name, (0,), dtype=dtype)

    def __len__(self):
        return len(self.__file)

    def __getitem__(self, index):
        return Dataset.Subset(self.__file[index])

    @property
    def name(self):
        return self.__name

    @property
    def device(self):
        return self.__device

    @property
    def samples(self):
        return self.__samples

    def close(self):
        self.__file.flush()
        self.__file.close()


if __name__ == '__main__':
    from spectrum import Spectrum
    from gps import GPS

    dataset = Dataset("./", "Neustadt")
    print(dataset["minhold"])

    dataset.close()
