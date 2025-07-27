# OCUR to EVEN Compatibility Mapping

## Overview

This document explains how to map between the Occurrence extension (_OCUR) and standard GEDCOM 7 events (EVEN) for backward compatibility.

## Key Concepts

### OCUR (Occurrence)
- Independent, top-level record
- Multiple participants with roles
- Single source of truth
- Referenced by individuals/families

### EVEN (Event)
- Embedded in INDI or FAM records
- Single participant implied
- May be duplicated across records
- TYPE required to specify event type

## Compatibility Strategies

### Strategy 1: Hybrid Approach (Recommended)

Enhance existing event structures with occurrence references:

```gedcom
# The authoritative occurrence
0 @O1@ _OCUR
1 TYPE Census
1 DATE 5 JUN 1850
1 PLAC Boston, Massachusetts
1 _PART @I1@
2 ROLE Head
2 AGE 45y
1 _PART @I2@
2 ROLE Spouse
2 AGE 42y
1 SOUR @S1@

# Individual event views (compatible with legacy)
0 @I1@ INDI
1 NAME John /Smith/
1 CENS
2 DATE 5 JUN 1850      # Matches OCUR (required)
2 PLAC Boston, Massachusetts # Matches OCUR (required)
2 AGE 45y               # Person-specific (allowed)
2 NOTE Head of household # Person-specific (allowed)
2 _OCREF @O1@          # Extension: points to authority

0 @I2@ INDI
1 NAME Mary /Smith/
1 CENS
2 DATE 5 JUN 1850      # Matches OCUR (required)
2 PLAC Boston, Massachusetts # Matches OCUR (required)
2 AGE 42y               # Person-specific (allowed)
2 NOTE Wife of head     # Person-specific (allowed)
2 _OCREF @O1@          # Extension: points to authority
```

**Benefits**:
- **Legacy systems**: See normal census events, work perfectly
- **Extension systems**: Use OCUR as authoritative source
- **No duplication**: Shared data exists once in OCUR
- **User-friendly**: No mysterious duplicate events

### Strategy 2: Pure Extension (Alternative)

#### OCUR → EVEN Algorithm

```python
def ocur_to_even(ocur, participants):
    """
    Convert an OCUR record to EVEN structures for each participant
    """
    events = []
    
    # Get occurrence data
    event_type = ocur.TYPE
    date = ocur.DATE
    place = ocur.PLAC
    sources = ocur.SOUR
    
    # Get all participants
    all_participants = [(p.pointer, p.ROLE, p.AGE) for p in ocur._PART]
    
    for person_id, role, age in all_participants:
        # Create EVEN for this person
        even = create_structure('EVEN')
        even.TYPE = event_type
        even.DATE = date
        even.PLAC = place
        even.AGE = age
        
        # Add occurrence reference
        even._OCREF = ocur.id
        
        # Copy sources
        for source in sources:
            even.SOUR = source
        
        # Add to person record
        person = get_record(person_id)
        person.add_structure(even)
        
        # Add ASSO links to other participants
        for other_id, other_role, _ in other_parts:
            if should_link(event_type, role, other_role):
                asso = create_structure('ASSO', other_id)
                asso.RELA = f"{event_type} with - {other_role}"
                person.add_structure(asso)
        
        events.append((person_id, even))
    
    return events
```

### Strategy 3: Legacy Import Conversion

#### EVEN → OCUR Algorithm

```python
def even_to_ocur(all_individuals):
    """
    Detect shared events and create OCUR records
    """
    # Group potential shared events
    event_candidates = defaultdict(list)
    
    for person in all_individuals:
        for even in person.get_structures('EVEN'):
            # Create signature for matching
            sig = (even.TYPE, even.DATE, even.PLAC)
            event_candidates[sig].append({
                'person': person,
                'even': even,
                'age': even.AGE,
                'role': infer_role(even, person)
            })
    
    # Create OCUR for multi-person events
    ocur_records = []
    for sig, participants in event_candidates.items():
        if len(participants) > 1:
            # Create new OCUR
            ocur = create_record('_OCUR')
            ocur.TYPE = sig[0]
            ocur.DATE = sig[1]
            ocur.PLAC = sig[2]
            
            # Add participants
            for p in participants:
                part = create_structure('_PART', p['person'].xref)
                part.ROLE = p['role']
                part.AGE = p['age']
                ocur.add_structure(part)
                
                # Add reference from person
                ocref = create_structure('_OCREF', ocur.xref)
                ocref.ROLE = p['role']
                p['person'].add_structure(ocref)
            
            # Merge sources (remove duplicates)
            sources = merge_sources(participants)
            for source in sources:
                ocur.add_structure(source)
            
            ocur_records.append(ocur)
    
    return ocur_records
```

## Event Type Mapping

| OCUR TYPE | EVEN TYPE | Standard Tag | Notes |
|-----------|-----------|--------------|-------|
| Census | Census | CENS | Use CENS if primary person |
| Birth | Birth | BIRT | Single participant only |
| Death | Death | DEAT | Single participant only |
| Marriage | Marriage | MARR | Use FAM.MARR if available |
| Burial | Burial | BURI | Can have multiple |
| Baptism | Baptism | BAPM/CHR | Multiple participants |
| Probate | Probate | PROB | Multiple beneficiaries |
| Will | Will | WILL | Multiple beneficiaries |
| Immigration | Immigration | IMMI | Family groups |
| Custom | [Type] | EVEN | Always use EVEN |

