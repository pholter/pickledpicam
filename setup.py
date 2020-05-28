from setuptools import setup
import os

ROOT_DIR='pickledpicam'
with open(os.path.join(ROOT_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pickledpicam',
      version=version,
      description='The pickled Raspberry PI camera used for underwater footage',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='https://github.com/MarineDataTools/pickledpicam',
      author='Peter Holtermann',
      author_email='peter.holtermann@io-warnemuende.de',
      license='GPLv03',
      packages=['pickledpicam'],
      scripts = [],
      entry_points={ 'console_scripts': ['pipicamviewer=pickledpicam.pickledpiviewer_v02:main']},
      package_data = {'':['VERSION']},
      install_requires=[ 'cobs'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
      ],
      python_requires='>=3.5',
      zip_safe=False)
