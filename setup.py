from setuptools import setup, find_packages

setup(
    name='stadtradeln_data',
    version="0.0.1",
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
    author="Paul Daum",
    author_email="paul.daum@posteo.de",
    description="A python package for downloading bicycle traffic count data from the STADTRADELN database",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
        ]
    },
)