## Role Mapping

### Standard Roles
| OCUR Role | EVEN Representation |
|-----------|--------------------|
| Principal | Primary record holder |
| Witness | ASSO with RELA "Witness at [event]" |
| Officiator | NOTE "Officiated by [name]" |
| Spouse | ASSO with RELA "Spouse at [event]" |
| Child | ASSO with RELA "Child at [event]" |
| Parent | ASSO with RELA "Parent at [event]" |

### Role Inference (EVEN → OCUR)
| Context | Inferred Role |
|---------|---------------|
| Person has the EVEN | Principal |
| ASSO to person with EVEN | Based on RELA |
| FAM event, HUSB/WIFE | Spouse |
| FAM event, CHIL | Child |
| NOTE mentions "witness" | Witness |
| NOTE mentions "officiated" | Officiator |

## Special Cases

### 1. Family Events

Family-level occurrences need special handling:

```gedcom
# OCUR for family event
0 @O2@ _OCUR
1 TYPE Marriage
1 DATE 14 FEB 1848
1 _PART @I1@
2 ROLE Groom
1 _PART @I2@
2 ROLE Bride
1 _PART @F1@
2 ROLE Family
1 _PART @I3@
2 ROLE Witness

# Compatible FAM record
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 14 FEB 1848
2 NOTE Witness: Robert Jones
1 _OCREF @O2@
2 ROLE Family
```

### 2. Single-Person Events

Some events should remain as traditional EVEN:

```gedcom
# Better as traditional event
0 @I1@ INDI
1 BIRT
2 DATE 15 MAR 1805
2 PLAC London

# Not recommended as OCUR unless multiple people involved
```

### 3. Census Enumerations

Census is the classic shared event:

```gedcom
# One OCUR
0 @O3@ _OCUR
1 TYPE Census
1 DATE 1850
1 PLAC Household 123, Boston
1 _PART @I1@
2 ROLE Head
1 _PART @I2@
2 ROLE Spouse
1 _PART @I3@
2 ROLE Child
1 _PART @I4@
2 ROLE Boarder

# Each person gets EVEN for compatibility
0 @I1@ INDI
1 CENS
2 DATE 1850
2 PLAC Household 123, Boston
2 NOTE Head of household (see associated individuals)
1 _OCREF @O3@
```

## Authority and Conflict Resolution

### Data Authority Rules
1. **OCUR is authoritative** for shared attributes (DATE, PLAC, TYPE)
2. **Embedded events** are "person's view" and can add person-specific data
3. **Conflicts**: If embedded event contradicts OCUR, OCUR takes precedence
4. **Validation**: Tools should warn about conflicts

### What Can Be Different
```gedcom
0 @O1@ _OCUR
1 DATE 5 JUN 1850        # Authoritative
1 PLAC Boston            # Authoritative

0 @I1@ INDI
1 CENS
2 DATE 5 JUN 1850        # Must match OCUR
2 PLAC Boston            # Must match OCUR
2 AGE 45y                # OK: person-specific
2 NOTE Head of household # OK: person-specific
2 _OCREF @O1@
```

## Best Practices

### 1. When to Use OCUR
- Multiple participants (census, burial plots)
- Shared ceremonies (marriage, baptism)
- Group events (immigration, military service)
- Complex events with many roles

### 2. Implementation Strategy
- **Start with hybrid**: Both OCUR and embedded events
- **Legacy support**: Ensure embedded events work standalone
- **Validation**: Check OCUR/embedded consistency
- **Migration path**: Eventually drop embedded events when ecosystem ready

### 3. Source Citation
- Place sources on OCUR when shared
- Duplicate sources on EVEN for compatibility
- Use source-specific details in EVEN if needed

### 4. Notes Strategy
- OCUR: General event notes
- EVEN: Participant-specific notes
- Include participant list in EVEN notes

## Validation Rules

1. **Consistency**: OCUR and EVEN data should match
2. **Completeness**: All OCUR._PART should have corresponding _OCREF
3. **No Orphans**: Every _OCREF should point to valid _OCUR
4. **Role Matching**: Roles should be consistent between _PART and _OCREF
5. **Date/Place Matching**: EVEN should have same date/place as referenced OCUR

## Example Conversion Functions

### Full Export with Compatibility

```python
def export_with_compatibility(database):
    output = GedcomFile()
    
    # Add schema
    output.add_extension('_OCUR', 'https://gedcom.io/terms/v7/_OCUR')
    output.add_extension('_PART', 'https://gedcom.io/terms/v7/_PART')
    output.add_extension('_OCREF', 'https://gedcom.io/terms/v7/_OCREF')
    
    # Export all OCUR records
    for event in database.get_events():
        ocur = export_event_as_ocur(event)
        output.add_record(ocur)
    
    # Export individuals with both EVEN and _OCREF
    for person in database.get_people():
        indi = create_indi(person)
        
        for event_ref in person.get_event_refs():
            # Add traditional EVEN
            even = create_even_from_event_ref(event_ref)
            indi.add_structure(even)
            
            # Add OCREF
            ocref = create_ocref(event_ref)
            indi.add_structure(ocref)
        
        output.add_record(indi)
    
    return output
```