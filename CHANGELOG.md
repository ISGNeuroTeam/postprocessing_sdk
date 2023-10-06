# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.2] - 2023-10-06
### Changed
- added missing return expression in run_otl() function
 
## [1.3.1] - 2023-10-02
### Changed
- run_otl() function now returns actual result

## [1.3.0] - 2023-03-29
### Added
- Added jenkinsfile, changelog, releasenotes and license to command template
- csv type to write command

### Changed
- Download and use conda in command makefile template
- pp_exec_env version up to 1.4.8
- pp_stdlib version up to 0.2.1

### Fixed
- Fix error in BaseCommand subclass checking
### Removed
- Removed otl_v1_config.ini from command template


## [1.2.1] - 2023-01-16
### Changed
- Set 500  max rows and columns for dataframe

## [1.2.0] - 2022-12-14
### Added
- Added `--file` option to run otl query from file

## [1.1.2] - 2022-11-28
### Fixed
- Remove unnecessary lines in requirements.txt

## [1.1.1] - 2022-07-28
### Changed
- `pp_stdlib` version bump

## [1.1.0] - 2022-07-26
### Changed
- Changed `createcommandlinks` to create links in the package directory instead of the local one
- Changed `createcommandrepo` to create a link to the command in the package directory
- Bumped pp_exec_env version

## [1.0.1] - 2022-07-06
### Changed
- Bumped OTLand version

## [1.0.0] - 2022-07-06
### Added
- Initial release
- CHANGELOG.md
