from setuptools import setup, find_packages

exec(open("nuclei/_version.py").read())

setup(
    name="cems-nuclei",
    version=__version__,
    description="Python wrapper around NUCLEI's functionality.",
    author="Ritchie Vink",
    author_email="info@cemsbv.nl",
    url="https://github.com/cemsbv/nuclei",
    license="mit",
    packages=find_packages(),
    install_requires=[
        "requests>=2.21.0",
        "numpy>=1.16.1",
        "pandas>=0.24.1",
        "ipython>=7.3.0",
        "pyarrow>=0.16.0",
        "polars>=0.7.0",
    ],
    extras_require={"geo": ["geopandas>=0.8.0"]},
    python_requires=">=3.7",
)
