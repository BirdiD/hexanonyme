from setuptools import setup, find_packages

from codecs import open
from os import path

current_path = path.abspath(path.dirname(__file__))

with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hexanonyme', 
    version='0.1.1',  
    description='A Python package for PII data anonymization',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author='Dioula DOUCOURE',
    author_email='diioula.doucoure@gmail.com',
    url='https://github.com/BirdiD/hexanonyme',
    packages=find_packages(),
    install_requires=[
        'transformers>=4.32.1', 
        'sentencepiece>=0.1.99',
        'faker>=19.3.1', 
        'torch>=2.0.1',

    ],
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)