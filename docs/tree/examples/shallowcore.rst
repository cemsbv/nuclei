.. _shallowcore:

ShallowCore
================

ShallowCore is a python library and API service aimed at shallow foundation design according to
NEN9997-1 for a range of applications such as permanent structures like buildings and bridges or
temporary structures like cranes and work platforms. From a set of inputs - characteristic values
for soil strength parameters, loads, foundation dimensions or slopes, a fully automated sequence
of calculations is carried out to check all required failure mechanisms. Optimization of foundation
dimensions for a defined load case is possible by showing the change in bearing capacity for a
range of foundation widths or horizontal load orientations and the thickness of a ground improvement.
All this allows for rapid design and automation of an engineers' repetitive tasks, freeing up their
time for critical thinking and analysis of results.
The complete API documentation can be accesses `here <https://nuclei.cemsbv.io/#/shallowcore/api>`__.

Please note that you need a NUCLEI account to call one of our endpoints.
You can sign up `here <https://nuclei.cemsbv.io/#/>`__ to get your free access to `ShallowCore`!
For this example we set the account information in our environment. If you are not
confident to reproduce that `nuclei` will ask you to provide the `user token` when calling the
endpoint.

Lets show you how to use `nuclei` and access the `ShallowCore` API.

.. ipython:: python

    from nuclei.client import NucleiClient

    # set app name
    APP = "ShallowCore"

    # create session
    client = NucleiClient()

Next we define the schema to send to the endpoint.

.. ipython:: python
    :okexcept:

    # create the body to send to the ShallowCore endpoint.
    schema = {
      "alpha_undrained": 8,
      "foundation": {
        "alpha": 0,
        "foundation_level": -0.5,
        "foundation_type": "rectangle",
        "stiff": True,
        "geometry": {
          "length": 2,
          "width": 3
        }
      },
      "freatic_level": -3.5,
      "load": {
        "gamma_f;bijz;u": 0.9,
        "gamma_f;g;u": 0.85,
        "gamma_f;og;u": 1.1,
        "gamma_f;q;u": 1
      },
      "material": {
        "gamma_m;c": 1.4,
        "gamma_m;fundr": 1.25,
        "gamma_m;gamma": 1.15,
        "gamma_m;phi": 1.7
      },
      "soil_profile": {
        "c_k": [
          0,
          5,
          0,
        ],
        "elevation_top": [
          -0.44,
          -0.5,
          -0.9,
        ],
        "f_und;rep": [
          0,
          0,
          11,
        ],
        "gamma_sat": [
          20,
          18,
          15,
        ],
        "gamma_unsat": [
          18,
          18,
          15,
        ],
        "layer_name": [
          "sand 1",
          "clay",
          "sand 2",
        ],
        "phi_k": [
          27,
          22.5,
          22.5,
        ],
        "thickness": [
          0.06,
          0.4,
          15,
        ]
      },
      "undrained_above_freatic": False,
      "vertical_load": {
        "V_bijz_rep": 7.5,
        "V_per_rep": 19.3,
        "V_ver_rep": 5.3,
        "favorable_load": True,
        "load_eccentricity": {
          "x_length": 0.15,
          "x_width": 0.1
        },
        "q_load_rep": 0
      }
    }

    # call the ShallowCore endpoint with nuclei
    response = client.call_endpoint(APP, "/bearingCapacity", schema)

    # print validation
    print(response["conclusion_dr"])


If you have any questions please send an email to info@cemsbv.nl