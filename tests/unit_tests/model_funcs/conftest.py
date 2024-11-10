# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Common fixtures for testing model functionality."""

import re

import pytest
from docplex.mp.model import Model


def regex_trim(input: str) -> str:
    return re.sub(r'\s+', '', input)


@pytest.fixture()
def mdl():
    mdl = Model()
    yield mdl
    mdl.end()


@pytest.fixture()
def expected_log_start():
    text = '\n'.join(
        [
            '------------------------------  LP problem statistics  ------------------------------',
            '',
            'Problem name         : %s',
            'Objective sense      : Minimize',
            'Variables            :       0',
            'Objective nonzeros   :       0',
            'Linear constraints   :       0',
            '  Nonzeros           :       0',
            '  RHS nonzeros       :       0',
            '',
            'Variables            : Min LB: all infinite     Max UB: all infinite   ',
            'Objective nonzeros   : Min   : all zero         Max   : all zero       ',
            'Linear constraints   :',
            '  Nonzeros           : Min   : all zero         Max   : all zero       ',
            '  RHS nonzeros       : Min   : all zero         Max   : all zero       ',
            '',
            '-------------------------------  CPLEX optimizer log  -------------------------------',
            '',
        ]
    )
    return text


@pytest.fixture()
def expected_log_end():
    text = '\n'.join(
        [
            '---------------------------  Solution quality statistics  ---------------------------',
            '',
            'There are no bound infeasibilities.',
            'There are no reduced-cost infeasibilities.',
            'Maximum Ax-b residual              = 0',
            "Maximum c-B'pi residual            = 0",
            'Maximum |x|                        = 0',
            'Maximum |pi|                       = 0',
            'Maximum |red-cost|                 = 0',
            'Condition number of unscaled basis = 0.0e+00',
            '',
            '-------------------------------------------------------------------------------------',
            '',
        ]
    )
    return text
