# setup.py
from setuptools import setup

setup(
    name='kernel-remove',
    version='1.0',
    packages=['kernel-remove'],
    install_requires=['inquirer'],
    entry_points={
        'console_scripts': [
            'kernel-remove=kernel-remove.main:main',
        ],
    },
)