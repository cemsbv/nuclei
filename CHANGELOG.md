# Changelog

All notable changes to this project will be documented in this file.

## [1.0.2] - 2024-12-12

### Features

- *(timeout)* Set DEFAULT_REQUEST_TIMETOUT to 10 seconds

## [1.0.1] - 2024-09-26

### Testing

- *(ci)* Test Python 3.12 in CI

## [1.0.0] - 2024-07-22

### Bug Fixes

- Typos in ConnectionError message
- *(ci)* Use PyPi tokenless authentication

### Miscellaneous Tasks

- !feat: allow multiple versions of one application (#215)
- * feat: allow multiple versions of one application
- * test: update test, add version in mock functions
- * !chore: remove deprecated code
- * chore(deps): update dependecies
- * chore: make version optional
- * chore: reorder parameters checks
- * docs: update doc strings
- PabloVasconez <pvascon@hotmail.com>
- * chore: remove redundant type checks
- * test(client): test valid version error
- ---------
- PabloVasconez <pvascon@hotmail.com>

## [0.5.5] - 2024-01-17

### Bug Fixes

- Use self.timout instead of DEFAULT_REQUEST_TIMEOUT

## [0.5.4] - 2024-01-17

### Features

- Retry endpoint calls by default for specific response status codes, with MAX_RETRIES

## [0.5.3] - 2023-12-14

### Features

- Set timeout as attribute of client

## [0.5.2] - 2023-11-28

### Bug Fixes

- Throw TypeError or ValueError when passing incorrect type or value to arguments of nuclei.client functions

### Miscellaneous Tasks

- Fix typo in Errormessage

## [0.5.1] - 2023-11-23

### Bug Fixes

- Use serialize_jsonifyable_object in post request

### Documentation

- Update reference page

### Features

- Resolve #211 activate option OPT_UTC_Z and OPT_NAIVE_UTC

## [0.5.0] - 2023-11-23

### Documentation

- Update docs

### Features

- Add new serialization functions to nuclei.client.utils
- Deprecate nuclei.client.utils.python_types_to_message

### Miscellaneous Tasks

- Update auto-generated changlog settings

### Refactor

- Use new serialization functions in nuclei.client.call_endpoint()

## [0.4.0] - 2023-11-21

### Documentation

- Update installation instruction

### Features

- Get the application version
- Let use set HTTP methode

### Miscellaneous Tasks

- Clean up tests
- Remove __init__ definition of client class
- Set timeout on all requests
- Test multiple python-versions

### Refactor

- [**breaking**] Remove short-lived token

## [0.4.0-beta.2] - 2023-10-26

### Build

- Update release with token
- Release wheel and source

## [0.4.0-beta.1] - 2023-10-26

### Bug Fixes

- Prepare for cemdev release

### Refactor

- [**breaking**] Client utils remove deserialization (#206)
- [**breaking**] Client utils remove deserialization (#206)
- [**breaking**] Client utils remove deserialization (#206)
- [**breaking**] Client utils remove deserialization (#206)
- [**breaking**] Client utils remove deserialization (#206)
- [**breaking**] Client utils remove deserialization (#206)
- [**breaking**] Client utils remove deserialization (#206)
- [**breaking**] Client utils remove deserialization (#206)
- [**breaking**] Client utils remove deserialization (#206)

## [0.3.2] - 2023-10-05

### Miscellaneous Tasks

- Merge pull request #204 from cemsbv/update-dependencies

## [0.3.1] - 2023-09-22

### Bug Fixes

- Raise a user-friendly error when server is offline (#203)

### Miscellaneous Tasks

- Release 0.3.1

## [0.3.0] - 2023-03-21

### Bug Fixes

- *(ci)* Remove dependency from release on test
- Add deploy docs to github workflow (#189)
- *(docs)* Resolve #185 update pygef (#187)
- *(naming)* Remove _get from properties (#184)
- *(ci)* Update workflows
- *(ci)* Release to pypi trigger (#176)

### Miscellaneous Tasks

- Release 0.3.0
- Merge pull request #178 from cemsbv/fix-ci
- Update ci workflows
- Release 0.3.0a2 (#175)
- Thijs Lukkezen <t.lukkezen@cemsbv.io>
- Merge pull request #172 from cemsbv/update-dependencies
- Update dependencies
- Update dependencies: nuclei, polars, pandas, geopandas
- *(project)* Update name

### Dep

- Bump polars range (#188)

## [0.3.0-alpha] - 2023-03-02

### Co-authored-by

- Thijs Lukkezen <t.lukkezen@cemsbv.io>

### Miscellaneous Tasks

- *(setuptools)* Add pyproject.toml and linting (#169)
- 136 - Explicitly assign lint config-file pyproject.toml in workflow job
- Add user claims to client, update dependencies

### Refactor

- Refactor authentication

## [0.2.0] - 2022-11-29

### Miscellaneous Tasks

- New user token (#119)
- * WIP new user token
- * update input text, add example
- * update docs
- * update setup move dependencies extras_require
- * update documentation
- * raise ImportError when dependencies are not installed
- * WIP new user token
- * update input text, add example
- * update docs
- * update setup move dependencies extras_require
- * update documentation
- * raise ImportError when dependencies are not installed
- * create Client class and update docs
- * fix linter errors

## [0.1.2] - 2022-06-23

### Bug Fixes

- Fix ipython version

### Miscellaneous Tasks

- Fix ci and pin dependecies (#50)
- * pin all (sub) dependencies with pip-tools
- * Fix ci, use pytest
- * Use python 3.7 for pip tools
- * pin all (sub) dependencies with pip-tools
- * Fix ci, use pytest
- * Use python 3.7 for pip tools
- * mock authenticate call
- * lint file
- * pin all (sub) dependencies with pip-tools
- * Fix ci, use pytest
- * Use python 3.7 for pip tools
- * mock authenticate call
- * lint file
- * bump polars version to 0.13.0
- * use `to_json` to serialize polars DataFrame
- Thomas Versteeg <t@versteeg.email>
- Update polars[pyarrow] requirement from ~=0.13.32 to ~=0.13.34
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.32...py-polars-v0.13.34)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.31 to ~=0.13.32
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.31...py-polars-v0.13.32)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.29 to ~=0.13.31
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.29...py-polars-v0.13.31)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.17 to ~=0.13.29
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.17...py-polars-v0.13.29)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.16 to ~=0.13.17
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.16...py-polars-v0.13.17)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.13 to ~=0.13.16
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.13...py-polars-v0.13.16)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.12 to ~=0.13.13
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.12...py-polars-v0.13.13)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.9 to ~=0.13.12
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.9...py-polars-v0.13.12)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.8 to ~=0.13.9
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.8...py-polars-v0.13.9)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.7 to ~=0.13.8
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.7...py-polars-v0.13.8)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Bump actions/checkout from 2 to 3
- Bumps [actions/checkout](https://github.com/actions/checkout) from 2 to 3.
- - [Release notes](https://github.com/actions/checkout/releases)
- - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
- - [Commits](https://github.com/actions/checkout/compare/v2...v3)
- ---
- Updated-dependencies:
- - dependency-name: actions/checkout
-   dependency-type: direct:production
-   update-type: version-update:semver-major
- ...
- Dependabot[bot] <support@github.com>
- Update polars requirement from <0.13.0,>=0.9.12 to >=0.9.12,<0.14.0
- Updates the requirements on [polars](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.9.12...py-polars-v0.13.0)
- ---
- Updated-dependencies:
- - dependency-name: polars
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.3 to ~=0.13.7
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.3...py-polars-v0.13.7)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Bump actions/setup-python from 2 to 3
- Bumps [actions/setup-python](https://github.com/actions/setup-python) from 2 to 3.
- - [Release notes](https://github.com/actions/setup-python/releases)
- - [Commits](https://github.com/actions/setup-python/compare/v2...v3)
- ---
- Updated-dependencies:
- - dependency-name: actions/setup-python
-   dependency-type: direct:production
-   update-type: version-update:semver-major
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.13.1 to ~=0.13.3
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.13.1...py-polars-v0.13.3)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.12.23 to ~=0.13.1
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.12.23...py-polars-v0.13.1)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.12.22 to ~=0.12.23
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.12.22...py-polars-v0.12.23)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.12.20 to ~=0.12.22
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.12.20...py-polars-v0.12.22)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.12.19 to ~=0.12.20
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.12.19...py-polars-v0.12.20)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Update polars[pyarrow] requirement from ~=0.12.17 to ~=0.12.19
- Updates the requirements on [polars[pyarrow]](https://github.com/pola-rs/polars) to permit the latest version.
- - [Release notes](https://github.com/pola-rs/polars/releases)
- - [Changelog](https://github.com/pola-rs/polars/blob/master/CHANGELOG.md)
- - [Commits](https://github.com/pola-rs/polars/compare/py-polars-v0.12.17...py-polars-v0.12.19)
- ---
- Updated-dependencies:
- - dependency-name: polars[pyarrow]
-   dependency-type: direct:production
- ...
- Dependabot[bot] <support@github.com>
- Add range to dependencies

## [0.1.1] - 2022-01-26

### Co-authored-by

- Robin Wimmers <r.wimmers@cemsbv.io>

## [0.1.0] - 2022-01-25

<!-- CEMS BV. -->
