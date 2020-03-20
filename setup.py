#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='python-netbox',
      version='0.0.15',
      description='Python NetBox Client',
      long_description=readme(),
      python_requires='>=3',
      author='Thomas van der Jagt',
      author_email='thomas@tjrb.nl',
      url='https://github.com/jagter/python-netbox',
      download_url='https://github.com/jagter/python-netbox/releases/tag/0.0.15.tar.gz',
      packages=find_packages(),
      install_requires=['ipaddress', 'requests'],
      classifiers = [
        "Programming Language :: Python :: 3",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
      ],
     )
