# EOS Python Utilities
A common utils framework which includes common modules across components
## Build
Use setup.py to update the eos-py-utils distributive.
```bash
python3 setup.py bdist_wheel
```
setup.py is also able to build RPMs. Run
```bash
python3 setup.py bdist_rpm
```
## Installation
Use pip and the wheel file to install the package. E.g.
```bash
cd dist
pip3 install eos-0.1-py3-none-any.whl
```
Use pip to uninstall the package
```bash
pip3 uninstall eos
```
## Usage
After eos package is installed, it can be used the common way as any other Python module, E.g.:
```python
from eos.utils.security.cipher import Cipher
```
### Security
#### Cipher
All Cipher methods are static, parameters contain all the neccessary information to perform tasks.

Use `generate_key` method to create an encryption key. The method requires two strings (could be considered
as salt and password), but user can pass more strings if neccessary:
```python
key = Cipher.generate_key('salt','pass','more','strings')
```
Use the obtained key to `encrypt` or `decrypt` your data. Note, that all arguments must be `bytes`:
```python
encrypted = Cipher.encrypt(key, b'secret')
decrypted = Cipher.decrypt(key, encrypted)
```
Note that `decrypt` method might raise a `CipherInvalidToken` exception if the key is not valid.
User might need to handle the exception gracefully if not sure about the key:
```python
try:
    decrypted = Cipher.decrypt(key, encrypted)
except CipherInvalidToken:
    print('Key is wrong')
```

