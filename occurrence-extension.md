# Occurrence Extension for GEDCOM 7

## Overview

This extension enables GEDCOM 7 to represent occurrences as independent, first-class objects that multiple people can participate in with different roles, matching the data models of both GRAMPS and GEDCOM X. The term "occurrence" (_OCUR) distinguishes these independent records from traditional embedded events (EVEN).

## Motivation

### Current GEDCOM 7 Limitations
```gedcom
0 @I1@ INDI
1 NAME John /Smith/
1 CENS               # Census embedded in person
2 DATE 1850
2 PLAC Boston

0 @I2@ INDI  
1 NAME Mary /Smith/
1 CENS               # Same census duplicated!
2 DATE 1850
2 PLAC Boston
```

Problems:
- Same event duplicated across participants
- No way to indicate roles (head of household, boarder, etc.)
- Updates must be made in multiple places
- No single source of truth for the event

### GRAMPS Model
```python
# Event is independent
event = Event()
event.type = EventType.CENSUS
event.date = "1850"
event.place = "Boston"

# People reference the event with roles
person1.add_event_ref(EventRef(event, role="Head"))
person2.add_event_ref(EventRef(event, role="Spouse"))
person3.add_event_ref(EventRef(event, role="Boarder"))
```

### GEDCOM X Model
```json
{
  "events": [{
    "id": "event1",
    "type": "http://gedcomx.org/Census",
    "date": {"formal": "+1850"},
    "place": {"original": "Boston"},
    "roles": [
      {"person": {"resource": "#person1"}, "type": "Principal"},
      {"person": {"resource": "#person2"}, "type": "Household"},
      {"person": {"resource": "#person3"}, "type": "Witness"}
    ]
  }]
}
```

## Extension Design

### Core Tags

#### `_OCUR` - Occurrence Record
```yaml
tag: _OCUR
uri: https://gedcom.io/terms/v7/_OCUR
type: record
substructures:
  TYPE: "{1:1}"   # Occurrence type (Birth, Census, etc.)
  DATE: "{0:1}"   # When it happened
  PLAC: "{0:1}"   # Where it happened
  CAUS: "{0:1}"   # Cause (for deaths, etc.)
  AGNC: "{0:1}"   # Agency (for official occurrences)
  RELI: "{0:1}"   # Religion (for religious occurrences)
  NOTE: "{0:M}"   # General notes
  SOUR: "{0:M}"   # Sources for the occurrence itself
  OBJE: "{0:M}"   # Media for the occurrence
  _PART: "{0:M}"  # Participants
  UID: "{0:M}"    # Unique identifiers
  CHAN: "{0:1}"   # Change tracking
```

#### `_PART` - Occurrence Participant
```yaml
tag: _PART
uri: https://gedcom.io/terms/v7/_PART
type: structure
payload: "@<XREF:INDI>@ | @<XREF:FAM>@"
substructures:
  ROLE: "{0:1}"   # Role in occurrence
  AGE: "{0:1}"    # Age at occurrence
  NOTE: "{0:M}"   # Participant-specific notes
  SOUR: "{0:M}"   # Sources for this participation
```

#### `_OCREF` - Reference from Person/Family to Occurrence
```yaml
tag: _OCREF
uri: https://gedcom.io/terms/v7/_OCREF
type: structure
payload: "@<XREF:_OCUR>@"
superstructures: ["INDI", "FAM"]
substructures:
  ROLE: "{0:1}"   # Person's role in occurrence
  AGE: "{0:1}"    # Age at occurrence
  NOTE: "{0:M}"   # Participation notes
  SOUR: "{0:M}"   # Sources for participation
```

### Role Vocabulary

Based on GEDCOM X and GRAMPS:

| Role | Description | Used For |
|------|-------------|----------|
| Principal | Primary person | Most events |
| Witness | Observer/informant | All events |
| Officiator | Performed ceremony | Religious events |
| Bride | Female spouse | Marriage |
| Groom | Male spouse | Marriage |
| Spouse | Gender-neutral | Marriage |
| Child | Child participant | Baptism, etc. |
| Parent | Parent participant | Various |
| Godparent | Spiritual parent | Baptism |
| Informant | Info provider | Death, birth |
| Beneficiary | Received benefit | Will, probate |
| Heir | Inherited | Probate |

