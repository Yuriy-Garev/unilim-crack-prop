from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wcrack',
    version='2019.001a',
    packages=find_packages(),
    url='https://bitbucket.org/Yuriy_Garev/wcrack/',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Yurii Hariev',
    author_email='yuriy.garev@gmail.com',
    description='The package is designed for computations of wood behavior under the stress',
    python_requires='>=3.6, <4',
    install_requires=['numpy', 'getclass', 'seaborn', 'matplotlib'],
    classifiers=[
        # 1 - Planning
        # 2 - Pre-Alpha
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        # 6 - Mature
        # 7 - Inactive
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        'Topic :: Scientific/Engineering :: Mathematics',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
