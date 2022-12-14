.. _pilecore:

PileCore
================

PileCore aims to give you the full pile calculation utilities without an engineer in the loop.
This means that calculations must be able to run from start to finish from a set of given
parameters. `Pilecore` is able to determine the tipping point between positive and negative
friction and will optimize pile groups automatically.
The complete API documentation can be accesses `here <https://nuclei.cemsbv.io/#/pilecore/api>`__.

Please note that you need a NUCLEI account to call one of our endpoints.
You can sign up `here <https://nuclei.cemsbv.io/#/>`__ to get your free access to `PileCore`!
For this example we set the account information in our environment. If you are not
confident to reproduce that `nuclei` will ask you to provide the `user token` when calling the
endpoint.

Lets show you how to use `nuclei` and access the `PileCore` API.

.. ipython:: python

    from time import sleep
    import pandas as pd

    from nuclei import NucleiClient

    # set app name
    APP = "PileCore"

    # create session
    client = NucleiClient()

Next we define the schema to send to the endpoint.

.. ipython:: python
    :okexcept:

    # create the body to send to the PileCore endpoint.
    schema = {
      "cpt_objects": [
        {
          "bottom_bearing_capacity": [
            10,
            20,
            30
          ],
          "coordinates": {
            "x": 142892.19,
            "y": 470783.87
          },
          "name": "CPT101",
          "negative_friction": [
            10,
            10,
            10
          ],
          "shaft_bearing_capacity": [
            90,
            180,
            270
          ]
        },
        {
          "bottom_bearing_capacity": [
            10,
            20,
            30
          ],
          "coordinates": {
            "x": 142892.19,
            "y": 470783.87
          },
          "name": "CPT102",
          "negative_friction": [
            10,
            10,
            10
          ],
          "shaft_bearing_capacity": [
            90,
            180,
            270
          ]
        }
      ],
      "pile_tip_level": [
        0,
        -1,
        -2
      ],
      "pile_load_uls": 100,
      "stiff_construction": True,
      "spatial_factor": [
        0.5,
        0.7,
        0.9,
        1.1
      ],
      "optimize_result_by": [
        "minimum_pile_level",
        "number_of_cpts",
        "number_of_consecutive_pile_levels"
      ],
      "resolution": 1
    }

    # call the pilecore endpoint with nuclei
    response = client.call_endpoint(APP, "/grouper/group_cpts", schema)

    # fetch the task result
    sleep(5)
    response = client.call_endpoint(APP, "/get-task-result", response)
    print(pd.DataFrame(response["sub_groups"][0]["table"]))


If you have any questions please send an email to info@cemsbv.nl