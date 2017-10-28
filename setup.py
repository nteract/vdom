#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import versioneer

ipython_req = 'ipython'

import sys
if sys.version_info[0] < 3 and 'bdist_wheel' not in sys.argv:
    ipython_req = 'ipython<6'

extras_require = {"tests": ["pytest"]}

extras_require['all'] = list(
    set([val for k, v in extras_require.items() for val in v]))

setup(
    name='vdom',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='VDOM for Python',
    author='nteract contributors',
    author_email='jupyter@googlegroups.com',
    license='BSD',
    keywords="vdom, html",
    long_description=(open('README.md').read() if exists('README.md') else ''),
    url='https://github.com/nteract/vdom',
    packages=['vdom'],
    package_data={'vdom': ['schemas/vdom_schema_v0.json']},
    install_requires=[ipython_req, 'jsonschema'],
    extras_require=extras_require)
