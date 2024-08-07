.. _getting_started:

Getting started
===============

New to `Nuclei` in `Python`? Don’t worry, you’ve found the perfect place to get started!

Full documentation of the `Nuclei` APIs can be found by logging in to on the `nuclei <https://nuclei.cemsbv.io/#>`_ website.

If you don't yet have a `Nuclei` account you can create one for free(!)
from the `Sign Up` tab after clicking `Log In` on the `nuclei <https://nuclei.cemsbv.io/#>`_
website.

Installation
------------
To install this package, including the `NucleiClient` library and its dependencies, run:

.. code-block::

    pip install cems-nuclei[client]


To skip the installation of the `NucleiClient` library, in case you do not need it (e.g. only use pure requests), run:

.. code-block::

    pip install cems-nuclei

User Token
------------
To connect to `Nuclei` you'll first need a user token. You can obtain
this token by signing in to the `nuclei <https://nuclei.cemsbv.io/#>`_
website and navigate to the 
`API Access Tokens <https://nuclei.cemsbv.io/#/personal-access-tokens>`_ 
section. Here you can create new tokens and copy the `User Token`.

It is recommended to store this token as the environmental variable 
NUCLEI_TOKEN in your `Python` environment. Else you will be prompted 
for this token when necessary.

Guided usage
------------
If you're not so comfortable with creating your own API calls, you can easily access
the `nuclei` endpoints by creating a :class:`~.NucleiClient` object and using
the :meth:`~.call_endpoint` to handle the calls for you.

For instance, calling the `healthcheck` endpoint of the `VibraCore` application
can be done as such:

.. ipython:: python

    from nuclei.client import NucleiClient

    client = NucleiClient()

    client.call_endpoint(
        app="VibraCore",
        endpoint="/healthcheck",
    )

:meth:`~.call_endpoint` automatically returns the unpacked response object. You
can get the raw response by setting the `return_response` argument to `True`.

If the endpoint requires a schema, it can be passed as a Python dictionary to the
`schema` argument of :meth:`~.call_endpoint`. The schema is automatically parsed
with the :func:`~.serialize_jsonifyable_object` function (see below) so in most cases 
you won't have to worry about passing the correct types.

The :class:`~.NucleiClient` can provide you with a list of `Nuclei` applications:

.. ipython:: python

    print(client.applications)

And can also fetch the available versions for an application for you:

.. ipython:: python

    versions = print(client.get_versions(app="PileCore"))

And can also fetch the available endpoints for an application for you:

.. ipython:: python

    endpoints = print(client.get_endpoints(app="PileCore", version="latest"))

You can also check the applications to which you have full access:

.. ipython:: python

    permissions = print(client.user_permissions)

If an application is not listed here, your usage of the app is limited. Check the
documentation of the specific apps to see the limitations.

Advanced usage
--------------
If you want to have full control and create your own API calls
with the `requests` package, you can do so by calling :func:`~.create_session`.

.. ipython:: python

    import nuclei

    nuclei.create_session()

This will return a :class:`requests.Session` object with a response hook that
covers authentication for you.

Schema serialization
--------------------
The automatic schema serialization tools are also available to advanced users by
calling the :func:`~.serialize_jsonifyable_object` function directly.

The following code-block shows the mechanism behind these functions. First we
create a `numpy.array` and transforms it to a serialized list with :func:`~.serialize_jsonifyable_object`.

.. ipython:: python

    import numpy as np

    from nuclei.client import utils

    schema = np.array([[np.int16(1), 2.0], [np.nan, np.float32(4)]])
    message = utils.serialize_jsonifyable_object(schema)
    print(message)
