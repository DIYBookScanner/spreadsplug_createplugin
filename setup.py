#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    install_requires=['spreads'],
    name='spreadsplug_createplugin',
    provides=['spreadsplug_createplugin'],
    version='0.1',
    author='Matti Kariluoma <matti@kariluo.ma>',
    author_email='matti@kariluo.ma',
    description='Spreads (http://github.com/DIYBookScanner/spreads http://spreads.readthedocs.org) plugin',
    license='MIT',
    classifiers=['Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX',
        'Topic :: Multimedia :: Graphics :: Capture',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion'],
    keywords='spreads spreadsplugin',
    packages=['spreadsplug_createplugin'],
    package_dir={'spreadsplug_createplugin': 'spreadsplug_createplugin'},
    package_data={'spreadsplug_createplugin': ['template/*.in', 'template/module/*.in']},
    entry_points={u'spreadsplug.hooks': [u'CreatePlugin = spreadsplug_createplugin.CreatePluginPlugin:CreatePluginPlugin']},
  )
