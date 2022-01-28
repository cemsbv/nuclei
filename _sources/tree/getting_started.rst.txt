.. _getting_started:

Getting started
================

New to `nuclei`? Don’t worry, you’ve found the perfect place to get started!

Installation
-------------
`nuclei` can be installed by running

.. code-block::

    pip install cems-nuclei


Please note that to use `GeoDataFrames` from the `geopandas` library `cems-nuclei[geo]` should be installed.

Basic usage
-----------
To have a look at the available API's in NUCLEI run the following code-block:

.. ipython:: python

    import nuclei

    print(nuclei.get_applications())

For more information about the available endpoints of single API run the following code-block:

.. ipython:: python

    print(nuclei.get_endpoints("piles"))

To call an endpoint use :func:`nuclei.api_zoo.call_endpoint()`


To help the user create a `schema` to use in the API call `nuclei` has a
:func:`nuclei.utils.python_types_to_message` function. This function
transforms python types to JSON types.

The following code-block creates a `pandas.DataFrame` and transforms it to a
serialized DataFrame.

.. ipython:: python

    import pandas as pd

    schema = pd.get_dummies(pd.Series(list('abcaa')))
    print(nuclei.utils.python_types_to_message(schema))

To transform a serialized DataFrame to its original type use the :func:`nuclei.utils.python_types_to_message` function.

.. ipython:: python

    message = nuclei.utils.python_types_to_message(schema)
    print(nuclei.utils.message_to_python_types(message))

Please note that a list that of python types will be serialized as well.
This means that the individual object will be transformed.

.. ipython:: python

    message = nuclei.utils.python_types_to_message(schema)
    print(nuclei.utils.message_to_python_types([{"a": 12}, message]))


.. toctree::
   :maxdepth: 1
   :caption: User Guide:

   examples/gef-model.rst