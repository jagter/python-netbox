#!/usr/bin/env python

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='python-netbox',
      version='1.0',
      description='Python NetBox',
      long_description=readme(),
      author='Thomas van der Jagt',
      author_email='thomas@tjrb.nl',
      url='https://github.com/jagter/python-netbox',
      packages=find_packages(),
      install_requires=['ipaddress', 'requests']
     )
