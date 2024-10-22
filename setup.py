
from setuptools import find_packages
from distutils.core import setup


with open('requirements.txt') as of:
    install_requires = of.readlines()

setup(
    name='mail-rule-engine',
    version='0.1.0',
    author='Srinivas Adavi',
    author_email='srinivas.adavi@gmail.com',
    description=('Performs some rule based operations on emails'
                  'Using smart-mail-manager and smart-mail-router.'),
    packages=find_packages(),
    namespace_packages=['mre'],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=True,
)
