from setuptools import setup
from Cython.Build import cythonize

import glob  # find path with given pattern

import sys
import os
cur_path = sys.path[0]
os.chdir(cur_path)

# --------------- user define -------------
module_list = ["CameraHelper",]
# --------------- user define end-------------

# para = sys.argv[1]
file_list = []
for module in module_list:
    list_include = glob.glob(f"./{module}/*.py")
    list_exclude = glob.glob(f"./{module}{os.sep}__init__.py")
    file_list += list(set(list_include) - set(list_exclude))

setup(
    name="CameraHelper",
    ext_modules=cythonize(file_list),
    zip_safe=False,
)
