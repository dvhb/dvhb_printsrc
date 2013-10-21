# -*- coding: utf-8 -*-

import os

from setuptools import setup

__version__ = "0.0.5"

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


setup(
    name='dvhb_printsrc',
    version=__version__,
    packages=['dvhb_printsrc'],
    include_package_data=True,
    license='private',
    description='Library for generation printable .html file from selected source files in directory.',
    long_description=README,
    url='https://github.com/dvhb/dvhb_printsrc/',
    author='Vadim Lopatyuk',
    author_email='vl@dvhb.ru',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'pygments',
    ],
)
