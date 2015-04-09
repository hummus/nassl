import setuptools
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from distutils.command.build import build as _build
from distutils.core import setup, Extension
from sys import platform

from setup_config import NASSL_SETUP, NASSL_EXT_SETUP
from buildAll_config import OPENSSL_DIR, ZLIB_DIR
from buildAll_unix import OPENSSL_INSTALL_DIR
from buildAll_unix import build_deps as _build_deps
from fetch_deps import fetch_and_extract_deps

extra_compile_args = ['-Wall', '-Wno-deprecated-declarations']

if platform == 'darwin': # Workaround for Clang 3.4
    # add as the element of an array rather than a string, py 2.7.5 
    extra_compile_args += ['-Wno-error=unused-command-line-argument-hard-error-in-future']


class bdist_egg(_bdist_egg):
    def run(self):
        self.run_command('build_deps')
        _bdist_egg.run(self)


class build_deps(setuptools.Command):
    description = 'build statically linked deps'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        fetch_and_extract_deps()
        _build_deps()


class build(_build):
    sub_commands = [('build_deps', None)] + _build.sub_commands


# Add arguments specific to Unix builds
unix_ext_args = NASSL_EXT_SETUP.copy()
unix_ext_args.update({
    'include_dirs' : [OPENSSL_INSTALL_DIR + '/include'],
    'extra_compile_args' : extra_compile_args,
    'library_dirs' : [OPENSSL_DIR, ZLIB_DIR],
    'libraries' : ['ssl', 'z', 'crypto']})


unix_setup = NASSL_SETUP.copy()
unix_setup.update({
    'ext_modules' : [Extension(**unix_ext_args)],
    'cmdclass' : {
        'bdist_egg': bdist_egg,
        'build': build,
        'build_deps': build_deps,
    },
    'test_suite': "nassl.tests.as_test_suite"
})


if __name__ == '__main__':
    setuptools.setup(**unix_setup)

