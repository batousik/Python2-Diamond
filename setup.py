from setuptools import setup
from codecs import open  # To use a consistent encoding
from os import path
from setuptools.command.test import test as test_command
import sys


class Tox(test_command):
    # user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        test_command.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

here = path.abspath(path.dirname(__file__))
print(here)
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Python2-Diamond',
    description='Diamond board game in Python',
    url='https://github.com/batousik/Python2-Diamond',
    keywords='boardgame diamond python',
    long_description=long_description,
    version='0.1',
    packages=['diamond_game', ],
    install_requires=['tox', 'sphinx', ],
    # tests_require=['tox', ],
    author='130017964, Cheryl, Emil',
    license='MIT',
    cmdclass={'test': Tox},
)

if __name__ == '__main__':
    setup()