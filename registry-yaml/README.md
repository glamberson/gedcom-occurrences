# Registry-Compliant YAML Files

This directory contains the GEDCOM registry-compliant YAML files for the gedcom-occurrences extension.

These files were submitted to the official GEDCOM registry via PR #173:
https://github.com/FamilySearch/GEDCOM-registries/pull/173

## Structure

The files follow the official GEDCOM registry structure:

- `structure/` - Extension tag definitions (_OCUR, _OCREF, etc.)
- `enumeration/` - Individual enumeration values (Present, Absent, Unknown)
- `enumeration-set/` - Enumeration set definition (Presence)

## Key Differences from Original yaml/ Directory

The original `yaml/` directory files had several issues that prevented registry acceptance:
- Used `type: record` instead of `type: structure`
- Missing enumeration definitions
- Incorrect payload URIs

These registry-compliant versions have been validated and accepted by the GEDCOM registry validator.

## Usage

These files are the authoritative definitions for the gedcom-occurrences extension tags.
Applications implementing this extension should reference these definitions.