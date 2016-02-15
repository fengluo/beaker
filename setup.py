from setuptools import setup, find_packages
setup(
    name='Beaker',
    version='1.0',
    author='Shawn Xie',
    author_email='fengluo17@gmail.com',
    packages=find_packages(exclude=['sample*']),
    include_package_data=True,
    install_requires=[
        "Werkzeug"
    ])
