# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Dunder setitem & delitem of VarDict1D & VarDictND."""

import pytest

from docplex_extensions import IndexSet1D, IndexSetND, add_variables

test_cases = [(IndexSet1D(['A', 'B', 'C']), 'A'), (IndexSetND(range(2), range(2)), (0, 0))]


@pytest.mark.parametrize('indexset, key', test_cases)
def test_vardict_setitem_err(mdl_1, indexset, key):
    v = add_variables(mdl_1, indexset, 'C', name='VAL')
    with pytest.raises(AttributeError):
        v[key] = 1


@pytest.mark.parametrize('indexset, key', test_cases)
def test_vardict_delitem_err(mdl_1, indexset, key):
    v = add_variables(mdl_1, indexset, 'C', name='VAL')
    with pytest.raises(AttributeError):
        del v[key]
