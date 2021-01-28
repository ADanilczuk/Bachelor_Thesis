from setuptools import setup, find_packages
import pathlib


setup(
    name='Sound analysis',
    version='0.0.1',
    description='The sound analysis application.',
    long_description='long',
    author='Alicja Danilczuk, Klaudia Osowska',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['wheel'],
    project_urls={
        'Bug Reports': 'https://github.com/MartinM98/Handwriting-synthesis-with-the-help-of-machine-learning/issues',
        'Source': 'https://github.com/MartinM98/Handwriting-synthesis-with-the-help-of-machine-learning',
    },
)