# setup.py
from setuptools import setup

setup(
    name='kernel-remove',
    version='0.1',
    packages=['kernel-remove'],
    install_requires=['inquirer'],
    entry_points={
        'console_scripts': [
            'kernel-remove=kernel-remove.main:main',
        ],
    },
)