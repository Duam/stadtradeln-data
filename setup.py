import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='stadtradeln-data',
    version="0.0.2-rc-1",
    setup_requires=['setuptools'],
    use_scm_version=False,
    install_requires=[
        'tqdm',
        'requests',
        'click',
        'pytest',
        'numpy',
        'pandas'
    ],
    python_requires='>=3.6',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    license="MIT",
    url="https://github.com/Duam/stadtradeln-data",
    author="Paul Daum",
    author_email="paul.daum@posteo.de",
    description="A python package for downloading, extracting and clipping bicycle traffic count data "
                "from the STADTRADELN database",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Typing :: Typed"
    ],
    entry_points={
        'console_scripts': [
            'stadtradeln-data-manager = stadtradeln_data_manager.__main__:cli'
        ]
    },
)
