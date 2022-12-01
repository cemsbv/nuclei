.. _getting_started:

Getting started
================

New to `nuclei`? Don’t worry, you’ve found the perfect place to get started!

Installation
-------------
`nuclei` can be installed by running

.. code-block::

    pip install cems-nuclei


Please note that to use `NucleiClient` library `cems-nuclei[client]` should be installed.

Basic usage
-----------
To have a look at the available API's in NUCLEI go to the platform and have a look at the API documentation.
To initialise your session call :func:`nuclei.api.main.create_session`.

.. code-block:: python

    import nuclei

    session = nuclei.create_session()


To help the user create a `schema` to use in the API call `nuclei` has a
:func:`nuclei.client.main.NucleiClient` class. This classes holds a `call_endpoint`
function that transforms python types to JSON types.

The following code-block shows the mechanism behind module. First we
create a `pandas.DataFrame` and transforms it to a serialized DataFrame.

.. ipython:: python

    import pandas as pd

    from nuclei.client import utils

    schema = pd.get_dummies(pd.Series(list('abcaa')))
    print(utils.python_types_to_message(schema))

To transform a serialized DataFrame to its original type use the :func:`nuclei.client.utils.python_types_to_message` function.

.. ipython:: python

    message = utils.python_types_to_message(schema)
    print(utils.message_to_python_types(message))

Please note that a list that of python types will be serialized as well.
This means that the individual object will be transformed.

.. ipython:: python

    message = utils.python_types_to_message(schema)
    print(utils.message_to_python_types([{"a": 12}, message]))


User Guide
-----------

.. toctree::
   :maxdepth: 1

   examples/gef-model.rst

   examples/vibracore.rst