.. _gef-model:

Gef-Model
================

The `gef-model` is the first developed API that has been widely used by CRUX employees and external clients in the past years.
It consists of a fully automated soil classification based on a convolutional neural network,
The complete API documentation can be accesses `here <https://crux-nuclei.com/api/gef-model/ui/>`__.

Please note that you need a NUCLEI account to call one of our endpoints.
You can sign up `here <https://crux-nuclei.com/sign-up>`__ to get your free access to `gef-model`!
For this example we set the account information in our environment. If you are not
confident to reproduce that `nuclei` will ask you to provide the credentials when calling the
endpoint.


Lets show you how to use `nuclei` and access the `gef-model` API.
We use the :func:`nuclei.api_zoo.get_endpoints` function to get an overview of the different endpoints
that are available within `gef-model`.


.. ipython:: python

    import os

    from pygef import Cpt
    import numpy as np
    import nuclei

    APP = "gef-model"
    print(nuclei.get_endpoints(APP))

Next we use the cpt parser of `pygef <https://cemsbv.github.io/pygef/>`__ to parse a cpt and create the request body.
This body is used to call the `"/plot"` endpoint of the `gef-model` with :func:`nuclei.api_zoo.call_endpoint()`.

.. ipython:: python

    # Parse a CPT file with pygef.
    path_cpt = os.path.join(
        os.environ.get("DOC_PATH"), "_static/data/cpt.gef"
    )
    cpt = Cpt(path_cpt)

    # create the body to send to the gef-model endpoint.
    schema = {
        "cpt_object": {
            "name": cpt.test_id,
            "x": cpt.x,
            "y": cpt.y,
            "ref": cpt.zid,
            "index": np.array(
                cpt.df["elevation_with_respect_to_nap"], dtype=float
            ),
            "qc": np.array(cpt.df["qc"], dtype=float),
            "fs": np.array(cpt.df["fs"], dtype=float),
        },
        "img_encoding": "base64",
    }

    # call the gef-model endpoint with nuclei
    @savefig cpt_plot.png
    plot = nuclei.call_endpoint(APP, "/plot", schema)

    @suppress
    with open(
        os.path.join(
            os.environ.get("DOC_PATH"), "savefig/cpt_plot.png"), "wb") as png:
        png.write(plot.data)
        # FIXME: ipython savefig does not work with plot result


The `"/classify"` endpoint allows you the access the data of the graph above.
Please note that the :func:`nuclei.api_zoo.call_endpoint()` will transform the responds
to python types by default. This means that for example a `polars <https://www.pola.rs/>`__ DataFrames are transformed
from `json` back to the DataFrame.

.. ipython:: python

    # call the gef-model endpoint with nuclei
    responds = nuclei.call_endpoint(APP, "/classify", schema)
    print(responds["prediction"])

If you have any questions please send an email to info@cemsbv.nl