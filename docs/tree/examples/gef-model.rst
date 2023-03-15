.. _gef-model:

CPT Core
================

The `CPT Core` is the first developed API that has been widely used by CRUX employees and external clients in the past years.
It consists of a fully automated soil classification based on a convolutional neural network,
The complete API documentation can be accesses `here <https://nuclei.cemsbv.io/#/cptcore/api>`__.

Please note that you need a NUCLEI account to call one of our endpoints.
You can sign up `here <https://nuclei.cemsbv.io/#/>`__ to get your free access to `CPT Core`!
For this example we set the account information in our environment. If you are not
confident to reproduce that `nuclei` will ask you to provide the `user token` when calling the
endpoint.

Lets show you how to use `nuclei` and access the `CPT Core` API.

.. ipython:: python

    import os

    from pygef import read_cpt
    import numpy as np
    from nuclei.client import NucleiClient

    # set app name
    APP = "CPT Core"

    # create session
    client = NucleiClient()

Next we use the cpt parser of `pygef <https://cemsbv.github.io/pygef/>`__ to parse a cpt and create the request body.
This body is used to call the `"/plot"` endpoint of the `CPT Core` with
:meth:`~.call_endpoint`.

.. ipython:: python
    :okexcept:

    # Parse a CPT file with pygef.
    path_cpt = os.path.join(
        os.environ.get("DOC_PATH"), "_static/data/cpt.gef"
    )
    cpt = read_cpt(path_cpt)

    # create the body to send to the gef-model endpoint.
    schema = {
        "cpt_object": {
            "name": cpt.alias,
            "x": cpt.delivered_location.x,
            "y": cpt.delivered_location.y,
            "ref": cpt.delivered_vertical_position_offset,
            "index": np.array(
                cpt.data["depthOffset"], dtype=float
            ),
            "qc": np.array(cpt.data["coneResistance"], dtype=float),
            "fs": np.array(cpt.data["localFriction"], dtype=float),
        },
        "img_encoding": "base64",
    }

    # call the gef-model endpoint with nuclei
    @savefig cpt_plot.png
    plot = client.call_endpoint(APP, "/plot", schema)

    @suppress
    with open(
        os.path.join(
            os.environ.get("DOC_PATH"), "savefig/cpt_plot.png"), "wb") as png:
        png.write(plot.data)
        # FIXME: ipython savefig does not work with plot result


The `"/classify"` endpoint allows you the access the data of the graph above.
Please note that the :meth:`~.call_endpoint` will transform the responds
to python types by default. This means that for example a `polars <https://www.pola.rs/>`__ DataFrames are transformed
from `json` back to the DataFrame.

.. ipython:: python
    :okexcept:

    # call the gef-model endpoint with nuclei
    responds = client.call_endpoint(APP, "/classify", schema)
    print(responds["prediction"])

If you have any questions please send an email to info@cemsbv.nl