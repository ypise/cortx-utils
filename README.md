# EOS Python Utilities
A common utils framework which includes common modules across components
## Build
Use setup.py to update the eos-py-utils distributive.
```bash
python setup.py bdist_wheel
```
setup.py is also able to build RPMs. Run
```bash
python setup.py bdist_rpm
```
## Installation
Use pip and the wheel file to install the package. E.g.
```bash
cd dist
pip install eos_py_utils-0.1-py3-none-any.whl
```
Use pip to uninstall the package
```bash
pip uninstall eos_py_utils
```
