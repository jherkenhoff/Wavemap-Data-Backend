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

import os.path
from h5py import File

# Local modules
from .device import Device
from .subset import Subset

class Dataset(File):

    FILE_EXTENSION = ".hdf"

    def __init__(self, directory, name, write_access=True):
        self.__name = name
        path = os.path.join(directory, name + Dataset.FILE_EXTENSION)
        super().__init__(path, "a")

    def create_subset(self, name, freq_bins, gps_support):
        # Subset creation is encapsulated in a static method in "Subset" class
        Subset.create(self, name, freq_bins, gps_support)

    def __getitem__(self, index):
        if index in self:
            return Subset(super().__getitem__(index).id)
        else:
            raise Exception("Subset '%s' does not exist" %index)

    @property
    def name(self):
        return self.__name

    @property
    def device(self):
        return Device(self)


if __name__ == '__main__':
    dataset = Dataset("./", "neusstadt")
    #dataset.create_subset("maxhold", freq_bins=[1e3, 1e4, 1e5], gps_support=True)
    dataset["maxhold"].append_sample(
        time     = 9,
        spectrum = [-87.3, -91.3, -89.2],
        lat      = 53.073635,
        lon      = 8.806422,
        alt      = 12,
        speed    = 4,
        sats     = 8,
        accuracy = 6
    )
    print(dataset["maxhold"][0:2]["spectrum"].mean(1))

    dataset.close()
