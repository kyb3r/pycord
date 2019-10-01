from distutils.core import setup
import sys, os

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='pycord',
    packages=['pycord', 'pycord.utils', 'pycord.models', 'pycord.api'],  # this must be the same as the name above
    version='v0.3.5-alpha',
    description='A Discord API library for Python running on the Trio and Curio async libraries',
    author='verixx, king1600, fourjr, henry232323, JustMaffie',
    author_email='abdurraqeeb53@gmail.com',
    url='https://github.com/verixx/pycord',  # use the URL to the github repo
    download_url='https://github.com/verixx/pycord/archive/v0.3.4-alpha.tar.gz',  # I'll explain this in a second
    keywords=['discord'],  # arbitrary keywords
    classifiers=[],
)
