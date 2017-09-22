from distutils.core import setup

setup(
  name = 'py-cord',
  packages = ['pycord', 'pycord.utils', 'pycord.models', 'pycord.api'], # this must be the same as the name above
  version = 'v0.3.4-alpha',
  description = 'An async discord api wrapper',
  author = 'verixx',
  author_email = 'abdurraqeeb53@gmail.com',
  url = 'https://github.com/verixx/pycord', # use the URL to the github repo
  download_url = 'https://github.com/verixx/pycord/archive/v0.3.4-alpha.tar.gz', # I'll explain this in a second
  keywords = ['discord'], # arbitrary keywords
  classifiers = [],
)