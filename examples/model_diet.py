"""
============
Diet problem
============

Please refer to chapter 2 in the `AMPL Book <https://ampl.com/learn/ampl-book>`_ for a
detailed description of the problem. We will illustrate how to implement this model with
DOcplex using the `docplex-extensions` library.

Implementation reference:
https://github.com/ampl/colab.ampl.com/blob/master/ampl-lecture/diet_case_study.ipynb
— Copyright (c) 2022-2022, AMPL Optimization inc. (licensed under the MIT License)
"""

# %%
# Ensure DOcplex and its required dependecies are installed correctly
# -------------------------------------------------------------------

from docplex.mp.check_list import run_docplex_check_list

run_docplex_check_list()

# %%
# Import libraries
# ----------------

from docplex.mp.model import Model

import docplex_extensions as dex

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
#    i &\in NUTR: && \text{Nutrients to consider} \\
#    j &\in FOOD: && \text{Food items to consider} \\
#    \end{align*}
#

NUTR = dex.IndexSet1D(['A', 'B1', 'B2', 'C'], name='NUTRIENT')

FOOD = dex.IndexSet1D(['BEEF', 'CHK', 'FISH', 'HAM', 'MCH', 'MTL', 'SPG', 'TUR'], name='FOOD')

# %%
# Parameters
# ^^^^^^^^^^
#
# .. math::
#
#    \begin{align*}
#    cost_{j} &\in \mathbb{R}^{+}: && \text{Cost of food item $j$}, \; \forall \; j \in FOOD \\
#    f\_min_{j} &\in \mathbb{R}_{0}^{+}: && \text{Minimum purchase quantity required for food item
#     $j$}, \; \forall \; j \in FOOD \\
#    f\_max_{j} &\in \mathbb{R}_{0}^{+}: && \text{Maximum purchase quantity allowed for food item
#     $j$}, \; \forall \; j \in FOOD \\
#    n\_min_{i} &\in \mathbb{R}_{0}^{+}: && \text{Minimum amount required of nutrient $i$}, \;
#     \forall \; i \in NUTR \\
#    n\_max_{i} &\in \mathbb{R}_{0}^{+}: && \text{Maximum amount allowed of nutrient $i$}, \;
#     \forall \; i \in NUTR \\
#    amt_{i, j} &\in \mathbb{R}_{0}^{+}: && \text{Amount of nutrient $i$ in food item $j$}, \;
#     \forall \; i \in NUTR \; \text{and} \; j \in FOOD \\
#    \end{align*}
#

cost = dex.ParamDict1D(
    {
        'BEEF': 3.19,
        'CHK': 2.59,
        'FISH': 2.29,
        'HAM': 2.89,
        'MCH': 1.89,
        'MTL': 1.99,
        'SPG': 1.99,
        'TUR': 2.49,
    },
    key_name='FOOD',
    value_name='COST',
)

f_min = dex.ParamDict1D(
    {
        'BEEF': 0,
        'CHK': 0,
        'FISH': 0,
        'HAM': 0,
        'MCH': 0,
        'MTL': 0,
        'SPG': 0,
        'TUR': 0,
    },
    key_name='FOOD',
    value_name='MIN-QTY',
)

f_max = dex.ParamDict1D(
    {
        'BEEF': 100,
        'CHK': 100,
        'FISH': 100,
        'HAM': 100,
        'MCH': 100,
        'MTL': 100,
        'SPG': 100,
        'TUR': 100,
    },
    key_name='FOOD',
    value_name='MAX-QTY',
)

n_min = dex.ParamDict1D(
    {'A': 700, 'C': 700, 'B1': 700, 'B2': 700},
    key_name='NUTRIENT',
    value_name='MIN-AMT',
)

n_max = dex.ParamDict1D(
    {'A': 10000, 'C': 10000, 'B1': 10000, 'B2': 10000},
    key_name='NUTRIENT',
    value_name='MAX-AMT',
)

amt = dex.ParamDictND(
    {
        ('A', 'BEEF'): 60,
        ('C', 'BEEF'): 20,
        ('B1', 'BEEF'): 10,
        ('B2', 'BEEF'): 15,
        ('A', 'CHK'): 8,
        ('C', 'CHK'): 0,
        ('B1', 'CHK'): 20,
        ('B2', 'CHK'): 20,
        ('A', 'FISH'): 8,
        ('C', 'FISH'): 10,
        ('B1', 'FISH'): 15,
        ('B2', 'FISH'): 10,
        ('A', 'HAM'): 40,
        ('C', 'HAM'): 40,
        ('B1', 'HAM'): 35,
        ('B2', 'HAM'): 10,
        ('A', 'MCH'): 15,
        ('C', 'MCH'): 35,
        ('B1', 'MCH'): 15,
        ('B2', 'MCH'): 15,
        ('A', 'MTL'): 70,
        ('C', 'MTL'): 30,
        ('B1', 'MTL'): 15,
        ('B2', 'MTL'): 15,
        ('A', 'SPG'): 25,
        ('C', 'SPG'): 50,
        ('B1', 'SPG'): 25,
        ('B2', 'SPG'): 15,
        ('A', 'TUR'): 60,
        ('C', 'TUR'): 20,
        ('B1', 'TUR'): 15,
        ('B2', 'TUR'): 10,
    },
    key_names=('FOOD', 'NUTR'),
    value_name='AMT',
)

# %%
# Set up model
# ------------

# %%
# Instantiate
# ^^^^^^^^^^^

model: Model = Model(name='diet')

# %%
# Add decision variables
# ^^^^^^^^^^^^^^^^^^^^^^
#
# .. math::
#
#    \begin{align*}
#    buy_{j} &\in \mathbb{R}_{0}^{+}: && \text{Quantity of food item $j$ to be purchased}, \;
#     \forall \; j \in FOOD \\
#    &\geq f\_min_{j} \\
#    &\leq f\_max_{j} \\
#    \end{align*}
#

buy = dex.add_variables(
    model,
    indexset=FOOD,
    var_type='continuous',
    lb=f_min,
    ub=f_max,
    name='BUY-QTY',
)

# %%
# Set objective
# ^^^^^^^^^^^^^
#
# .. math::
#
#    \begin{align*}
#    &\text{Minimize the total cost of the diet:} \\
#    &\text{min.} \; \sum_{j \in FOOD} cost_{j} \times buy_{j} \\
#    \end{align*}
#

# fmt: off
model.minimize(
    model.sum(cost[j] * buy[j] for j in FOOD)
)
# fmt: on

# %%
# Add constraints
# ^^^^^^^^^^^^^^^
#
# .. math::
#
#    \begin{align*}
#    &\text{Ensure that the nutritional limits are satisfied by the diet:} \\
#    & \sum_{j \in FOOD} amt_{i, j} \times buy_{j} \geq n\_min_{i}, \; \forall \; i \in NUTR \\
#    & \sum_{j \in FOOD} amt_{i, j} \times buy_{j} \leq n\_max_{i}, \; \forall \; i \in NUTR \\
#    \end{align*}
#

# fmt: off
min_nutr_reqd = model.add_constraints(
    (model.sum(amt[i, j] * buy[j] for j in FOOD) >= n_min[i], f'min-nutr-reqd_{i}')
    for i in NUTR
)

max_nutr_allwd = model.add_constraints(
    (model.sum(amt[i, j] * buy[j] for j in FOOD) <= n_max[i], f'max-nutr-allwd_{i}')
    for i in NUTR
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
