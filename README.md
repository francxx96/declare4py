# Declare4Py

Declare4PY is a novel and easy-to-use Python package that covers the main tasks of process mining based on the 
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

## Tutorials
The `tutorials/` folder contains a walk-through of Declare4Py. In order, the tutorials cover the following topics:

- [Log analysis](https://github.com/francxx96/declare4py/blob/main/tutorials/log_analysis.ipynb): simple functions to extract useful information from logs;
- [Model checking](https://github.com/francxx96/declare4py/blob/main/tutorials/conformance_checking.ipynb): check what are the traces that satisfy a given DECLARE model;
- [Model Discovery](https://github.com/francxx96/declare4py/blob/main/tutorials/model_discovery.ipynb): discover what are the most satisfied DECLARE constraints in a given log;
- [Query Checking](https://github.com/francxx96/declare4py/blob/main/tutorials/query_checking.ipynb): discover what are the activities that make an input DECLARE constraint satisfied in a given log.

The tutorials are Jupyter notebooks and consider the [Sepsis cases log](https://data.4tu.nl/articles/dataset/Sepsis_Cases_-_Event_Log/12707639).

## Repository Structure
- `src/api/` -- core system containing the main Declare4Py functions.
- `src/constraint_checkers/` -- the implementation of the checkers of the DECLARE constraints.
- `src/models/` -- data models supporting the data structures for Declare4Py.
- `test/` -- a collection of tests for computing the Declare4Py performance;
- `tutorials/` -- tutorials to start with Declare4Py,

## Citing Declare4Py
If you use Declare4Py in your research, please use the following BibTeX entry.

```
@inproceedings{dfmMaking2022,
  author    = {Chiara Di Francescomarino and Ivan Donadello and Chiara Ghidini and Fabrizio Maria Maggi and Williams Rizzi},
  title     = {Making sense of temporal data: the {DECLARE} encoding},
  booktitle = {PMAI@IJCAI},
  series    = {{CEUR} Workshop Proceedings},
  volume    = {},
  pages     = {},
  publisher = {CEUR-WS.org},
  year      = {2022}
}
```
