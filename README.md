# JCPDSTools

[![DOI](https://zenodo.org/badge/247157282.svg)](https://zenodo.org/badge/latestdoi/247157282)

A python application for creating and editing JCPDS files for PeakPo.

Major functions include:

- Convert a CIF to JCPDS  
- Convert a DIOPTAS JCPDS to PeakPo JCPDS  
- Edit existing JCPDS  
- Examine possible errors on JCPDS  

## Required packages

`pymatgen` version 2019.4.11 or later.  

## How to install

```
mkdir JCPDSTools
cd JCPDSTools
git clone https://github.com/SHDShim/JCPDSTools.git .
```

## How to run

```
cd JCPDSTools/JCPDSTools
python -m jcpdstools
```

## How to download executables

Check [my google drive folder](https://drive.google.com/drive/folders/0B0kkQLbYpQDYfjBGT21uMkx5cU1JMHJIUUhGR1FkdDVUdzFYVUdKR0Zya2NRcFYtUmRVUGM?resourcekey=0-FT-Lc6ZeuUBMaqHzzjZSbg&usp=sharing)


## Where to get CIF files

CIF files for a wide range of materials can be downloaded from web databases, such as:

- [American Mineralogist Crystal Structure Database](http://rruff.geo.arizona.edu/AMS/amcsd.php)  
- [Materials Project](https://materialsproject.org)  
- [Crystallography Open Database](http://www.crystallography.net/cod/index.php)  
- [Crystallographic and Crystallochemical Database for Minerals and their Structural Analogues](http://database.iem.ac.ru/mincryst/index.php)  

The website below is useful if you have unknown phase.

- [Crystal lattice - Structures](https://homepage.univie.ac.at/michael.leitner/lattice/index.html)

## How to cite

S.-H. Shim (2022) JCPDSTools - A python app for creating, converting, and revising high-pressure diffraction information file. Zenodo. https://doi.org/10.5281/zenodo.6349449
