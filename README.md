# JCPDSTools

[![DOI](https://zenodo.org/badge/247157282.svg)](https://zenodo.org/badge/latestdoi/247157282)

A Python application for creating and editing JCPDS files for PeakPo.

Main features include:

- Convert a CIF to JCPDS  
- Convert a DIOPTAS JCPDS to PeakPo JCPDS  
- Edit existing JCPDS files  
- Check JCPDS files for possible errors  

## Required packages

- `PeakPo`

## How to install

`JCPDSTools` works with `PeakPo`. It is recommended to create a dedicated `conda` environment and install `PeakPo`.

```
conda create -n pkpo793 python=3.11 -y
```

```
conda activate pkpo793
```

```
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple PeakPo==7.9.3
```

Then install `JCPDSTools`.

```
pip install jcpdstools
```

## How to run

```
jcpdstools
```

or

```
python -m jcpdstools
```

## How to download executables (old version)

See [this Google Drive folder](https://drive.google.com/drive/folders/0B0kkQLbYpQDYfjBGT21uMkx5cU1JMHJIUUhGR1FkdDVUdzFYVUdKR0Zya2NRcFYtUmRVUGM?resourcekey=0-FT-Lc6ZeuUBMaqHzzjZSbg&usp=sharing).


## Where to get CIF files

CIF files for a wide range of materials can be downloaded from online databases such as:

- [American Mineralogist Crystal Structure Database](http://rruff.geo.arizona.edu/AMS/amcsd.php)  
- [Materials Project](https://materialsproject.org)  
- [Crystallography Open Database](http://www.crystallography.net/cod/index.php)  
- [Crystallographic and Crystallochemical Database for Minerals and their Structural Analogues](http://database.iem.ac.ru/mincryst/index.php)  

The website below is useful if you have an unknown phase:

- [Crystal lattice - Structures](https://homepage.univie.ac.at/michael.leitner/lattice/index.html)

## How to cite

S.-H. Shim (2022). *JCPDSTools: A Python app for creating, converting, and revising high-pressure diffraction information files*. Zenodo. https://doi.org/10.5281/zenodo.6349449
