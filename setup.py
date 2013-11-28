#! /usr/bin/env python2

import sys
from distutils.core import setup

# Patch distutils if it can't cope with
# the "classifiers" or "download_url" keywords.
if sys.version < '2.2.3':
  from distutils.dist import DistributionMetadata
  DistributionMetadata.classifiers = None
  DistributionMetadata.download_url = None

#
# Setup.
#
setup(name='weibo4pic',
      version='0.0.1',
      description='Yet Another Getting Things Done',
      author='wxg',
      author_email='wxg4dev@gmail.com',
      contact='wxg',
      contact_email='wxg4dev@gmail.com',
      long_description='a demo for sina weibo sdk',
      license='GNU General Public License',
      url='https://github.com/wxg4net/weibo4pic',
      download_url = 'https://github.com/wxg4net/weibo4pic/archive/master.zip',
      platforms='Theorically all platforms.',
      package_dir = {'': 'src'},
      packages = ['weibo'],
      scripts=['src/weibo4pic.py'],
      classifiers = ['Development Status :: 4 - Beta',
                     'Intended Audience :: End Users/Desktop',
                     'Environment :: Console (Text Based)',
                     'License :: OSI Approved :: GNU General Public License (GPL)',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Office/Business']
      )
