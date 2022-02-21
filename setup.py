#!/usr/bin/env python
#DOCLINES = 'This Python library provides an implementation of the Target-Approximation-Model.\n\
#\n\
#Core features are:\
#- a one dimensional aero-acoustic simulation of vocal tract dynamics using a\
#  vocal tract model based on MRI scans of a human vocal tract\
#- synthesis of artificial speech through high-level gestural control or low-\
#  level motor control of individual articulators through dynamic targets\
#- extensive visualization options\
#- estimation of articulatory targets from audio files directly (pitch target-\
#  estimation) or from arbitrary data (e.g. articulatory measurements)\
#- phoneme-to-speech functionality and a basic text-to-speech pipeline\
#- and much more\
#\
#Besides the scientific purpose, this module is well suited for any production\
#environments that need to access the VocalTractLab-backend.\
#VocalTractLab and its Python module are licensed under GPL-3.0.'


import os, sys
import logging
import subprocess
import shutil

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.extension import Extension

import numpy as np
from Cython.Build import cythonize
import cmake


WORKING_PATH = os.getcwd()

class Build_Target_Optimizer( build_py ):
    """Build TargetOptimizer-Backend API"""
    def run( self ):
        print( 'Building Target_Optimizer-Backend using cmake:' )
        os.chdir( 'Target-Approximation-Model/src/targetoptimizer-backend' )
        #with TemporaryDirectory() as tmpdir:
        #    os.chdir(tmpdir)
        subprocess.check_call( [ 'cmake', '.' ] )
        subprocess.check_call( [ 'cmake', '--build', '.', '--config', 'Release' ] )
        api_name = 'TargetOptimizerApi'
        if sys.platform == 'win32':
            file_extension = '.dll'
            shutil.move( os.path.join( 'Release', api_name + file_extension ), os.path.join( WORKING_PATH, 'Target-Approximation-Model' ) )
            shutil.move( os.path.join( 'release', api_name + '.lib' ), os.path.join( WORKING_PATH, 'Target-Approximation-Model' ) )
        else:
            file_extension = '.so'
            shutil.move( 'lib' + api_name + file_extension, os.path.join( WORKING_PATH, 'Target-Approximation-Model' ) )
        #print( os.listdir( os.getcwd() ) )
        #print( os.listdir( os.path.join( os.getcwd(), 'CMakeFiles' ) ) )
        shutil.move( os.path.join( '', api_name + '.h' ), os.path.join( WORKING_PATH, 'Target-Approximation-Model' ) )
        shutil.move( os.path.join( '', 'Data.h' ), os.path.join( WORKING_PATH, 'Target-Approximation-Model' ) )
        os.chdir( WORKING_PATH )
        #build_py.run( self )


class Build_Backends( build_py ):
    def run(self):
        self.run_command( 'build_target_optimizer' )
        build_py.run(self)




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


# Build extension modules 
EXT_MODULES = cythonize(
    [
        Extension( 'Target-Approximation-Model.target_estimation',
              ['Target-Approximation-Model/target_estimation.pyx'],
              language="c++",
              libraries=['Target-Approximation-Model/TargetOptimizerApi'],
              library_dirs=['.'],#, './src/', './src/targetoptimizer-backend/'],
              include_dirs=[np.get_include()],#, './src/', './src/targetoptimizer-backend/']
              ),
    ]
)

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
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Programming Language :: C++
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development
Topic :: Scientific/Engineering
Typing :: Typed
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
"""


cmdclass = dict(
    build_target_optimizer = Build_Target_Optimizer,
    build_py = Build_Backends,
    )
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
    ext_modules=EXT_MODULES,
    cmdclass = cmdclass,
    include_dirs=np.get_include(),
    packages=find_packages(),
    package_dir={'Target-Approximation-Model': 'Target-Approximation-Model'},
    package_data= {'Target-Approximation-Model': [ 
                              os.path.join( WORKING_PATH, 'Target-Approximation-Model/src/targetoptimizer-backend/*' ),
                              os.path.join( WORKING_PATH, 'Target-Approximation-Model/src/targetoptimizer-backend/dlib/*' ),
                              os.path.join( WORKING_PATH,'./Target-Approximation-Model/*' ) ]},
    include_package_data = True,
    install_requires=DEPENDENCIES,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    #zip_safe= False,
)






setup(**setup_args)