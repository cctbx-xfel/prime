#!/usr/bin/env python
"""
Minimal setup.py for building PRIME C++ extensions against conda cctbx
"""
import os
import sys
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import subprocess


def get_conda_prefix():
    """Get the active conda environment prefix"""
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if not conda_prefix:
        raise RuntimeError("No active conda environment found. Please activate the prime-env environment.")
    return conda_prefix


def get_site_packages():
    """Get the site-packages directory"""
    import site
    site_packages = site.getsitepackages()
    if site_packages:
        return site_packages[0]
    # Fallback
    conda_prefix = get_conda_prefix()
    python_ver = f"python{sys.version_info.major}.{sys.version_info.minor}"
    return os.path.join(conda_prefix, 'lib', python_ver, 'site-packages')


def find_boost_python_lib():
    """Find the correct boost_python library name"""
    conda_prefix = get_conda_prefix()
    lib_dir = os.path.join(conda_prefix, 'lib')
    
    # Try common boost_python naming patterns
    patterns = [
        'boost_python',  # Generic
        f'boost_python{sys.version_info.major}{sys.version_info.minor}',  # e.g., boost_python39
        f'boost_python{sys.version_info.major}',  # e.g., boost_python3
    ]
    
    for pattern in patterns:
        # Check for .so on Linux, .dylib on macOS
        for ext in ['.so', '.dylib', '.a']:
            if os.path.exists(os.path.join(lib_dir, f'lib{pattern}{ext}')):
                return pattern
    
    # Default fallback
    return 'boost_python'


class BuildExt(build_ext):
    """Custom build extension"""
    
    def build_extensions(self):
        # Get conda environment paths
        conda_prefix = get_conda_prefix()
        
        # Add conda include and lib directories to all extensions
        for ext in self.extensions:
            ext.include_dirs.insert(0, os.path.join(conda_prefix, 'include'))
            ext.library_dirs.insert(0, os.path.join(conda_prefix, 'lib'))
            
            # Platform-specific flags
            if sys.platform == 'darwin':
                ext.extra_compile_args.extend(['-std=c++11', '-stdlib=libc++'])
                ext.extra_link_args.extend(['-stdlib=libc++'])
            elif sys.platform.startswith('linux'):
                ext.extra_compile_args.extend(['-std=c++11'])
        
        super().build_extensions()


# Get paths from conda environment
conda_prefix = get_conda_prefix()
site_packages = get_site_packages()
boost_python_lib = find_boost_python_lib()

# Include directories from conda cctbx installation
include_dirs = [
    os.path.join(conda_prefix, 'include'),
    site_packages,  # For scitbx, cctbx headers in site-packages
    os.path.join(site_packages, 'scitbx'),
    os.path.join(site_packages, 'cctbx'),
    os.path.join(site_packages, 'boost_adaptbx'),
    os.path.join(conda_prefix, 'include', 'boost'),
]

# Library directories
library_dirs = [
    os.path.join(conda_prefix, 'lib'),
]

# Common libraries needed
libraries = [
    'cctbx',
    'scitbx_boost_python',
    boost_python_lib,
]

# Define extensions
# Note: The module names must match what the C++ code exports and what __init__.py imports
extensions = [
    Extension(
        'prime_ext',  # This is what the C++ BOOST_PYTHON_MODULE macro expects
        sources=['src/prime/ext.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=['-O3'],
        language='c++',
    ),
    Extension(
        'prime_index_ambiguity_ext',  # This is what index_ambiguity/__init__.py imports
        sources=['src/prime/index_ambiguity/ext.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=['-O3'],
        language='c++',
    ),
]

setup(
    name='prime',
    version='0.1.0',
    description='PRIME - Archived crystallography post-refinement package',
    package_dir={'': 'src'},
    packages=['prime', 'prime.command_line', 'prime.postrefine', 'prime.index_ambiguity', 'prime.isoform_cluster'],
    ext_modules=extensions,
    cmdclass={'build_ext': BuildExt},
    python_requires='>=3.8',
)
