
from setuptools import find_packages
from distutils.core import setup


with open('requirements.txt') as of:
    install_requires = of.readlines()

setup(
    name='smart-mail-manager',
    version='0.1.0',
    author='Srinivas Adavi',
    author_email='srinivas.adavi@gmail.com',
    description=('Manager '
                 '- Handles Email API data(i.e payload), DB data(i.e models) '
                 '- Data validation, serialization '
                 '- Rule-based operations'),
    packages=find_packages(),
    namespace_packages=['smm'],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=True,
)
