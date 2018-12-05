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

from h5py import Group
import numpy as np

class Subset(Group):

    def __init__(self, identifier):
        super().__init__(identifier)

    @staticmethod
    def create(parent, name, freq_bins, gps_support, dtype=np.float64, compression=None):
        if name in parent:
            raise Exception("Subset %s already exists" % name)

        if not dtype in [np.uint8, np.uint16, np.float32, np.float64]:
            raise Exception("The class 'Subset' does not support the specified dtype: %s" %dtype)

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
        group.create_dataset("spectrum", (0,freq_bins.size), dtype=dtype, compression=compression, maxshape=(None,freq_bins.size), chunks=(32,freq_bins.size))

    # Store sample
    def append_sample(self, time, spectrum, lat=None, lon=None, alt=None, speed=None, sats=None, accuracy=None):
        if self.supports_gps:
            if (lat == None) or (lon == None):
                raise Exception("You need to provide lat and lon arguments if gps support is enabled '%s'" %self.name)
        if not len(self.freq_bins) == len(spectrum):
            raise Exception("Length of spectrum does not match the specified frequency bins. Expected length: %d, but got: %d" %(len(self.freq_bins), len(spectrum)))

        time = np.datetime64(time)
        time = np.uint64(time)

        self.meta.resize( (self.meta.len() + 1,) )
        if self.supports_gps:
            self.meta[-1] = (time, lat, lon, alt, speed, sats, accuracy)
        else:
            self.meta[-1] = (time)

        # Write spectrum data
        self.spectrum.resize( (self.spectrum.len() + 1,len(spectrum)) )
        self.spectrum[-1] = spectrum

    def __getitem__(self, index):
        if index in self:
            return Subset(super().__getitem__(index).id)
        else:
            raise Exception("Subset '%s' does not exist" %index)

    @property
    def meta(self):
        return super().__getitem__("meta")

    @property
    def spectrum(self):
        return super().__getitem__("spectrum")

    @property
    def supports_gps(self):
        return self.attrs["gps_support"]

    @property
    def freq_bins(self):
        return super().__getitem__("freq_bins")

    def len(self):
        return self.meta.len()
