# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
Example: The multicommodity transportation problem

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-book/multmip1.ipynb
"""

import pandas as pd
from docplex.mp.model import Model

import docplex_extensions as dex


def test_multicommodity():
    ##### Input data
    # Units of prodcuts available at origins
    df_supply = (
        pd.DataFrame(
            {
                'CLEV': {'bands': 700, 'coils': 1600, 'plate': 300},
                'GARY': {'bands': 400, 'coils': 800, 'plate': 200},
                'PITT': {'bands': 800, 'coils': 1800, 'plate': 300},
            }
        )
        .rename_axis('PROD', axis=0)
        .rename_axis('ORI', axis=1)
        .transpose()
    )

    # Units of prodcuts required at destinations
    df_demand = (
        pd.DataFrame(
            {
                'DET': {'bands': 300, 'coils': 750, 'plate': 100},
                'FRA': {'bands': 300, 'coils': 500, 'plate': 100},
                'FRE': {'bands': 225, 'coils': 850, 'plate': 100},
                'LAF': {'bands': 250, 'coils': 500, 'plate': 250},
                'LAN': {'bands': 100, 'coils': 400, 'plate': 0},
                'STL': {'bands': 650, 'coils': 950, 'plate': 200},
                'WIN': {'bands': 75, 'coils': 250, 'plate': 50},
            }
        )
        .rename_axis('PROD', axis=0)
        .rename_axis('DES', axis=1)
        .transpose()
    )

    # Variable cost of shipping a product from an origin to a destination
    df_vcost = (
        pd.DataFrame(
            {
                ('CLEV', 'DET'): {'bands': 7, 'coils': 9, 'plate': 9},
                ('CLEV', 'FRA'): {'bands': 22, 'coils': 27, 'plate': 29},
                ('CLEV', 'FRE'): {'bands': 82, 'coils': 95, 'plate': 99},
                ('CLEV', 'LAF'): {'bands': 13, 'coils': 17, 'plate': 18},
                ('CLEV', 'LAN'): {'bands': 10, 'coils': 12, 'plate': 13},
                ('CLEV', 'STL'): {'bands': 21, 'coils': 26, 'plate': 28},
                ('CLEV', 'WIN'): {'bands': 7, 'coils': 9, 'plate': 9},
                ('GARY', 'DET'): {'bands': 10, 'coils': 14, 'plate': 15},
                ('GARY', 'FRA'): {'bands': 30, 'coils': 39, 'plate': 41},
                ('GARY', 'FRE'): {'bands': 71, 'coils': 82, 'plate': 86},
                ('GARY', 'LAF'): {'bands': 6, 'coils': 8, 'plate': 8},
                ('GARY', 'LAN'): {'bands': 8, 'coils': 11, 'plate': 12},
                ('GARY', 'STL'): {'bands': 11, 'coils': 16, 'plate': 17},
                ('GARY', 'WIN'): {'bands': 10, 'coils': 14, 'plate': 16},
                ('PITT', 'DET'): {'bands': 11, 'coils': 14, 'plate': 14},
                ('PITT', 'FRA'): {'bands': 19, 'coils': 24, 'plate': 26},
                ('PITT', 'FRE'): {'bands': 83, 'coils': 99, 'plate': 104},
                ('PITT', 'LAF'): {'bands': 15, 'coils': 20, 'plate': 20},
                ('PITT', 'LAN'): {'bands': 12, 'coils': 17, 'plate': 17},
                ('PITT', 'STL'): {'bands': 25, 'coils': 28, 'plate': 31},
                ('PITT', 'WIN'): {'bands': 10, 'coils': 13, 'plate': 13},
            }
        )
        .rename_axis('PROD', axis=0)
        .rename_axis(['ORI', 'DES'], axis=1)
        .transpose()
    )

    # Fixed cost of shipping from an origin to a destination
    df_fcost = (
        pd.DataFrame(
            {
                'DET': {'CLEV': 1000, 'GARY': 1200, 'PITT': 1200},
                'FRA': {'CLEV': 2000, 'GARY': 3000, 'PITT': 2000},
                'FRE': {'CLEV': 3000, 'GARY': 3500, 'PITT': 3500},
                'LAF': {'CLEV': 2200, 'GARY': 2500, 'PITT': 2200},
                'LAN': {'CLEV': 1500, 'GARY': 1200, 'PITT': 1500},
                'STL': {'CLEV': 2500, 'GARY': 2500, 'PITT': 2500},
                'WIN': {'CLEV': 1200, 'GARY': 1200, 'PITT': 1500},
            }
        )
        .rename_axis('ORI', axis=0)
        .rename_axis('DEST', axis=1)
    )

    ##### Index-sets

    ORIG = df_supply.index.dex.to_indexset()
    DEST = df_demand.index.dex.to_indexset()
    PROD = df_supply.columns.dex.to_indexset()

    ##### Parameters

    supply = df_supply.stack().dex.to_paramdict()
    demand = df_demand.stack().dex.to_paramdict()
    vcost = df_vcost.stack().dex.to_paramdict()
    fcost = df_fcost.stack().dex.to_paramdict()

    # Limit on shipping total units of products from an origin to a destination
    limit = 625

    ##### Instantiate

    model = Model(name='multicommodity')

    ##### Add decision variables

    # Units of product to ship from an origin to a destination
    trans = dex.add_variables(
        model,
        indexset=dex.IndexSetND(ORIG, DEST, PROD, names=('ORIG', 'DEST', 'PROD')),
        var_type='continuous',
        name='NUM-UNITS',
    )

    # Whether to ship from an origin to a destination
    use = dex.add_variables(
        model,
        indexset=dex.IndexSetND(ORIG, DEST, names=('ORIG', 'DEST')),
        var_type='binary',
        name='USE-ROUTE',
    )

    ##### Set objective

    # Minimize the total shipping cost
    model.minimize(
        model.sum(vcost[i, j, p] * trans[i, j, p] for i in ORIG for j in DEST for p in PROD)
        + model.sum(fcost[i, j] * use[i, j] for i in ORIG for j in DEST)
    )

    ##### Add constraints

    # Total units of prodcuts shipped from each origin should be equal to its supply
    model.add_constraints_(
        (trans.sum(i, '*', p) == supply[i, p], f'supply_{i}_{p}') for i in ORIG for p in PROD
    )

    # Total units of prodcuts shipped to each destination should be equal to its demand
    model.add_constraints_(
        (trans.sum('*', j, p) == demand[j, p], f'demand_{j}_{p}') for j in DEST for p in PROD
    )

    # Total units of prodcuts shipped from an origin to a destination is limited
    model.add_constraints_(
        (trans.sum(i, j, '*') <= limit * use[i, j], f'multi_{i}_{j}') for i in ORIG for j in DEST
    )

    ##### Solve

    sol = dex.solve(model)

    sol_str = ''.join(
        [
            f'{var.name}={round(val, 3)}'
            for var, val in sol.as_dict().items()
            if abs(round(val, 3)) > 0
        ]
    )
    assert sol_str == (
        'NUM-UNITS_CLEV_DET_coils=525.0NUM-UNITS_CLEV_DET_plate=100.0NUM-UNITS_CLEV_FRA_bands=225.0NU'
        'M-UNITS_CLEV_FRA_plate=50.0NUM-UNITS_CLEV_LAF_bands=50.0NUM-UNITS_CLEV_LAF_coils=375.0NUM-UN'
        'ITS_CLEV_LAN_coils=350.0NUM-UNITS_CLEV_STL_bands=350.0NUM-UNITS_CLEV_STL_coils=100.0NUM-UNIT'
        'S_CLEV_STL_plate=100.0NUM-UNITS_CLEV_WIN_bands=75.0NUM-UNITS_CLEV_WIN_coils=250.0NUM-UNITS_C'
        'LEV_WIN_plate=50.0NUM-UNITS_GARY_FRE_coils=525.0NUM-UNITS_GARY_FRE_plate=100.0NUM-UNITS_GARY'
        '_LAN_bands=100.0NUM-UNITS_GARY_LAN_coils=50.0NUM-UNITS_GARY_STL_bands=300.0NUM-UNITS_GARY_ST'
        'L_coils=225.0NUM-UNITS_GARY_STL_plate=100.0NUM-UNITS_PITT_DET_bands=300.0NUM-UNITS_PITT_DET_'
        'coils=225.0NUM-UNITS_PITT_FRA_bands=75.0NUM-UNITS_PITT_FRA_coils=500.0NUM-UNITS_PITT_FRA_pla'
        'te=50.0NUM-UNITS_PITT_FRE_bands=225.0NUM-UNITS_PITT_FRE_coils=325.0NUM-UNITS_PITT_LAF_bands='
        '200.0NUM-UNITS_PITT_LAF_coils=125.0NUM-UNITS_PITT_LAF_plate=250.0NUM-UNITS_PITT_STL_coils=62'
        '5.0USE-ROUTE_CLEV_DET=1.0USE-ROUTE_CLEV_FRA=1.0USE-ROUTE_CLEV_LAF=1.0USE-ROUTE_CLEV_LAN=1.0U'
        'SE-ROUTE_CLEV_STL=1.0USE-ROUTE_CLEV_WIN=1.0USE-ROUTE_GARY_FRE=1.0USE-ROUTE_GARY_LAN=1.0USE-R'
        'OUTE_GARY_STL=1.0USE-ROUTE_PITT_DET=1.0USE-ROUTE_PITT_FRA=1.0USE-ROUTE_PITT_FRE=1.0USE-ROUTE'
        '_PITT_LAF=1.0USE-ROUTE_PITT_STL=1.0'
    )
