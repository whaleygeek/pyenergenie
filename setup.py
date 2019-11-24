try: 
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: 
    # for pip <= 9.0.3
    from pip.req import parse_requirements
from setuptools import setup

# read the long description
with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

# read the requirements.txt
requirements = [str(r.req) for r in parse_requirements('requirements.txt', session='hack')]

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
    package_dir={'pyenergenie': 'src/', 'energenie': 'src/energenie/'},
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
