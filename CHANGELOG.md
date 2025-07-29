# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2025-07-29

### Fixed
- Fixed YAML indentation errors in all structure files
- Removed blank lines in the middle of specification sentences
- Corrected key ordering to match GEDCOM registry standards
- Added proper indentation for extension tags arrays
- Added missing _VALUE structure definition

### Changed
- All YAML files now pass official registry validator
- Specification text reformatted for clarity

## [0.2.1] - 2025-07-28

### Added
- Registry-compliant YAML files in `registry-yaml/` directory
- CHANGELOG.md file
- Link to GEDCOM Registry PR #173 in README

### Changed
- Updated README to reference registry submission status

### Technical Details
- Added 9 YAML files validated by official GEDCOM registry validator:
  - 5 structure definitions (_OCUR, _OCREF, _PART, _PRESENCE, _ATTR)
  - 3 enumeration definitions (Present, Absent, Unknown)
  - 1 enumeration-set definition (Presence)

## [0.2.0] - 2025-01-27

### Changed
- **BREAKING**: Switched to container-only model
- _OCUR now contains only event data, no participant information
- _PART simplified to just person pointer (no role/attributes)
- Participant data moved to _OCREF under individual records

### Added
- Migration guide for upgrading from v0.1.0
- Compatibility examples showing hybrid approach

## [0.1.0] - 2025-01-26

### Added
- Initial release
- _OCUR occurrence record
- _PART participant substructure
- _OCREF occurrence reference
- Basic examples