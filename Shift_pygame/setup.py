#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'

from setuptools import setup, find_packages

setup(
    name='Shift_pygame',
    version='0.1',
    keywords=('Shift',),
    description='A Python implementation of Shift, using pygame library.',
    license='MIT',

    url='https://github.com/fyabc/MiniGames/tree/master/Shift_pygame',
    author='fyabc',
    author_email='fyabc@mail.ustc.edu.cn',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[],

    scripts=[],
    entry_points={
        'console_scripts': [
            'shift-pygame = Shift_pygame.main:main',
        ],
    },
)
