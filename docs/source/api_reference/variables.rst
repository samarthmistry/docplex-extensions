======================
Variable functionality
======================

.. currentmodule:: docplex_extensions._var_funcs

---------------
Add variable(s)
---------------
.. autosummary::
   :toctree: ../auto_api/

   add_variable
   add_variables

.. currentmodule:: docplex_extensions._var_dicts

---------
VarDict1D
---------

Custom subclass of `dict` to store DOcplex model variables with 1-dim scalar keys.

.. autosummary::
   :toctree: ../auto_api/
   :nosignatures:

   VarDict1D

Attributes
----------
.. autosummary::

   VarDict1D.key_name
   VarDict1D.value_name

Numerical operations
--------------------
.. autosummary::

   VarDict1D.sum

Mapping operations
------------------
.. autosummary::

   VarDict1D.get
   VarDict1D.lookup

Views
-----
- ``VarDict1D.items()``
- ``VarDict1D.keys()``
- ``VarDict1D.values()``

---------
VarDictND
---------

Custom subclass of `dict` to store DOcplex model variables with N-dim tuple keys.

.. autosummary::
   :toctree: ../auto_api/
   :nosignatures:

   VarDictND

Attributes
----------
.. autosummary::

   VarDictND.key_names
   VarDictND.value_name

Numerical operations
--------------------
.. autosummary::

   VarDictND.sum

Mapping operations
------------------
.. autosummary::

   VarDictND.get
   VarDictND.lookup

Views
-----
- ``VarDictND.items()``
- ``VarDictND.keys()``
- ``VarDictND.values()``
