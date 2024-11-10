# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""VarDict1D & VarDictND constructor and attributes."""

from collections import abc

import pytest

from docplex_extensions import IndexSet1D, IndexSetND, VarDict1D, VarDictND, add_variables


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
def test_vardict_init_typerr0(mdl_1, cls, indexset):
    docpx_vars = mdl_1.continuous_var_dict(indexset)
    with pytest.raises(TypeError):
        cls(docpx_vars, indexset, model=mdl_1)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
@pytest.mark.parametrize('vardict', [0, int, [1, 2], 'A'])
def test_vardict_init_typerr1(mdl_1, cls, indexset, vardict):
    with pytest.raises(TypeError):
        cls._create(vardict, indexset, model=mdl_1)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
def test_vardict_init_valerr1(mdl_1, cls, indexset):
    with pytest.raises(ValueError):
        cls._create({}, indexset, model=mdl_1)


@pytest.mark.parametrize(
    'cls, indexset',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C'])],
        [VarDictND, IndexSetND(range(2), range(2))],
    ],
)
@pytest.mark.parametrize('vardict', [{'A': 0, 'B': 1}, {1: [1, 2], 2: [2, 3]}])
def test_vardict_init_typerr2(mdl_1, cls, indexset, vardict):
    with pytest.raises(TypeError):
        cls._create(vardict, indexset, model=mdl_1)


@pytest.mark.parametrize(
    'cls, indexset, incorrect',
    [
        [VarDict1D, IndexSet1D(['A', 'B', 'C']), IndexSet1D(['A', 'B'])],
        [VarDictND, IndexSetND(range(2), range(2)), IndexSetND(range(1), range(2))],
    ],
)
def test_vardict_init_valerr2(mdl_1, cls, indexset, incorrect):
    v = add_variables(mdl_1, indexset, 'C')
    with pytest.raises(ValueError):
        cls._create(v, incorrect, model=mdl_1)


@pytest.mark.parametrize('name', [None, 'KEY'])
def test_vardict1d_init_keyname_pass(mdl_1, name):
    indexset = IndexSet1D(['A', 'B', 'C'], name=name)
    v = add_variables(mdl_1, indexset, 'C')
    assert v.key_name == name


@pytest.mark.parametrize('input', ['DEF', 'Z'])
def test_vardict1d_init_keyname_update_pass(mdl_1, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = add_variables(mdl_1, indexset, 'C')
    v.key_name = input
    assert v.key_name == input


@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict1d_init_keyname_update_typeerr(mdl_1, input):
    indexset = IndexSet1D(['A', 'B', 'C'], name='KEY')
    v = add_variables(mdl_1, indexset, 'C')
    with pytest.raises(TypeError):
        v.key_name = input


@pytest.mark.parametrize(
    'input, expected',
    [
        [None, None],
        [('KEY1', 'KEY2'), ['KEY1', 'KEY2']],
        [['KEY1', 'KEY2'], ['KEY1', 'KEY2']],
        [('KEY1', 'KEY2', 'KEY3'), ['KEY1', 'KEY2', 'KEY3']],
        # ^ valid because ParamDictND doesn't enforce the names to conform with len of keys
    ],
)
def test_vardictNd_init_keynames_pass(mdl_1, input, expected):
    indexset = IndexSetND(range(2), range(2), names=input)
    v = add_variables(mdl_1, indexset, 'C')
    assert v.key_names == expected


@pytest.mark.parametrize('input', [('C', 'D'), ['A', 'B', 'C']])
def test_vardictNd_init_keynames_update_pass(mdl_1, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = add_variables(mdl_1, indexset, 'C')
    v.key_names = input
    assert v.key_names == list(input)


@pytest.mark.parametrize('input', ['CD', 1, 0.0, int, [1], (1, 'D', 9.0), {'Z', 'Y'}])
def test_vardictNd_init_keynames_update_typeerr(mdl_1, input):
    indexset = IndexSetND(range(2), range(2), names=('KEY1', 'KEY2'))
    v = add_variables(mdl_1, indexset, 'C')
    with pytest.raises(TypeError):
        v.key_names = input


@pytest.mark.parametrize('name', [None, 'VAL'])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_pass(mdl_1, indexset, name):
    v = add_variables(mdl_1, indexset, 'C', name=name)
    assert v.value_name == name


@pytest.mark.parametrize('input', ['DEF', 'Z'])
@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_init_valname_update_pass(mdl_1, indexset, input):
    v = add_variables(mdl_1, indexset, 'C', name='VAL')
    v.value_name = input
    assert v.value_name == input


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
@pytest.mark.parametrize('input', [123, 1.9, ('A', 'B', 'C'), ['A', 'B'], {'ABC'}])
def test_vardict_init_valname_update_typeerr(mdl_1, indexset, input):
    v = add_variables(mdl_1, indexset, 'C', name='VAL')
    with pytest.raises(TypeError):
        v.value_name = input


@pytest.mark.parametrize('indexset', [IndexSet1D(['A', 'B', 'C']), IndexSetND(range(2), range(2))])
def test_vardict_isinstance_dict(mdl_1, indexset):
    v = add_variables(mdl_1, indexset, 'C', name='VAL')

    assert isinstance(v, dict)
    assert isinstance(v, abc.MutableMapping)
