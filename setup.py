import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-privacyidea-auth',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Authenticate against a privacyIDEA server. (https://www.privacyidea.org/)',
    long_description=README,
    url='https://www.tek2b.de/',
    author='Jens Weber',
    author_email='jweber@tek2b.de',
    install_requires=['Django', 'requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Topic :: Internet',
	'Topic :: Security',
	'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: Software Development :: Libraries',
    ],
)
