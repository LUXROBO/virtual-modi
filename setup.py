from os import path
from setuptools import setup, find_packages


def get_readme():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
        readme = readme_file.read()
        return readme


def get_requirements():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'requirements.txt'), encoding='utf-8') as \
            requirements_file:
        requirements = requirements_file.read().splitlines()
        return requirements


setup(
    name="virtual-modi",
    version="0.3.1",
    author="LUXROBO",
    author_email="tech@luxrobo.com",
    description=(
        "Implementation of virtual MODI modules written in Python."
    ),
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=get_requirements(),
    url="https://github.com/LUXROBO/virtual-modi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
