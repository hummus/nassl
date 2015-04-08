#!/usr/bin/python2.7
from distutils.core import setup, Extension
from sys import platform

from setup_config import NASSL_SETUP, NASSL_EXT_SETUP
from buildAll_config import OPENSSL_DIR, ZLIB_DIR
from buildAll_unix import OPENSSL_INSTALL_DIR
from buildAll_unix import build
from fetch_deps import fetch_and_extract_deps

extra_compile_args = ['-Wall', '-Wno-deprecated-declarations']

if platform == 'darwin': # Workaround for Clang 3.4
    # add as the element of an array rather than a string, py 2.7.5 
    extra_compile_args += ['-Wno-error=unused-command-line-argument-hard-error-in-future']


# Add arguments specific to Unix builds
unix_ext_args = NASSL_EXT_SETUP.copy()
unix_ext_args.update({
    'include_dirs' : [OPENSSL_INSTALL_DIR + '/include'],
    'extra_compile_args' : extra_compile_args,
    'library_dirs' : [OPENSSL_DIR, ZLIB_DIR],
    'libraries' : ['ssl', 'crypto']})


unix_setup = NASSL_SETUP.copy()
unix_setup.update({
    'ext_modules' : [Extension(**unix_ext_args)] })

if __name__ == '__main__':
    fetch_and_extract_deps()
    build()
    setup(**unix_setup)
