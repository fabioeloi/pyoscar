#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyoscar",
    version="0.1.0",
    author="Fabio Eloi Silva",
    author_email="fabioeloi@gmail.com",
    description="A Python port of OSCAR visualization components for data visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fabioeloi/pyoscar",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.6",
    install_requires=[
        "matplotlib>=3.4.0",
        "numpy>=1.20.0",
    ],
)
