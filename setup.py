import os

from setuptools import setup

here = lambda *a: os.path.join(os.path.dirname(__file__), *a)

# read the long description
with open(here('README.md'), 'r') as readme_file:
    long_description = readme_file.read()

# read the requirements.txt
with open(here('requirements.txt'), 'r') as requirements_file:
    requirements = [x.strip() for x in requirements_file.readlines()]

setup(
    name='pyenergenie',
    version='0.0.1',
    description='A python interface to the Energenie line of products',
    long_description=long_description,
    author='whaleygeek',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    packages=['pyenergenie', 'pyenergenie.energenie'],
    package_dir={
        'pyenergenie': 'src/', 
        'pyenergenie.energenie': 'src/energenie/'
    },
    install_requires=requirements,
    package_data={
        'pyenergenie': [
            'energenie/drv/*'
        ]
    },
    entry_points={
        'console_scripts': [
            'pyenergenie=pyenergenie.setup_tool:main'
        ]
    }
)
