""" Setup for memphis.view package """
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='1.0dev'


setup(name='memphis.view',
      version=version,
      description="A package implementing advanced Page Template patterns.",
      long_description=(
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('memphis', 'view', 'README.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Repoze Public License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI'],
      author='Nikolay Kim',
      author_email='fafhrd91@gmail.com',
      url='http://pypi.python.org/pypi/memphis.view/',
      license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
      packages=find_packages(),
      namespace_packages=['memphis'],
      install_requires = ['setuptools',
                          'chameleon',
                          'pyramid',
                          'pyinotify',
                          'pytz',
                          'simplejson',
                          'webob',
                          'memphis.config',
                          'zope.component',
                          'zope.interface',
                          ],
      include_package_data = True,
      zip_safe = False,
      entry_points = {
        'memphis': ['package = memphis.view'],
        'paste.global_paster_command': [
            'static = memphis.view.commands:StaticCommand',
            'templates = memphis.view.commands:TemplatesCommand',
            ],
        },
      )
