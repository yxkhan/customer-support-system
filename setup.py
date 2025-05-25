#This is required to create a setup.py file for the project. 
# This file is used to package the project and make it installable. 
# It contains information about the project, such as its name, version, author, and dependencies.
# It also specifies the packages that should be included in the distribution.
# The setup.py file is used by setuptools to create a package that can be installed using pip.

#This is required to install local package, as local installer. whereever __init__.py is created
from setuptools import find_packages,setup

setup(name="e-commerce-bot",
       version="0.0.1",
       author="sunny",
       author_email="snshrivas3365@gmail.com",
       packages=find_packages(),                #it gets the packages whereever __init__.py is created, and will be installed in the environment
       install_requires=['langchain-astradb','langchain'])  #required packages to run the project, best practice you have to write code to read the requirements.txt file and install the packages from there.

#run "pip show e-commerce-bot" in terminal to check the package is installed or not.