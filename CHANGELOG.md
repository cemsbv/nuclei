# Changelog

All notable changes to this project will be documented in this file.

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

### Co-authored-by

- Thijs Lukkezen <t.lukkezen@cemsbv.io>

### Miscellaneous Tasks

- Release 0.3.0
- Release 0.3.0a2 (#175)
- *(project)* Update name

### Dep

- Bump polars range (#188)

## [0.3.0-alpha] - 2023-03-02

### Co-authored-by

- Thijs Lukkezen <t.lukkezen@cemsbv.io>

### Miscellaneous Tasks

- *(setuptools)* Add pyproject.toml and linting (#169)

## [0.1.2] - 2022-06-23

### Co-authored-by

- Thomas Versteeg <t@versteeg.email>

### Signed-off-by

- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>
- Dependabot[bot] <support@github.com>

## [0.1.1] - 2022-01-26

### Co-authored-by

- Robin Wimmers <r.wimmers@cemsbv.io>

<!-- CEMS BV. -->
