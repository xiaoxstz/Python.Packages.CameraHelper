# cython: language_level=3
from enum import IntEnum

from CameraHelper import CamPylonFreerun

class CameraType(IntEnum):
    CommonWrapper=0x0,
    PylonWrapper=0x1,
    PylonFreerun = 0x2,