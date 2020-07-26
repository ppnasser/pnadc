========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/pnadc/badge/?style=flat
    :target: https://readthedocs.org/projects/pnadc
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/ppnasser/pnadc.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ppnasser/pnadc

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ppnasser/pnadc?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ppnasser/pnadc

.. |requires| image:: https://requires.io/github/ppnasser/pnadc/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ppnasser/pnadc/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/ppnasser/pnadc/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ppnasser/pnadc

.. |version| image:: https://img.shields.io/pypi/v/pnadc.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pnadc

.. |wheel| image:: https://img.shields.io/pypi/wheel/pnadc.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pnadc

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pnadc.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pnadc

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pnadc.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pnadc

.. |commits-since| image:: https://img.shields.io/github/commits-since/ppnasser/pnadc/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/ppnasser/pnadc/compare/v0.0.0...master



.. end-badges

A python package to deal with IBGE-PNADc database.

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

::

    pip install pnadc

You can also install the in-development version with::

    pip install https://github.com/ppnasser/pnadc/archive/master.zip


Documentation
=============


https://pnadc.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
