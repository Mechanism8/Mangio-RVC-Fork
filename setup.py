from setuptools import setup, find_packages

with open("requirements.txt", 'r') as f:
    requirements = f.read().splitlines()

setup(name='mangio-rvc',
      version='0.1.0',
      description='Installable package of Mangio RVC fork modified for external usage',
      author='Cole Mangio',
      packages=find_packages(),
      install_requires=requirements,
      package_data={
        'lib.uvr5_pack.lib_v5.modelparams': ['*.json']
        } 
      )

