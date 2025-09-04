# Non-intrusive Load Disaggregation based on Digital Signal Processing for Microcontroller Application
Manuscript ID: IEEE LATAM submission ID 9595

Autors: 
Maximiliano E. Véliz 
Alejandro D. Otero 

# Reproducibility Repository

## Overview
This repository provides the necessary material to reproduce the results presented in the referenced paper.  
It includes **four Jupyter Notebooks** and **four CSV datasets**, which contain the data and code used in the experiments.

## Contents
- `notebooks/`  
  Four Jupyter Notebook files with the step-by-step implementation of the methodology:

    1- _alpha,_beta_coefficients_in_DS1_pynb
  
    2-  _alpha,_beta_in_DS2.pynb
  
    3-  _alpha,_beta_in_DS3.pynb
  
    4-  _alpha,_beta_in_DS4.pynb

- `datasets/`  
  The datasets used in this repository are provided in the compressed file Stasets.rar.
  This archive contains four folders: DS1, DS2, DS3, and DS4.
  Each folder includes a collection of CSV files that are associated with the corresponding experiments and analyses presented in the notebooks.


## Requirements

The programs in this repository are written in Python and provided as Jupyter Notebooks.  
You can run them in one of the following ways:

1. **Local execution**
   - Install [Python 3.x](https://www.python.org/downloads/).
   - Install Jupyter Notebook or JupyterLab:
     ```bash
     pip install notebook
     ```
   - Launch the notebook with:
     ```bash
     jupyter notebook
     ```

2. **Execution in Google Colab**
   - No installation required.
   - Only a Google account is needed.
   - Each notebook can be opened directly in Colab using the following badge:

  Colab: https://colab.research.google.com/

## Data files

Each Python notebook requires specifying the directory path of the corresponding dataset folder in order to properly load the associated CSV files.

For example, the notebook alpha_beta_coefficients_in_DS1.ipynb requires providing the path to the DS1 folder, where the relevant dataset files are located.

This ensures that every notebook is correctly linked to the dataset it is designed to process.




## Contact
For questions or replication of results:  
mveliz@campus.ungs.edu.ar or alejandro.otero@csc.conicet.gov.ar



