from distutils.core import setup

setup(
    name='jsonTOxls',
    version='0.01',
    packages=['client','server','client/examples','common'],
    license='GPL',
    long_description=open('README.md').read(),
)
