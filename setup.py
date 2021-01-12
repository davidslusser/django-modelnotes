import os
from setuptools import setup, find_packages
import modelnotes

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as readme:
    README = readme.read()


with open('requirements/base.txt') as f:
    required = f.read().splitlines()

version = modelnotes.__version__

setup(
    name='django-modelnotes',
    description='a django application to add notes to models',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    license=modelnotes.__license__,
    author=modelnotes.__author__,
    author_email=modelnotes.__email__,
    url='https://github.com/davidslusser/django-modelnotes',
    download_url='https://github.com/davidslusser/django-modelnotes/archive/{}.tar.gz'.format(version),
    keywords=['django', 'helpers', 'notes', 'model', 'models'],
    install_requires=required,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 2.2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
