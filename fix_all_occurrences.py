#!/usr/bin/env python3
import os

# Define the correct content for each file
files_content = {
    'registry-yaml/structure/_OCREF.yaml': '''%YAML 1.2
---
lang: en-US

type: structure

uri: https://github.com/glamberson/gedcom-occurrences/_OCREF

extension tags:
  - _OCREF

specification:
  - Occurrence Reference
  - |
    A reference from an individual or family to an occurrence record (_OCUR).
    This structure contains all participant-specific data such as role, age,
    and participation details.
    
    In the container-only model (v0.2.0+), all participant data is stored
    exclusively in _OCREF structures to avoid data duplication and synchronization
    issues.

label: Occurrence Reference

payload: "@<https://github.com/glamberson/gedcom-occurrences/_OCUR>@"

substructures:
  "https://gedcom.io/terms/v7/AGE": "{0:1}"
  "https://gedcom.io/terms/v7/NOTE": "{0:M}"
  "https://gedcom.io/terms/v7/ROLE": "{1:1}"
  "https://gedcom.io/terms/v7/SNOTE": "{0:M}"
  "https://gedcom.io/terms/v7/SOUR": "{0:M}"
  "https://github.com/glamberson/gedcom-occurrences/_ATTR": "{0:M}"
  "https://github.com/glamberson/gedcom-occurrences/_PRESENCE": "{0:1}"

superstructures:
  "https://gedcom.io/terms/v7/record-FAM": "{0:M}"
  "https://gedcom.io/terms/v7/record-INDI": "{0:M}"

contact: https://github.com/glamberson/gedcom-occurrences
...''',

    'registry-yaml/structure/_PART.yaml': '''%YAML 1.2
---
lang: en-US

type: structure

uri: https://github.com/glamberson/gedcom-occurrences/_PART

extension tags:
  - _PART

specification:
  - Occurrence Participant
  - |
    A reference to an individual or family who participated in an occurrence.
    This structure is used within _OCUR records to list all participants.
    The actual participation details (role, age, etc.) are stored in the
    participant's _OCREF structure, not here.
    
    This design maintains a clean separation between occurrence data and
    participant-specific data.

label: Participant Reference

payload: "@<https://gedcom.io/terms/v7/record-INDI>@ | @<https://gedcom.io/terms/v7/record-FAM>@"

substructures:
  "https://gedcom.io/terms/v7/NOTE": "{0:M}"
  "https://github.com/glamberson/gedcom-occurrences/_PRESENCE": "{0:1}"

superstructures:
  "https://github.com/glamberson/gedcom-occurrences/_OCUR": "{0:M}"

contact: https://github.com/glamberson/gedcom-occurrences
...''',

    'registry-yaml/structure/_PRESENCE.yaml': '''%YAML 1.2
---
lang: en-US

type: structure

uri: https://github.com/glamberson/gedcom-occurrences/_PRESENCE

extension tags:
  - _PRESENCE

specification:
  - Presence Status
  - |
    Indicates the presence status of a participant in an occurrence.
    Used to explicitly note when someone was absent from an event they
    were expected to attend, or when their presence is uncertain.
    
    This is particularly useful for census records, family gatherings,
    or other events where absence is notable.

label: Presence Status

payload: https://github.com/glamberson/gedcom-occurrences/enumset-Presence

substructures:
  "https://gedcom.io/terms/v7/NOTE": "{0:M}"

superstructures:
  "https://github.com/glamberson/gedcom-occurrences/_OCREF": "{0:1}"
  "https://github.com/glamberson/gedcom-occurrences/_PART": "{0:1}"

contact: https://github.com/glamberson/gedcom-occurrences
...''',

    'registry-yaml/structure/_ATTR.yaml': '''%YAML 1.2
---
lang: en-US

type: structure

uri: https://github.com/glamberson/gedcom-occurrences/_ATTR

extension tags:
  - _ATTR

specification:
  - Custom Attribute
  - |
    A custom attribute for an occurrence or participant. This allows
    applications to add specific attributes that aren't covered by
    standard GEDCOM structures, ensuring data preservation during
    import/export cycles.
    
    The attribute name is in the payload, and the value is in the
    required _VALUE substructure.

label: Custom Attribute

payload: http://www.w3.org/2001/XMLSchema#string

substructures:
  "https://gedcom.io/terms/v7/NOTE": "{0:M}"
  "https://github.com/glamberson/gedcom-occurrences/_VALUE": "{1:1}"

superstructures:
  "https://github.com/glamberson/gedcom-occurrences/_OCUR": "{0:M}"
  "https://github.com/glamberson/gedcom-occurrences/_OCREF": "{0:M}"

contact: https://github.com/glamberson/gedcom-occurrences
...'''
}

# Write all files
for filepath, content in files_content.items():
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed: {filepath}")

print("\nAll files fixed!")