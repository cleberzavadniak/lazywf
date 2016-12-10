import codecs
import os
import re

from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))

version = "0.0.0"
changes = os.path.join(here, "CHANGES.rst")
match = r'^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        res = re.match(match, line)
        if res:
            version = res.group("version")
            break

# Get the long description
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get version
with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changelog = f.read()

with codecs.open(os.path.join(here, 'requirements.txt')) as f:
    install_requires = f.readlines()


class VersionCommand(Command):
    description = "print library version"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    name='lazywf',
    version=version,
    description='The laziest web framework ever',
    long_description=long_description,
    url='https://github.com/cleberzavadniak/lazywf',
    author='Cléber Zavadniak',
    author_email='cleberman@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='lazy web framework simple microframework',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=install_requires,
    cmdclass={
        "version": VersionCommand,
    },
)
