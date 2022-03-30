#!/usr/bin/env python


import os, sys
import logging
import subprocess
import shutil

from setuptools import setup, find_packages
#from setuptools.command.build_py import build_py
#from setuptools.extension import Extension

#import numpy as np
#from Cython.Build import cythonize
#import cmake




# Set up the logging environment
logging.basicConfig()
log = logging.getLogger()

# Handle the -W all flag
if 'all' in sys.warnoptions:
    log.level = logging.DEBUG

# Get version from the VocalTractLab module
with open('Target-Approximation-Model/__init__.py') as f:
    for line in f:
        if line.find('__version__') >= 0:
            version = line.split('=')[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue


# Dependencies
DEPENDENCIES = [
    'matplotlib>=3.4.3',
    'numpy>=1.22.0',
    'pandas>=1.3.2',
]


CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: C++
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Topic :: Software Development
Topic :: Scientific/Engineering
Typing :: Typed
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
"""


#cmdclass = dict(
#    build_target_optimizer = Build_Target_Optimizer,
#    build_py = Build_Backends,
#    )
#cmdclass['build_target_optimizer'] = Build_Target_Optimizer
#cmdclass['build_vtl'] = Build_VTL
#cmdclass['build_py'] = my_build

setup_args = dict(
    name='Target-Approximation-Model',
    version=version,
    description='Target-Approximation-Model for Python',
    #long_description= DOCLINES,
    url='https://github.com/paul-krug/Target-Approximation-Model',
    #download_url=,
    author='Paul Krug',
    author_email='paul_konstantin.krug@tu-dresden.de',
    license='MIT',
    classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f],
    keywords=[ 'speech synthesis', 'articulatory synthesis', 'articulatory modelling' ],
    #ext_modules=EXT_MODULES,
    #cmdclass = cmdclass,
    #include_dirs=np.get_include(),
    packages=find_packages(),
    package_dir={'Target-Approximation-Model': 'Target-Approximation-Model'},
    #package_data= {'Target-Approximation-Model': [ 
    #                          os.path.join( WORKING_PATH, 'Target-Approximation-Model/src/targetoptimizer-backend/*' ),
    #                          os.path.join( WORKING_PATH, 'Target-Approximation-Model/src/targetoptimizer-backend/dlib/*' ),
    #                          os.path.join( WORKING_PATH,'./Target-Approximation-Model/*' ) ]},
    #include_package_data = True,
    install_requires=DEPENDENCIES,
    #use_scm_version=True,
    #setup_requires=['setuptools_scm'],
    zip_safe=True,
)

setup(**setup_args)