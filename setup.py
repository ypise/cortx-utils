"""
 ****************************************************************************
 Filename:          setup.py
 Description:       Installer for EOS py-utils package

 Creation Date:     02/13/2020
 Author:            Alexander Voronov

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from setuptools import setup


with open('LICENSE', 'r') as lf:
    license = lf.read()

with open('README.md', 'r') as rf:
    long_description = rf.read()

setup(name='eos-py-utils',
      version='0.2',
      url='http://gitlab.mero.colo.seagate.com/eos/py-utils',
      license='Seagate',
      author='Alexander Voronov',
      author_email='alexander.voronov@seagate.com',
      description='Common Python utilities for EOS',
      package_dir={'eos': 'src'},
      packages=['eos', 'eos.utils', 'eos.utils.db', 'eos.utils.security', 'eos.utils.schema'],
      package_data={
        'eos': ['py.typed'],
      },
      long_description=long_description,
      zip_safe=False,
      python_requires='>=3.6.8',
      install_requires=['cryptography==2.8', 'schematics==2.1.0', 'toml==0.10.0',
                        'PyYAML==5.1.2', 'configparser==4.0.2'])
