from distutils.core import setup
import sys, os

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='pycord',
    packages=['pycord', 'pycord.utils', 'pycord.models', 'pycord.api'],  # this must be the same as the name above
    version='v0.3.6-alpha',
    description='A Discord API library for Python running on the Trio and Curio async libraries',
    author='verixx, king1600, fourjr, henry232323',
    url='https://github.com/henry232323/pycord',  # use the URL to the github repo
    keywords=['discord'],  # arbitrary keywords
    classifiers=[],
    install_requires=load_requirements("requirements.txt")
)
