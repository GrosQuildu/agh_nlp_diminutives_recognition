#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='rozpoznawaczek',
    version='1.0',
    packages=find_packages(),
    description='Tool for recognizing polish diminutives',
    url='https://github.com/GrosQuildu/agh_nlp_diminutives_recognition',
    author='Izabela Stechnij, Dominik Sepioło, Paweł Płatek',
    author_email='e2.8a.95@gmail.com',
    # install_requires=['morfeusz2'],  # see http://morfeusz.sgjp.pl/download/
    extras_require={
        'DEV': ['isort', 'mypy', 'pyflakes', 'autopep8', 'pytest', 'pyinstaller'],
        'DOCX': ['python-docx']
    },
    entry_points={
        'console_scripts': [
            'rozpoznawaczek = rozpoznawaczek.rozpoznawaczek:main',
            'rozpoznawaczek-docx = rozpoznawaczek.docx_highlight:main'
        ]
    }
)