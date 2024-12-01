# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""
=======================================
Evaluate variability of a DOcplex model
=======================================

We will evaluate variability of the instance `glass4` from MIPLIB 2010 using the
`docplex-extensions` library.

Reference:
Koch, Thorsten, Tobias Achterberg, Erling Andersen, Oliver Bastert, Timo
Berthold, Robert E. Bixby, Emilie Danna et al. "MIPLIB 2010: Mixed integer
programming library version 5." Mathematical Programming Computation 3
(2011): 103-163.
"""

# %%
# Ensure DOcplex and its required dependecies are installed correctly
# -------------------------------------------------------------------

from docplex.mp.check_list import run_docplex_check_list

run_docplex_check_list()

# %%
# Import libraries
# ----------------

from pathlib import Path
from urllib.request import urlopen

from docplex.mp.model_reader import ModelReader

import docplex_extensions as dex

# %%
# Fetch the instance
# ------------------

Path('instances').mkdir(exist_ok=True)
name = 'glass4.mps.gz'

response = urlopen(f'https://miplib.zib.de/WebData/instances/{name}')

response_OK = True
if response.getcode() == 200:
    with open(f'instances/{name}', 'wb') as fp:
        fp.write(response.read())
else:
    response_OK = False
    print(f'Could not fetch the instance {name} from MIPLIB 2010')

# %%
# Run the `runseeds` procedure
# ----------------------------

if response_OK:
    model = ModelReader.read('instances/glass4.mps.gz')
    model.parameters.timelimit = 5
    dex.runseeds(model, count=3, log_output=True)
