#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    install_requires=['spreads'],
    name='spreadsplug_createplugin',
    version='0.1',
    author='Anonymous',
    author_email='nobody@example.com',
    description='Spreads (http://github.com/DIYBookScanner/spreads http://spreads.readthedocs.org) plugin',
    license='na',
    classifiers=['Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX',
        'Topic :: Multimedia :: Graphics :: Capture',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion'],
    keywords='spreads',
    packages=['spreadsplug_createplugin'],
    entry_points={u'spreadsplug.hooks': [u'CreatePlugin = spreadsplug_createplugin.CreatePluginPlugin:CreatePluginPlugin']},
  )
