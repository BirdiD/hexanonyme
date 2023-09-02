from setuptools import setup, find_packages

setup(
    name='hexanonyme', 
    version='1.0.0',  
    description='A Python package for PII data anonymization',
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