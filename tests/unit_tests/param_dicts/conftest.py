# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures and functionality for testing parameter functionality."""

import pytest

from docplex_extensions import ParamDict1D, ParamDictND


@pytest.fixture
def paramdict1d_emp():
    return ParamDict1D()


@pytest.fixture
def paramdict1d_pop2():
    return ParamDict1D({'A': 0, 'B': 1})


@pytest.fixture
def paramdict1d_pop3():
    return ParamDict1D({'A': 0, 'B': 1, 'C': 2})


@pytest.fixture
def paramdictNd_emp():
    return ParamDictND()


@pytest.fixture
def paramdictNd_pop2():
    return ParamDictND({('A', 'B'): 0, ('C', 'D'): 1})


@pytest.fixture
def paramdictNd_pop3():
    return ParamDictND({('A', 'B'): 0, ('C', 'D'): 1, ('E', 'F'): 2})