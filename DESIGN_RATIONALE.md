# Design Rationale: Container-Only Model

## Overview

The gedcom-occurrences extension adopts a container-only model where:
- `_OCUR` records contain ONLY event-level data
- `_OCREF` structures contain ALL participant-specific data

This document explains why this design was chosen.

## The Problem with Data Duplication

### Original Design Flaw
The initial design stored participant data in both `_PART` and `_OCREF`:

```gedcom
# Data stored in TWO places
0 @O1@ _OCUR
1 _PART @I1@
2 ROLE Head         # Role here
2 AGE 45y           # Age here

0 @I1@ INDI
1 _OCREF @O1@
2 ROLE Head         # Role duplicated
2 AGE 45y           # Age duplicated
```

### Problems Created

1. **Synchronization Issues**
   - What happens when the values differ?
   - Which one is authoritative?
   - How to keep them in sync?

2. **Update Complexity**
   - Every change must be made in two places
   - Easy to forget one location
   - Leads to inconsistent data

3. **Validation Nightmares**
   - Need rules like "AGE in _OCREF must match AGE in _PART"
   - Complex validation logic
   - Poor user experience

4. **Import/Export Confusion**
   - When importing from systems with single storage
   - Where to put the data?
   - How to handle conflicts?

## The Container-Only Solution

### Clean Separation of Concerns

```gedcom
# Event contains event data
0 @O1@ _OCUR
1 TYPE Census
1 DATE 5 JUN 1850
1 PLAC Boston

# Person contains participation data
0 @I1@ INDI
1 _OCREF @O1@
2 ROLE Head
2 AGE 45y
2 NOTE Head of household
```

### Benefits

1. **Single Source of Truth**
   - Each piece of data stored once
   - No synchronization needed
   - Clear ownership

2. **Matches Existing Models**
   - GRAMPS: Event object + EventRef object
   - GEDCOM X: Event + Role
   - Natural separation

3. **Simplicity**
   - Easy to understand
   - Easy to implement
   - Easy to validate

4. **Flexibility**
   - Person owns their participation details
   - Can have different sources for participation
   - Privacy control per participant

## GRAMPS Model Alignment

### GRAMPS Design
```python
# Event object - container only
class Event:
    type = "Census"
    date = "1850"
    place = "Boston"
    # NO participant data

# EventRef - participation data
class EventRef:
    event = event_handle
    role = "Primary"
    attributes = {"age": "45"}
    # ALL participant data
```

### Our Design (Matches Exactly)
```gedcom
# _OCUR = Event (container)
0 @O1@ _OCUR
1 TYPE Census
1 DATE 1850
1 PLAC Boston

# _OCREF = EventRef (participation)
0 @I1@ INDI
1 _OCREF @O1@
2 ROLE Primary
2 AGE 45y
```

## Use Case Examples

### Census Record
**Event Data** (shared by all participants):
- Date: 5 JUN 1850
- Place: Boston, MA
- Type: Census

**Participation Data** (unique per person):
- John: Head, 45y, dwelling 123
- Mary: Wife, 38y, dwelling 123
- Thomas: Boarder, 22y, dwelling 123

### Marriage Ceremony
**Event Data**:
- Date: 15 JUN 1875
- Place: St. Mary's Church
- Type: Marriage

**Participation Data**:
- John: Groom, age 25
- Mary: Bride, age 22
- Rev. Wilson: Officiator
- James Smith: Witness

## Backward Compatibility

The container model still supports backward compatibility:

```gedcom
# Modern system uses _OCUR
0 @O1@ _OCUR
1 TYPE Census
1 DATE 1850

# Also exports traditional CENS for legacy
0 @I1@ INDI
1 CENS
2 DATE 1850
1 _OCREF @O1@  # Ignored by legacy systems
```

## Conclusion

The container-only model:
- Eliminates data duplication
- Matches proven designs (GRAMPS)
- Simplifies implementation
- Improves data integrity
- Maintains backward compatibility

This is why we're refactoring from the original dual-storage design to the cleaner container-only approach.