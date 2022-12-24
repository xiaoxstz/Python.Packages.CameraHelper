from setuptools import setup
from Cython.Build import cythonize

import glob # find path with given pattern

import sys,os
cur_path = sys.path[0]
os.chdir(cur_path)

# para = sys.argv[1]
file_patterns =["./CameraHelper/*.py",]
file_list = []
for pattern in file_patterns:
    file_list += glob.glob(pattern)

setup(
    name="CameraHelper",
    ext_modules=cythonize(file_list),
    zip_safe=False,
)
