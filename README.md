## About

The aim of UMLARS Translator project is to enable simple interaction with UML diagrams using Python code.
It allows manual translation between various XMI or JSON formats of UML model representation and modification using Python methods.

Reads XMI files data using built-in xml package and builds from them internal OOP representation of MOF-based objects.
Currently supports Enterprise Architect XMI 2.1, Eclipse Papyrus XMI 2.1 and StarUML MDJ. Compliant with OMG specification.

The main motivation behind this project is to provide a unification framework between various incosistent formats implemented by MDE tools vendors.
It offers a convinient way to modify UML Diagrams using scripts written in
high-level programming languages rather than manually interact with them using graphical editors.

## Requirements

Python 3.10+

## Installation

pip install umlars_translator

## Dev Usage

- **make setup**: installs all dependencies
- **make test**: runs pytest tests
- **make tox-test**: runs tox tests
- **make docs**: serves documentation at localhost
- **make docs-build**: builds docs
- **make export**: exports dependencies to requirements.txt
- **make publish**: - publishes the package to PyPI
- **make publish-test**: - publishes the package to Test PyPI
- **make clean**: - cleans working directory

## Informations

Published as Python package to test PyPi.
Documented using mkdocs.
Tested on multiple Python versions using tox.

## Deployment as microservice

Setup:
1. Install docker

To start:
1. Run **docker compose build**
2. Run **docker compose up**

To restart:
1. Run **docker compose down --volumes**
2. Run **docker compose up**



## License

This project is licensed under the terms of the MIT license.
