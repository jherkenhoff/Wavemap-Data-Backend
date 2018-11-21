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

from h5py import AttributeManager

class Device(AttributeManager):
    def __init__(self, parent):
        super().__init__(parent)

    @property
    def name(self):
        if "device_name" in self:
            return self["device_name"]
        else:
            return None

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self["device_name"] = name
        else:
            raise Exception("Device name must be a string")

    @property
    def version(self):
        if "device_version" in self:
            return self.__file.attrs["device_version"]
        else:
            return None

    @version.setter
    def version(self, version):
        if isinstance(version, str):
            self["device_version"] = version
        else:
            raise Exception("Device version must be a string")
