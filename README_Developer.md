
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [1. Build steps](#1-build-steps)
  - [1.1. firstly,build into binary file](#11-firstlybuild-into-binary-file)
  - [1.2. secondly,build the wheel file](#12-secondlybuild-the-wheel-file)

<!-- /code_chunk_output -->

# 1. Build steps
## 1.1. firstly,build into binary file
Firstly,ensure the terminal path is `.\src`

Then, use the command below to compile the `.py` files to `.pyd` files

`python setup.py build_ext --inplace`

## 1.2. secondly,build the wheel file
Firstly,ensure the terminal path is the root folder

```bash
python -m build
```
then it will create a folder `dist` and a folder `mypackage.egg-info`
* there are `*.tar.gz` and `*.whl` in the folder `dist`