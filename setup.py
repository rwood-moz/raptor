import os

from setuptools import setup

here = os.path.dirname(os.path.abspath(__file__))
description = 'Browser performance test framework prototype'
version = "0.0"

with open(os.path.join(here, "requirements.txt")) as f:
    dependencies = f.read().splitlines()

setup(name='raptor',
      version=version,
      description=description,
      url='https://github.com/rwood-moz/raptor',
      author='Mozilla',
      author_email='tools@lists.mozilla.org',
      license='MPL',
      packages=['raptor'],
      zip_safe=False,
      install_requires=dependencies,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      raptor = raptor.raptor:main
      """)
