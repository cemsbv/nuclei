# Changelog

All notable changes to this project will be documented in this file.

## [3.1.0] - 2026-01-14

### Bug Fixes
- *Deps*: Update all non-major dependencies (#239)

### Features
- Add PileCore v4 to routing table

### Miscellaneous Tasks

- *Ci*:
    - Disable pyink in github super-linter
    - Move from dependabot to renovate

### Deploy
- Update deploy_docs.yaml

## [3.0.1] - 2025-04-22

### Bug Fixes

- *Call_endpoint*:
    - Apply suggestions from code review
    - Skip check of available endpoints when get API specification fails
- *Ci*: Use ubuntu-latest for docs CI

## [3.0.0] - 2025-04-10

### Documentation
- *Changelog*: Use default changelog format

### Refactor
- *Client*:  [**BREAKING**]Use return image bytes back directly

## [2.0.1] - 2025-04-09

### Bug Fixes
- *Deps*: Re-add ipython dependency

## [2.0.0] - 2025-04-08

### Bug Fixes

- *Deps*:
    - Use correct dependencies for documentation
    - Pin dependencies and update linting dependencies

### Refactor
- *Python*:  [**BREAKING**]Bump minimum supported Python version to 3.11

## [1.0.3] - 2025-03-03

### Bug Fixes
- *Deps*: Unpin pyjwt and refresh all requirements

### Miscellaneous Tasks
- *Deps*: Bump actions/upload-artifact from 3 to 4

## [1.0.2] - 2024-12-12

### Features
- *Timeout*: Set DEFAULT_REQUEST_TIMETOUT to 10 seconds

## [1.0.1] - 2024-09-26

### Testing
- *Ci*: Test Python 3.12 in CI

## [1.0.0] - 2024-07-22

### Bug Fixes
- *Ci*: Use PyPi tokenless authentication
- Typos in ConnectionError message

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

### Features
- Add new serialization functions to nuclei.client.utils

### Miscellaneous Tasks
- Update auto-generated changlog settings

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
- [**BREAKING**] Remove short-lived token

## [0.4.0-beta.2] - 2023-10-26

### Build
- Update release with token
- Release wheel and source

## [0.4.0-beta.1] - 2023-10-26

### Bug Fixes
- Prepare for cemdev release

### Refactor
- [**BREAKING**] Client utils remove deserialization (#206)

## [0.3.1] - 2023-09-22

### Bug Fixes
- Raise a user-friendly error when server is offline (#203)

### Miscellaneous Tasks
- Release 0.3.1

## [0.3.0] - 2023-03-21

### Bug Fixes

- *Ci*:
    - Remove dependency from release on test
    - Release to pypi trigger (#176)
- *Docs*: Resolve #185 update pygef (#187)
- *Naming*: Remove _get from properties (#184)
- Add deploy docs to github workflow (#189)

### Miscellaneous Tasks
- *Project*: Update name
- Release 0.3.0
- Release 0.3.0a2 (#175)

### Dep
- Bump polars range (#188)

## [0.3.0-alpha] - 2023-03-02

### Miscellaneous Tasks
- *Setuptools*: Add pyproject.toml and linting (#169)

## [0.1.0] - 2022-01-25

<!-- CEMS BV. -->
