from setuptools import setup
from Cython.Build import cythonize

import sys

cur_path = sys.argv[1]

module_list = [
    "./CameraHelper/CamCommonWrapper.py",
    "./CameraHelper/CamPylonFreerun.py",
    "./CameraHelper/CamPylonWrapper.py",
    "./CameraHelper/PylonImageConvert.py",
    "./CameraHelper/CameraDetector.py",
]

setup(
    name="CameraHelper",
    ext_modules=cythonize(module_list),
    zip_safe=False,
)
