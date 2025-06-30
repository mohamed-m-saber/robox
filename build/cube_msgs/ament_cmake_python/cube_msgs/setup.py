from setuptools import find_packages
from setuptools import setup

setup(
    name='cube_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('cube_msgs', 'cube_msgs.*')),
)
