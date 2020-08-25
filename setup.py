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

import os
import sys
from setuptools import setup

SPEC_DIR = "src/utils/ha/hac/specs/"
_ROOT = os.path.abspath(os.path.dirname(__file__)) + "/" + SPEC_DIR
specs = []
for root, directories, filenames in os.walk(_ROOT):
    for filename in filenames:
        specs.append(SPEC_DIR + filename)

with open('LICENSE', 'r') as lf:
    license = lf.read()

with open('README.md', 'r') as rf:
    long_description = rf.read()

setup(name='eos-py-utils',
      version='1.0.0',
      url='https://github.com/Seagate/cortx-py-utils',
      license='Seagate',
      author='Alexander Voronov',
      author_email='alexander.voronov@seagate.com',
      description='Common Python utilities for EOS',
      package_dir={'eos': 'src'},
      packages=['eos', 'eos.utils', 'eos.utils.cleanup',
                'eos.utils.data', 'eos.utils.data.access', 'eos.utils.data.db',
                'eos.utils.data.db.consul_db', 'eos.utils.data.db.elasticsearch_db',
                'eos.utils.security', 'eos.utils.schema', 'eos.utils.ha.hac',
                'eos.utils.ha.dm', 'eos.utils.ha.dm.models',
                'eos.utils.ha.dm.repository',
                'eos.utils.ha',
                'eos.utils.amqp', 'eos.utils.amqp.rabbitmq',
                'eos.utils.message_bus','eos.utils.message_bus.tcp',
                'eos.utils.message_bus.tcp.kafka'
                ],
      package_data={
        'eos': ['py.typed'],
      },
      entry_points={
        'console_scripts': [
            'hac = eos.utils.ha.hac.hac:main'
        ]
      },
      data_files = [ ('/var/lib/eos/ha/specs', specs),
                     ('/var/lib/eos/ha', ['src/utils/ha/hac/args.yaml', 'src/utils/ha/hac/re_build.sh'])],
      long_description=long_description,
      zip_safe=False,
      python_requires='>=3.6.8',
      install_requires=['cryptography==2.8', 'schematics==2.1.0', 'toml==0.10.0',
                        'PyYAML==5.1.2', 'configparser==4.0.2', 'networkx==2.4',
                        'matplotlib==3.1.3', 'argparse==1.4.0',
                        'confluent-kafka==1.5.0'])
