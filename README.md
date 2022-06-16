# declare4Py

Declare4PY is a novel and easy-to-use Python package that covers the main tasks of process mining based on the 
declarative modeling language DECLARE. Some functions include also the MP-DECLARE standard, that is, the 
multi-perspective extension of DECLARE that supports also data constraints. The declare4PY APIs implement consistency 
checking, model discovery and query checking from logs by considering (MP)-DECLARE models. Declare4Py can be easily 
integrated into your process mining software project.

## Getting Started

### Requirements
We test declare4Py with the following software configuration. However, more recent versions of the libraries could also work:
- Ubuntu==;
- Python==;
- mlxtend==;
- Pm4Py==;
- Pandas==;
- Numpy==;
- Scikit-learn==;
- Matplotlib==;

### Installation

### Tutorials
tutorials/ contains a walk-through of LTN. In order, the tutorials cover the following topics:

    Grounding in LTN part 1: Real Logic, constants, predicates, functions, variables,
    Grounding in LTN part 2: connectives and quantifiers (+ complement: choosing appropriate operators for learning),
    Learning in LTN: using satisfiability of LTN formulas as a training objective,
    Reasoning in LTN: measuring if a formula is the logical consequence of a knowledgebase.

The tutorials are implemented using Jupyter notebooks.

## Repository Structure
- ltn/core.py -- core system for defining constants, variables, predicates, functions and formulas,
- ltn/fuzzy_ops.py -- a collection of fuzzy logic operators defined using Tensorflow primitives,
- tutorials/ -- tutorials to start with LTN,

## Citing declare4Py
If you use declare4Py in your research, please use the following BibTeX entry.

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
