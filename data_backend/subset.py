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

from h5py import Dataset
import numpy as np

class Subset(Dataset):

    def __init__(self, identifier):
        super().__init__(identifier)

    @staticmethod
    def create(parent, name, freq_bins, gps_support):
        if name in parent:
            raise Exception("Subset %s already exists" % name)
        if gps_support:
            dtype = np.dtype([("time", np.uint64),
                              ("lat", np.float64),
                              ("lon", np.float64),
                              ("alt", np.float32),
                              ("speed", np.float32),
                              ("sats", np.uint8),
                              ("accuracy", np.float32),
                              ("spectrum", np.float64, len(freq_bins))])
        else:
            dtype = np.dtype([("time", np.uint64),
                              ("spectrum", np.float64, len(freq_bins))])

        dset = parent.create_dataset(name, (0,), dtype=dtype, maxshape=(None,), chunks=(16,))
        dset.attrs["gps_support"] = gps_support
        dset.attrs["freq_bins"] = freq_bins

    # Store sample
    def append_sample(self, time, spectrum, lat=None, lon=None, alt=None, speed=None, sats=None, accuracy=None):
        if self.supports_gps:
            if (lat == None) or (lon == None):
                raise Exception("You need to provide lat and lon arguments if gps support is enabled '%s'" %self.name)
        if not len(self.freq_bins) == len(spectrum):
            raise Exception("Length of spectrum does not match the specified frequency bins. Expected length: %d, but got: %d" %(len(self.freq_bins), len(spectrum)))

        self.resize( (self.len() + 1,) )
        if self.supports_gps:
            self[-1] = (time, lat, lon, alt, speed, sats, accuracy, spectrum)
        else:
            self[-1] = (time, spectrum)

    @property
    def samples(self):
        return Dataset.Subset.Samples(self.__hd5_dataset)

    @property
    def supports_gps(self):
        return self.attrs["gps_support"]

    @property
    def freq_bins(self):
        return self.attrs["freq_bins"]
