import os.path
import h5py
import numpy as np

class Dataset:

    def __init__(self, path, device_info=None):
        self.__path = path
        self.__name = os.path.splitext(os.path.basename(path))[0]


        if (device_info == None):
            # Open in read only mode
            self.__write_access = False
            self.__file = h5py.File(path, "r")
        else:
            self.__write_access = True
            if (os.path.isfile(self.__path)):
                # Open in write mode
                self.__file = h5py.File(self.__path, "a")
                if not self.is_device_compatible(device_info):
                    raise Exception("Tried to open dataset with incompatible device_info")
            else:
                # Create new dataset
                self.__file = h5py.File(self.__path, "a")
                self.__write_device_info(device_info)
                self.__create_empty_dataset(device_info)


    def __needs_write_access(func):
        """ Decorator function used to check if write access is granted before executing a function """
        def wrapper_needs_write_access(self, *args, **kwargs):
            if (self.__write_access):
                func(self, *args, **kwargs)
            else:
                raise Exception("Tried to execute %s without write access to dataset" %str(func))
        return wrapper_needs_write_access


    @__needs_write_access
    def __write_device_info(self, device_info):
        # TODO: Check for required keys in device_info
        for key, value in device_info.items():
            self.__file.attrs[key] = value


    def is_device_compatible(self, device_info):
        for key, value in device_info.items():
            try:
                if (np.all(self.__file.attrs[key] != value)):
                    return False
            except Exception as e:
                return False

        return True


    @__needs_write_access
    def __create_empty_dataset(self, device_info):
        dtype = np.dtype([("time", np.uint64),
                      ("gps_lat", np.float64),
                      ("gps_lon", np.float64),
                      ("gps_alt", np.float64),
                      ("gps_speed", np.float64),
                      ("gps_sats", np.uint8),
                      ("gps_accuracy", np.float32),
                      ("spectrum", np.float64, len(device_info["frequency_bins"]))])
        self.__file.create_dataset("samples", (0,), dtype=dtype)



    def get_write_access(self, device_info):
        if self.is_device_compatible(device_info):
            # Reopen hdf5 file in write/create mode
            self.__write_access = True
            self.__file.flush()
            self.__file.close()
            self.__file = h5py.File(self.__path, "a")
        else:
            raise Exception("Tried to get write access to dataset with incompatible device_info")

    @__needs_write_access
    def append_sample(self, sample):
        dset = self.__file["."]["samples"]


    @property
    def name(self):
        return self.__name


    @property
    def has_write_access(self):
        return self.__write_access


    @property
    def device_info(self):
        return dict(self.__file.attrs.items())


    def iterate_samples(self):
        pass

if __name__ == '__main__':
    device_info = {
        "name": "Red Pitaya",
        "version": "1.8",
        "method": "FFT + Maxhold",
        "gps_support": False,
        "frequency_bins": [50e6, 60e6, 70e6]
    }
    dataset = Dataset("/home/jost/Projects/Controller-Backend/test11.hdf", device_info);
