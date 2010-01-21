#!/usr/bin/env python
from DistUtilsExtra.command import *
import glob
from distutils.core import setup

setup(name='batterymon',
      version="1.2.4",
      description='A GNOME applet to monitor battery usage',
      author='Matthew Horsell',
      author_email='matthew.horsell@gmail.com',
      url='http://code.google.com/p/batterymon',
      package_dir={'batterymon': ''},
      packages = ['batterymon'],
      scripts=['batterymon'],
      data_files=[('share/batterymon/icons/gnome', 
                glob.glob('icons/gnome/*.png')), 
        ('share/batterymon/icons/default',
                glob.glob('icons/default/*.png'))], 
      cmdclass = { "build" : build_extra.build_extra,
                   "build_i18n" :  build_i18n.build_i18n },
      )
