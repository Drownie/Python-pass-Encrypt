from setuptools import setup, find_packages

def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()
    
setup(
    name="PyPass Manager",
    version="2.0.0",
    description="A python password manager application",
    long_description=readfile('readme.md'),
    author="Drownie",
    author_email="abrahammahanaim02@gmail.com",
    url="https://github.com/Drownie/Python-pass-Encrypt",
    packages= ["pypass"],
    license="MIT",
)