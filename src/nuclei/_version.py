from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("nuclei")
# during CI
except PackageNotFoundError:
    __version__ = "unknown"
