# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures and functionality for testing variable functionality."""

import pytest
from docplex.mp.model import Model


@pytest.fixture(scope='module')
def mdl_1():
    mdl_1 = Model(ignore_names=True)
    yield mdl_1
    mdl_1.end()


@pytest.fixture(scope='module')
def mdl_2():
    mdl_2 = Model(ignore_names=True)
    yield mdl_2
    mdl_2.end()
