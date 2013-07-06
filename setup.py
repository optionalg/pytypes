from os import path
from setuptools import setup


def read(filename):
    return open(filename, 'r').read()


setup(
    name='pytypes',
    version='0.1',
    packages=['pytypes', 'pytypes.test'],
    requires=['funcparserlib'],
    url='https://github.com/JetBrains/pytypes',
    license='Apache License 2.0',
    author='Andrey Vlasovskikh',
    author_email='andrey.vlasovskikh@gmail.com',
    description='Type annotations for Python',
    long_description=read(path.join(path.dirname(__file__), 'README.rst')),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Documentation',
    ])
