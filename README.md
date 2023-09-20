# Disclaimer

This versione is no longer supported and updated, please check the new Declare4Py versione [here](https://github.com/ivanDonadello/Declare4Py).

# Declare4Py

Declare4Py is a novel and easy-to-use Python package that covers the main tasks of process mining based on the 
declarative modeling language DECLARE. Some functions include also the MP-DECLARE standard, that is, the 
multi-perspective extension of DECLARE that supports also data constraints. The declare4PY APIs implement simple log analysis, consistency 
checking, model discovery and query checking from logs by considering (MP)-DECLARE models. Declare4Py can be easily 
integrated into your process mining software project.

## Requirements
We tested Declare4Py with the following software configuration. However, more recent versions of the libraries could also work:
- MacOs Big Sur==11.1;
- Python==3.9.7;
- mlxtend==0.20.0;
- Pm4Py==2.2.21;
- Pandas==1.3.4;

## Installation
Declare4Py can be easily installed by following these steps:
1. download the repository;
2. enter into the `dist` folder;
3. run `pip install declare4py-1.0.0.tar.gz`.

## Tutorials
The `tutorials/` folder contains a walk-through of Declare4Py. In order, the tutorials cover the following topics:

- [System overview](https://github.com/francxx96/declare4py/blob/main/tutorials/system_overview.ipynb): an overview of the Python modules (and dependencies) composing Declare4Py;
- [Log analysis](https://github.com/francxx96/declare4py/blob/main/tutorials/log_analysis.ipynb): simple functions to extract useful information from logs;
- [Model checking](https://github.com/francxx96/declare4py/blob/main/tutorials/conformance_checking.ipynb): check what are the traces that satisfy a given DECLARE model;
- [Model Discovery](https://github.com/francxx96/declare4py/blob/main/tutorials/model_discovery.ipynb): discover what are the most satisfied DECLARE constraints in a given log;
- [Query Checking](https://github.com/francxx96/declare4py/blob/main/tutorials/query_checking.ipynb): discover what are the activities that make an input DECLARE constraint satisfied in a given log.

The tutorials are Jupyter notebooks and consider the [Sepsis cases log](https://data.4tu.nl/articles/dataset/Sepsis_Cases_-_Event_Log/12707639).

## Repository Structure
- `src/declare4py/api_functions.py` -- core system containing the main Declare4Py functions.
- `src/declare4py/declare4py.py` -- a wrapper to the main Declare4Py functions containing the main Declare4Py class.
- `src/declare4py/constraint_checkers/` -- the implementation of the checkers of the DECLARE constraints.
- `src/declare4py/models/` -- data models supporting the data structures for Declare4Py.
- `docs/declare4py/index.html` -- documentation for Declare4Py in `html` format.
- `dist` -- built package containing Declare4Py for easing the user with the installation.
- `tests/` -- a collection of tests for computing the Declare4Py performance.
- `tutorials/` -- tutorials to start with Declare4Py,

## Citing Declare4Py
If you use Declare4Py in your research, please use the following BibTeX entry.

```
@inproceedings{DonadelloRMS22,
  author    = {Ivan Donadello and
               Francesco Riva and
               Fabrizio Maria Maggi and
               Aladdin Shikhizada},
  title     = {Declare4Py: {A} Python Library for Declarative Process Mining},
  booktitle = {{BPM} (PhD/Demos)},
  series    = {{CEUR} Workshop Proceedings},
  volume    = {3216},
  pages     = {117--121},
  publisher = {CEUR-WS.org},
  year      = {2022}
}

```
