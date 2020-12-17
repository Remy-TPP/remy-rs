from setuptools import find_packages, setup

setup(
    name='remy_rs',
    packages=find_packages(),
    scripts=['./remy_rs/data/make_dataset.py'],
    version='0.1.0',
    description='Dish recommender',
    author='Remy',
    license='MIT',
)