### Example Usage

```gedcom
0 HEAD
1 SCHMA
2 TAG _OCUR https://gedcom.io/terms/v7/_OCUR
2 TAG _PART https://gedcom.io/terms/v7/_PART  
2 TAG _OCREF https://gedcom.io/terms/v7/_OCREF

# Independent census occurrence
0 @O1@ _OCUR
1 TYPE Census
1 DATE 5 JUN 1850
1 PLAC Boston, Suffolk, Massachusetts, USA
1 _PART @I1@
2 ROLE Head
2 AGE 45y
1 _PART @I2@
2 ROLE Spouse  
2 AGE 42y
1 _PART @I3@
2 ROLE Child
2 AGE 12y
1 _PART @I4@
2 ROLE Boarder
2 AGE 23y
2 NOTE Occupation: Laborer
1 SOUR @S1@
2 PAGE Sheet 42, Lines 15-18

# People reference the occurrence
0 @I1@ INDI
1 NAME John /Smith/
1 _OCREF @O1@
2 ROLE Head

0 @I2@ INDI
1 NAME Mary /Smith/
1 _OCREF @O1@
2 ROLE Spouse

# Baptism with multiple participants
0 @O2@ _OCUR
1 TYPE Baptism
1 DATE 15 MAR 1838
1 PLAC St. Mary's Church, Boston
1 _PART @I3@
2 ROLE Child
2 AGE 3m
1 _PART @I1@
2 ROLE Parent
1 _PART @I2@
2 ROLE Parent
1 _PART @I5@
2 ROLE Godparent
1 _PART @I6@
2 ROLE Officiator
2 NOTE Rev. James Wilson

# Shared burial occurrence
0 @O3@ _OCUR
1 TYPE Burial  
1 DATE 18 NOV 1918
1 PLAC Flanders Field, Belgium
1 NOTE Mass grave for flu victims
1 _PART @I10@
2 ROLE Principal
1 _PART @I11@
2 ROLE Principal
1 _PART @I12@
2 ROLE Principal
```

## Compatibility Mappings

### From GEDCOM X
```javascript
// GEDCOM X event
{
  "type": "http://gedcomx.org/Census",
  "roles": [
    {"person": {"resource": "#p1"}, "type": "Principal"}
  ]
}

// Becomes
0 @O1@ _OCUR
1 TYPE Census
1 _PART @I1@
2 ROLE Principal
```

### From GRAMPS
```python
# GRAMPS EventRef
event_ref = EventRef()
event_ref.ref = "E0001" 
event_ref.role = "Witness"

# Becomes
1 _OCREF @O1@
2 ROLE Witness
```

### Backward Compatibility

For systems that don't understand the extension:
1. Include traditional embedded events that match the OCUR data
2. The _OCREF is simply ignored by legacy systems
3. Legacy systems see normal, working events

```gedcom
0 @O1@ _OCUR              # Extension: shared occurrence
1 TYPE Census
1 DATE 5 JUN 1850
1 PLAC Boston
1 _PART @I1@
2 ROLE Head
1 _PART @I2@
2 ROLE Spouse

0 @I1@ INDI
1 CENS                    # Legacy: person's view
2 DATE 5 JUN 1850         # Must match OCUR
2 PLAC Boston             # Must match OCUR
2 AGE 45y                 # Person-specific OK
2 _OCREF @O1@             # Extension (ignored by legacy)
```

## Benefits

1. **Single Source of Truth**: Event data in one place
2. **Rich Participation**: Multiple people with specific roles
3. **Research Clarity**: Can model complex historical events
4. **Tool Compatibility**: Maps cleanly to GRAMPS and GEDCOM X
5. **Extensible**: Can add new roles as needed

## Implementation Notes

### For GRAMPS Export
1. Each GRAMPS Event becomes an _OCUR record
2. Each EventRef becomes an _OCREF
3. Role types map directly
4. Preserve event handles as UID

### For GEDCOM X Import/Export
1. Event.roles map to _PART structures
2. Role types need URI mapping
3. Person resources become XREFs
4. Preserve event IDs

### Validation Rules
1. _OCUR records should have at least one _PART
2. _OCREF should match a _PART in the occurrence
3. Roles should use controlled vocabulary when possible
4. AGE in _OCREF should match AGE in corresponding _PART