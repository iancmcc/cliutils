#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
import sys, os

version = '0.1'

LONG_DESC = """

"""

setup(name='cliutils',
      version=version,
      description="A collection of utilities easing the creation of command line scripts",
      long_description=LONG_DESC,
      classifiers=[
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='Ian McCracken',
      author_email='ian.mccracken@gmail.com',
      url='http://code.google.com/p/cliutils',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      entry_points="",
      )
