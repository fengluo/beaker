import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('flask/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='Beaker',
    version=version,
    url='http://github.com/fengluo/beaker',
    license='Apache 2.0',
    author='Shawn Xie',
    author_email='fengluo17@gmail.com',
    discription='Beaker is a RESTful framework based on Werkzeug',
    packages=['beaker'],
    include_package_data=True,
    install_requires=[
        "Werkzeug" > 0.7
    ])
