=======================
Index-set functionality
=======================

.. currentmodule:: docplex_extensions

----------
IndexSet1D
----------

Custom `list`-like data structure to define index-sets with 1-dim scalar elements.

Constructor
-----------
.. autosummary::
   :toctree: ../auto_api/

   IndexSet1D

Attributes
----------
.. autosummary::

   IndexSet1D.name

Sequence operations
-------------------
.. autosummary::

   IndexSet1D.append
   IndexSet1D.extend
   IndexSet1D.insert
   IndexSet1D.remove
   IndexSet1D.pop
   IndexSet1D.clear
   IndexSet1D.index
   IndexSet1D.sort
   IndexSet1D.reverse

Dunder methods
--------------
- ``IndexSet1D.__contains__``
- ``IndexSet1D.__iter__``
- ``IndexSet1D.__reversed__``
- ``IndexSet1D.__len__``
- ``IndexSet1D.__getitem__``
- ``IndexSet1D.__setitem__``
- ``IndexSet1D.__delitem__``
- ``IndexSet1D.__add__``
- ``IndexSet1D.__iadd__``
- ``IndexSet1D.__lt__``
- ``IndexSet1D.__le__``
- ``IndexSet1D.__eq__``
- ``IndexSet1D.__ne__``
- ``IndexSet1D.__gt__``
- ``IndexSet1D.__ge__``

----------
IndexSetND
----------

Custom `list`-like data structure to define index-sets with N-dim tuple elements.

Constructor
-----------
.. autosummary::
   :toctree: ../auto_api/

   IndexSetND

Attributes
----------
.. autosummary::

   IndexSetND.names

Efficient subset selection
--------------------------
.. autosummary::

   IndexSetND.subset
   IndexSetND.squeeze

Sequence operations
-------------------
.. autosummary::

   IndexSetND.append
   IndexSetND.extend
   IndexSetND.insert
   IndexSetND.remove
   IndexSetND.pop
   IndexSetND.clear
   IndexSetND.index
   IndexSetND.sort
   IndexSetND.reverse

Dunder methods
--------------
- ``IndexSetND.__contains__``
- ``IndexSetND.__iter__``
- ``IndexSetND.__reversed__``
- ``IndexSetND.__len__``
- ``IndexSetND.__getitem__``
- ``IndexSetND.__setitem__``
- ``IndexSetND.__delitem__``
- ``IndexSetND.__add__``
- ``IndexSetND.__iadd__``
- ``IndexSetND.__lt__``
- ``IndexSetND.__le__``
- ``IndexSetND.__eq__``
- ``IndexSetND.__ne__``
- ``IndexSetND.__gt__``
- ``IndexSetND.__ge__``

------------------------------------------
Casting from pandas Series/DataFrame/Index
------------------------------------------

Methods to cast pandas Series/DataFrame/Index into IndexSet1D/IndexSetND are
provided through the custom ``.dex`` accessor.

.. currentmodule:: pandas

.. autosummary::
   :toctree: ../auto_api/
   :template: autosummary/accessor_method.rst

   Series.dex.to_indexset
   DataFrame.dex.to_indexset
   Index.dex.to_indexset
