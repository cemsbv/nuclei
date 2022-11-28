.. _gef-model:

Gef-Model
================

The `gef-model` is the first developed API that has been widely used by CRUX employees and external clients in the past years.
It consists of a fully automated soil classification based on a convolutional neural network,
The complete API documentation can be accesses `here <https://crux-nuclei.com/api/gef-model/ui/>`__.

Please note that you need a NUCLEI account to call one of our endpoints.
You can sign up `here <nuclei.cemsbv.io/#/>`__ to get your free access to `gef-model`!
For this example we set the account information in our environment. If you are not
confident to reproduce that `nuclei` will ask you to provide the `user token` when calling the
endpoint.

Lets show you how to use `nuclei` and access the `gef-model` API.

.. code-block:: python

    import os
    from IPython.display import Image
    from pygef import Cpt
    import numpy as np
    import nuclei
    from nuclei import utils

    # create session
    session = nuclei.create_session()

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
    responds = session.post(
        "https://crux-nuclei.com/api/gef-model/plot",
        json=utils.python_types_to_message(schema)
    )

    plot = Image(responds.content)



The `"/classify"` endpoint allows you the access the data of the graph above.
Please note that the :func:`nuclei.utils.message_to_python_types()` will transform the responds
to python types. This means that for example a `polars <https://www.pola.rs/>`__ DataFrames are transformed
from `json` back to the DataFrame.

.. code-block:: python

    # call the gef-model endpoint with nuclei
    responds = session.post(
        "https://crux-nuclei.com/api/gef-model/classify",
        json=utils.python_types_to_message(schema)
    ).json()
    print(utils.message_to_python_types(responds)["prediction"])

If you have any questions please send an email to info@cemsbv.nl