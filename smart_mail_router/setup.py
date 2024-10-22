
from setuptools import find_packages
from distutils.core import setup


with open('requirements.txt') as of:
    install_requires = of.readlines()

setup(
    name='smart-mail-router',
    version='0.1.0',
    author='Srinivas Adavi',
    author_email='srinivas.adavi@gmail.com',
    description=('Integrate with Email API(like GMail) using EmailProvider and'
                 'perform rule based operations on emails using RuleExecutor.'),
    packages=find_packages(),
    namespace_packages=['smr'],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=True,
)
