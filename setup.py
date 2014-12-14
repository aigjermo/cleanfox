from setuptools import setup

setup(
    name='CleanFox',
    version='0.1.0',
    author='Anders Iver Gjermo',
    author_email='ai@gjermo.com',
    packages=['cleanfox'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Spawn disposable firefox sessions',
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts':[
            'cleanfox = cleanfox.core:script_entry'
        ]
    },
    install_requires=[
        #"Django >= 1.1.1",
        #"caldav == 0.1.4",
    ],
)
