============
Installation
============

-------------
Prerequisites
-------------

Python >=3.10 and DOcplex >=2.25.236 is required.

Before installing `docplex-extensions`, ensure that DOcplex is installed and
functioning correctly. For detailed instructions, refer to its `installation
guide <https://ibmdecisionoptimization.github.io/docplex-doc/
getting_started_python.html>`_. To verify, run the following code snippet:

.. code-block:: python

    from docplex.mp.check_list import run_docplex_check_list

    run_docplex_check_list()

-------
Install
-------

`docplex-extensions` can be installed via pip from `PyPI <https://pypi.python
.org/pypi/docplex-extensions>`_.

.. code-block:: bash

    pip install docplex-extensions

---------------------
Optional dependencies
---------------------

`docplex-extensions` provides optional functionality to directly cast pandas
Series/DataFrame/Index into its specialized data structures. If pandas is
present, this functionality will be registered with a custom ``.dex`` accessor.
Refer to the `API reference` section for more details.

pandas >=1.5.0 is recommended.

|
