import os
from setuptools import setup

INSTALL_REQUIRES = [
        "astropy>=3.2.3",
        "jinja2"
        ]


with open("README.md", "r") as f:
    long_description= f.read()


def parse_version():
    thisdir = os.path.dirname(__file__)
    version_file = os.path.join(thisdir, 'psrcatpy', '_version.py')
    with open(version_file, 'r') as f:
        text = f.read()
    items = {}
    exec(text, None, items)
    return items['__version__']


setup(
      name="psrcatpy",
      author="Kaustubh Rajwade",
      author_email="kaustubh.rajwade@manchester.ac.uk",
      description= "A simple PSRCAT query parser",
      long_description = long_description,
      version=parse_version(),
      packages=setuptools.find_packages(),
      install_requires=INSTALL_REQUIRES)

