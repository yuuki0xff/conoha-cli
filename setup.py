#!/usr/bin/env python3
from setuptools import setup
import textwrap
import conoha

setup(name='conoha-cli',
      version=conoha.__version__,
      description='conoha-cli is a command and Python3 library for ConoHa API.',
      long_description=open('README.rst', 'r', encoding='utf8').read(),
      keywords='conoha cli api library cloud',
      url='https://github.com/yuuki0xff/conoha-cli',
      author='yuuki0xff',
      author_email='yuuki0xff@gmail.com',
      license='MIT',
      packages=['conoha'],
      zip_safe=False,
      classifiers=textwrap.dedent("""
        Development Status :: 5 - Production/Stable
        Environment :: Console
        Intended Audience :: Developers
        Intended Audience :: System Administrators
        License :: OSI Approved :: MIT License
        Natural Language :: Japanese
        Operating System :: POSIX :: Linux
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3 :: Only
        Programming Language :: Python :: Implementation :: CPython
        Topic :: Utilities
        """).strip().splitlines(),
      install_requires=['tabulate'],
      entry_points={
          'console_scripts': [
              'conoha-cli = conoha.cli:main',
              ],
          },
      )

# vim: expandtab
