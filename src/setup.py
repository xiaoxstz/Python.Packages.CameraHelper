from setuptools import setup
from Cython.Build import cythonize

import sys,os
cur_path = sys.path[0]
os.chdir(cur_path)

para = sys.argv[1]
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
