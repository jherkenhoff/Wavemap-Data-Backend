# Copyright 2018 Jost Herkenhoff
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to
# do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from h5py import Group, Dataset
import numpy as np

class Subset(Group):

    MIN_SPECTRUM_VALUE = -150
    MAX_SPECTRUM_VALUE = 20

    def __init__(self, identifier):
        """Subset Constructor
        The argument 'identifier' must be a valid h5py group-identifier"""
        super().__init__(identifier)

        # Convert value transformation coefficients:
        dtype = super().__getitem__("spectrum").dtype
        if (dtype == np.uint8 or dtype == np.uint16):
            # Linear equation system:
            # MIN_SPECTRUM_VALUE * scale + offset = dtype.min
            # MAX_SPECTRUM_VALUE * scale + offset = dtype.max
            dtype_min = np.iinfo(dtype).min
            dtype_max = np.iinfo(dtype).max

            a = np.array([[Subset.MIN_SPECTRUM_VALUE, 1], [Subset.MAX_SPECTRUM_VALUE, 1]])
            b = np.array([dtype_min, dtype_max])
            x = np.linalg.solve(a, b)
            self.__value_transform_scale = x[0]
            self.__value_transform_offset = x[1]
        else:
            self.__value_transform_scale = 1
            self.__value_transform_offset = 0

    @staticmethod
    def create(parent, name, freq_bins, gps_support, dtype=np.float32, compression=None):
        """Creates a new Subset"""
        if name in parent:
            raise Exception("Subset %s already exists" % name)

        if not dtype in [np.uint8, np.uint16, np.float32, np.float64]:
            raise Exception("The class 'Subset' does not support the specified dtype: %s. (Supported dtypes: np.uint8, np.uint16, np.float32, np.float64)" %str(dtype))

        # Create group for subset
        group = parent.create_group(name)

        # Write subset-metadata
        group.attrs["gps_support"] = gps_support

        if gps_support:
            meta_dtype = np.dtype([("time", np.uint64),
                              ("lat", np.float64),
                              ("lon", np.float64),
                              ("alt", np.float32),
                              ("speed", np.float32),
                              ("sats", np.uint8),
                              ("accuracy", np.float32)])
        else:
            meta_dtype = np.dtype([("time", np.uint64)])

        group.create_dataset("freq_bins", data=freq_bins)
        group.create_dataset("meta", (0,), dtype=meta_dtype, maxshape=(None,), chunks=(16,))
        group.create_dataset("spectrum", (0,len(freq_bins)), dtype=dtype, compression=compression, maxshape=(None,len(freq_bins)), chunks=(32,len(freq_bins)))

    # Store sample
    def append_sample(self, time, spectrum, lat=None, lon=None, alt=None, speed=None, sats=None, accuracy=None):
        # Check arguments
        if self.supports_gps:
            if (lat == None) or (lon == None):
                raise Exception("You need to provide lat and lon arguments if gps support is enabled '%s'" %self.name)
        if not len(self.freq_bins) == len(spectrum):
            raise Exception("Length of spectrum does not match the specified frequency bins. Expected length: %d, but got: %d" %(len(self.freq_bins), len(spectrum)))

        # Check spectrum bounds (min, max values)
        spectrum = np.array(spectrum)
        if (spectrum.max() > Subset.MAX_SPECTRUM_VALUE or spectrum.min() < Subset.MIN_SPECTRUM_VALUE):
            raise Exception("Spectrum values out of bounds: Expected [min=%.3f, max=%.3f], but got [min=%.3f, max=%.3f]" % (Subset.MIN_SPECTRUM_VALUE, Subset.MAX_SPECTRUM_VALUE, spectrum.min(), spectrum.max()))

        # Convert time argument to uint64
        time = np.uint64(np.datetime64(time))

        # Grow datasets by one row
        self.meta.resize( (self.meta.len() + 1,) )
        self.spectrum.resize( (self.spectrum.len() + 1,len(spectrum)) )

        # Write metadata
        if self.supports_gps:
            self.meta[-1] = (time, lat, lon, alt, speed, sats, accuracy)
        else:
            self.meta[-1] = (time)

        # Convert spectrum data to correct dtype
        spectrum = spectrum * self.__value_transform_scale + self.__value_transform_offset
        spectrum = spectrum.astype(self.spectrum.dtype)

        # Write spectrum data
        self.spectrum[-1] = spectrum

    @property
    def meta(self):
        return super().__getitem__("meta")

    @property
    def spectrum(self):
        class Spectrum_Value_Transform(Dataset):
            """Wrapper class to transform values back to float64 with correct scale and offset"""
            def __init__(self, dataset_identifier, scale, offset):
                super().__init__(dataset_identifier)
                self.__scale = scale
                self.__offset = offset

            def __getitem__(self, index):
                if (super().__getitem__(index).dtype == np.float64):
                    return (super().__getitem__(index).astype(np.float64) - self.__offset) / self.__scale
                else:
                    return (super().__getitem__(index).astype(np.float32) - self.__offset) / self.__scale

        return Spectrum_Value_Transform(super().__getitem__("spectrum").id, self.__value_transform_scale, self.__value_transform_offset)

    @property
    def supports_gps(self):
        return self.attrs["gps_support"]

    @property
    def freq_bins(self):
        return super().__getitem__("freq_bins")

    def len(self):
        return self.meta.len()
