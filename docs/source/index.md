% HALO-DROPS documentation master file, created by
% sphinx-quickstart on Tue Feb 14 01:00:50 2023.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

```{warning}
Currently under active development! We can help from your contributions. Please check out our {doc}`Contributing Guide <CONTRIBUTING>`.
```
# Overview

HALO-DROPS stands for **HALO DROpsonde Protocol & Software**

This package documents and enables a uniform workflow for the [HALO aircraft](https://halo-research.de)'s dropsondes operations and data. Although in some sense obvious, the {ref}`motivation to build this package <need-for-halo-drops>` is essentially to have consistency across campaigns in how dropsonde measurements are collected and how their data are processed and distributed. The objective of HALO-DROPS is to therefore create a holistic dropsonde protocol for:

- **OPERATIONS**: making them uniform across HALO experiments
- **DATA**: their collection, processing and distribution

-----

Keeping these objectives in mind, HALO-DROPS has two elements at its core:

1. {doc}`Operations <operations/index>`

The handbook serves as a document outlining the steps for dropsondes' routine operations, known issues and troubleshooting as well as for handling data such as the recommended data structure.

2. {doc}`Software <apidocs/index>`

The software contains the source code needed for data handling. It is written in the Python programming language and includes scripts for the quality check and quality control of data, processing the data and generating data products.

-----

Of course, what good is it to create software, but not document how to use it? Therefore, there are Jupyter notebooks available as {doc}`How-To Guides <howto/index>`, which explain how to perform routine steps in quality control and processing. Moreover, the rationale behind some important aspects of operations and data are also documented in a section titled {doc}`Explanations <explanation/index>`.

(need-for-halo-drops)=
## Need for a uniform HALO dropsondes protocol

Soundings do not have a better substitute for recording atmospheric profiles, particularly for wind measurements and for measurements in cloudy skies. For this reason, HALO dropsondes are part of the core components for several campaign configurations, such as the <a href="https://www.halo.dlr.de/science/missions/narval2/narval2.html" target="_blank">NARVAL experiments</a>, <a href="http://www.pa.op.dlr.de/nawdex/" target="_blank">NAWDEX</a>, <a href="https://eurec4a.eu/" target="_blank">EUREC$^4$A</a>, <a href="https://halo-ac3.de/" target="_blank">HALO-(AC)$^3$</a>, etc. Despite their usefulness and consistent deployment, there is a lack of uniformity in their operations and data handling across different campaigns.

Currently, every HALO campaign has its own strategy for dealing with operations, collection, quality control, processing and distribution of dropsondes’ data. This ends up in a lot of redundancy in decision-making and is prone to errors. Moreover, comparing dropsondes among different campaigns becomes cumbersome because of the non-uniformity in data structure. These differences can be resolved by developing a uniform protocol across HALO campaigns and an accompanying software package that makes it easy to standardize data handling of HALO dropsondes, also applicable retroactively to past campaigns’ data. This package aims to build such a protocol, called **HALO DROpsonde Protocol & Software (HALO-DROPS)**.

For a quick start to using `halodrops`, go to {doc}`Getting Started <tutorial/index>`.

```{toctree}
:caption: 'Contents:'
:maxdepth: 1

CONTRIBUTING.md
tutorial/index
explanation/index
data/index
operations/index
howto/index
apidocs/index
```
