"""
=====================================
Multicommodity transportation problem
=====================================

Please refer to chapters 4 & 20 in the `AMPL Book <https://ampl.com/learn/ampl-book>`_
for a detailed description of the problem. We will illustrate how to implement this model
with DOcplex using the `docplex-extensions` library.

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-book/multmip1.ipynb
— Copyright (c) 2022-2022, AMPL Optimization inc. (licensed under the MIT License)
"""

# %%
# Ensure DOcplex and its required dependecies are installed correctly
# -------------------------------------------------------------------

from docplex.mp.check_list import run_docplex_check_list

run_docplex_check_list()

# %%
# Import DOcplex, docplex-extensions, and pandas
# ----------------------------------------------

import pandas as pd
from docplex.mp.model import Model

import docplex_extensions as dex

# %%
# Input data
# ----------

# %%

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

print(df_supply)

# %%

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

print(df_demand)

# %%

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

print(df_vcost)

# %%

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

print(df_fcost)

# %%
# Set up problem data
# -------------------

# %%
# Index-sets
# ^^^^^^^^^^
#
# .. math::
#
#    \begin{align*}
#    i &\in ORIG: && \text{Origins to ship products from} \\
#    j &\in DEST: && \text{Destinations to ship products to} \\
#    p &\in PROD: && \text{Products to be shipped} \\
#    \end{align*}
#

ORIG = df_supply.index.dex.to_indexset()

DEST = df_demand.index.dex.to_indexset()

PROD = df_supply.columns.dex.to_indexset()

# %%
# Parameters
# ^^^^^^^^^^
#
# .. math::
#
#    \begin{align*}
#    supply_{i, p} &\in \mathbb{R}_{0}^{+}: && \text{Units of prodcut $p$ available at origin $i$},
#     \; \forall \; i \in ORIG \; \text{and} \; p \in PROD \\
#    demand_{j, p} &\in \mathbb{R}_{0}^{+}: && \text{Units of prodcut $p$ required at destination
#     $j$}, \; \forall \; j \in DEST \; \text{and} \; p \in PROD \\
#    vcost_{i, j, p} &\in \mathbb{R}_{0}^{+}: && \text{Variable cost of shipping product $p$ from
#     origin $i$ to destination $j$}, \; \forall \; i \in ORIG \; \text{and} \; j \in DEST \;
#     \text{and} \; p \in PROD \\
#    fcost_{i, j} &\in \mathbb{R}_{0}^{+}: && \text{Fixed cost of shipping from origin $i$ to
#     destination $j$}, \; \forall \; i \in ORIG \; \text{and} \; j \in DEST \\
#    limit &\in \mathbb{R}_{0}^{+}: && \text{Limit on shipping total units of products from any
#     origin to any destination} \\
#    \end{align*}
#

supply = df_supply.stack().dex.to_paramdict()

demand = df_demand.stack().dex.to_paramdict()

vcost = df_vcost.stack().dex.to_paramdict()

fcost = df_fcost.stack().dex.to_paramdict()

limit = 625

# %%
# Set up model
# ------------

# %%
# Instantiate
# ^^^^^^^^^^^

model = Model(name='multicommodity')

# %%
# Add decision variables
# ^^^^^^^^^^^^^^^^^^^^^^
#
# .. math::
#
#    \begin{align*}
#    trans_{i, j, p} &\in \mathbb{R}_{0}^{+}: && \text{Units of prodcut $p$ to ship from origin $i$
#     to destination $j$}, \; \forall \; i \in ORIG \; \text{and} \; j \in DEST \; \text{and} \;
#     p \in PROD \\
#    use_{i, j} &\in \mathbb{B}: && \text{Whether to ship from origin $i$ to destination $j$}, \;
#     \forall \; i \in ORIG \; \text{and} \; j \in DEST \\
#    \end{align*}
#

trans = dex.add_variables(
    model,
    indexset=dex.IndexSetND(ORIG, DEST, PROD, names=('ORIG', 'DEST', 'PROD')),
    var_type='continuous',
    name='NUM-UNITS',
)

use = dex.add_variables(
    model,
    indexset=dex.IndexSetND(ORIG, DEST, names=('ORIG', 'DEST')),
    var_type='binary',
    name='USE-ROUTE',
)

# %%
# Set objective
# ^^^^^^^^^^^^^
#
# .. math::
#
#    \begin{align*}
#    &\text{Minimize the total shipping cost:} \\
#    &\text{min.} \; \sum_{i \in ORIG} \sum_{j \in DEST} \sum_{p \in PROD} vcost_{i, j, p} \times
#     trans_{i, j, p} + \sum_{i \in ORIG} \sum_{j \in DEST} fcost_{i, j} \times use_{i, j} \\
#    \end{align*}
#

# fmt: off
model.minimize(
    model.sum(
        vcost[i, j, p] * trans[i, j, p]
        for i in ORIG
        for j in DEST
        for p in PROD
    )
    + model.sum(
        fcost[i, j] * use[i, j]
        for i in ORIG
        for j in DEST
    )
)
# fmt: on

# %%
# Add constraints
# ^^^^^^^^^^^^^^^
#
# .. math::
#
#    \begin{align*}
#    &\text{Total units of prodcut $p$ shipped from origin $i$ should be equal to its supply:} \\
#    & \sum_{j \in DEST} trans_{i, j, p} = supply_{i, p}, \; \forall \; i \in ORIG \; \text{and} \;
#     p \in PROD \\
#    &\text{Total units of prodcut $p$ shipped to destination $j$ should be equal to its demand:} \\
#    & \sum_{i \in ORIG} trans_{i, j, p} = demand_{j, p}, \; \forall \; j \in DEST \; \text{and} \;
#     p \in PROD \\
#    &\text{Total units of prodcuts shipped from origin $i$ to destination $j$ is limited:} \\
#    & \sum_{p \in PROD} trans_{i, j, p} \leq limit, \; \forall \; i \in ORIG \; \text{and} \; j
#     \in DEST \\
#    \end{align*}
#

# fmt: off
supply_cons = model.add_constraints(
    (trans.sum(i, '*', p) == supply[i, p], f'supply_{i}_{p}')
    for i in ORIG
    for p in PROD
)

demand_cons = model.add_constraints(
    (trans.sum('*', j, p) == demand[j, p], f'demand_{j}_{p}')
    for j in DEST
    for p in PROD
)

multi_cons = model.add_constraints(
    (trans.sum(i, j, '*') <= limit * use[i,j], f'multi_{i}_{j}')
    for i in ORIG
    for j in DEST
)
# fmt: on

# %%
# Solve
# ^^^^^

sol = dex.solve(model, log_output=True)

# %%
# Solution
# ^^^^^^^^

sol.display(print_zeros=False)
