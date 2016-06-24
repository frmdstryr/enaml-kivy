'''
Created on Jun 23, 2016

@author: jrm
'''
from setuptools import setup, find_packages


setup(
    name='enaml-kivy',
    version='0.1.0',
    author='frmdstryr',
    author_email='frmdstryr@gmail.com',
    url='https://gitlab.com/frmdstryr/enaml-kivy',
    description='Kivy Toolkit for Enaml',
    license = "MIT",
    long_description=open('README.md').read(),
    requires=['atom', 'enaml', 'kivy'],
    install_requires=['distribute', 'atom >= 0.3.8', 'enaml >= 0.9.8'],
    packages=find_packages(),
)
