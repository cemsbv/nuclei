.. _vibracore:

VibraCore
================

VibraCore is an API service that automates the risk management of building
damage during vibration works, such as the installation of sheet piles or driven piles. Based on the
soil profile (GEF file) the maximum impact force is calculated (according to CUR 166) or the elastic
modulus of the soil is determined (according to Prepal). This is used to predict the maximum vibration
velocity. Based on the attributes of the nearby buildings the failure vibration velocity is calculated
(according to SBR A). If the check fails the building has a unacceptable risk (according to SBR A) of
being damaged by the installation of the piles or sheet piles.
The complete API documentation can be accesses `here <https://nuclei.cemsbv.io/#/vibracore/api>`__.

Please note that you need a NUCLEI account to call one of our endpoints.
You can sign up `here <nuclei.cemsbv.io/#/>`__ to get your free access to `VibraCore`!
For this example we set the account information in our environment. If you are not
confident to reproduce that `nuclei` will ask you to provide the `user token` when calling the
endpoint.

Lets show you how to use `nuclei` and access the `VibraCore` API.

.. ipython:: python

    from time import sleep

    from nuclei import NucleiClient

    # set app name
    APP = "VibraCore"

    # create session
    client = NucleiClient()

Next we define the schema to send to the endpoint.

.. ipython:: python
    :okexcept:

    # create the body to send to the VibraCore endpoint.
    schema = {
      "building_info": [
        {
          "geometry": {
            "coordinates": [
              [
                [
                  0,
                  0
                ],
                [
                  0,
                  5
                ],
                [
                  5,
                  5
                ]
              ]
            ],
            "type": "Polygon"
          },
          "metadata": {
            "ID": "1234"
          },
          "properties_cur": {
            "building_part": "vloer",
            "foundation_element": "staal",
            "installation_type": "trillen",
            "material": "beton",
            "safety_factor": 0.05,
            "vibration_direction": "vertical"
          },
          "properties_sbr_a": {
            "category": "one",
            "frequency": 30,
            "monumental": True,
            "structural_condition": "gevoelig",
            "vibration_sensitive": True,
            "vibration_type": "continu"
          }
        }
      ],
      "prediction": {
        "attenuation_constant": 1.1,
        "force": 500,
        "measurement_type": "indicatief",
        "methode_safety_factor": "CUR",
        "references_velocity": 0.9,
        "variation_coefficient": 0.02
      },
      "validation": {
        "source_location": {
          "coordinates": [
            7,
            7
          ],
          "type": "Point"
        }
      }
    }

    # call the vibracore endpoint with nuclei
    response = client.call_endpoint(APP, "/cur166/geodataframe", schema)

    # fetch the task result
    sleep(5)
    gdf = client.call_endpoint(APP, "/get-task", response)
    print(gdf)

    # plot figure
    @savefig vibracore_map.png
    gdf.plot()

If you have any questions please send an email to info@cemsbv.nl