from setuptools import find_packages, setup

exec(open("nuclei/_version.py").read())

setup(
    name="cems-nuclei",
    version=__version__,  # type: ignore
    description="Python wrapper around NUCLEI's functionality.",
    author="Ritchie Vink",
    author_email="info@cemsbv.nl",
    url="https://github.com/cemsbv/nuclei",
    license="mit",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pyjwt==2.6.0",
        "ipython>=7.3.0",
    ],
    extras_require={
        "client": [
            "geopandas>=0.8.1,<0.11.0",
            "numpy>=1.19.4,<1.22.0",
            "pandas>=1.2,<1.4",
            "polars>=0.13.0,<0.14.0",
        ]
    },
    python_requires=">=3.7",
)
