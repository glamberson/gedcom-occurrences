# gedcom-occurrences

**Version:** 0.2.0

> ⚠️ **Breaking Change in v0.2.0**: This extension now uses a container-only model. 
> See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for upgrade instructions.

This repository contains proposed [FamilySearch GEDCOM](https://gedcom.io/specs/) extensions
for representing independent events that involve multiple participants with specific roles.

This extension enables GEDCOM 7 to handle shared events (like census enumerations, group burials, ceremonies) without duplicating event data across multiple person records.

## Quick Example

Traditional GEDCOM duplicates shared events:
```gedcom
0 @I1@ INDI
1 NAME John /Smith/
1 CENS
2 DATE 1850
2 PLAC Boston

0 @I2@ INDI  
1 NAME Mary /Smith/
1 CENS
2 DATE 1850
2 PLAC Boston
```

With the Occurrence Extension (hybrid compatibility):
```gedcom
0 HEAD
1 SCHMA
2 TAG _OCUR https://gedcom.io/terms/v7/_OCUR
2 TAG _PART https://gedcom.io/terms/v7/_PART
2 TAG _OCREF https://gedcom.io/terms/v7/_OCREF

0 @O1@ _OCUR              # Shared occurrence (event data only)
1 TYPE Census
1 DATE 1850
1 PLAC Boston
1 _PART @I1@             # Simple reference
1 _PART @I2@             # Simple reference

0 @I1@ INDI
1 NAME John /Smith/
1 _OCREF @O1@            # Reference to shared occurrence
2 ROLE Head              # Participant data here
2 AGE 45y                # Participant data here
1 CENS                   # For backward compatibility
2 DATE 1850
2 PLAC Boston

0 @I2@ INDI
1 NAME Mary /Smith/
1 _OCREF @O1@            # Reference to shared occurrence  
2 ROLE Spouse            # Participant data here
2 AGE 42y                # Participant data here
1 CENS                   # For backward compatibility
2 DATE 1850
2 PLAC Boston
```

## Extensions

The following extension is proposed for discussion:

* [Occurrence Extension](occurrence-extension.md)

All proposed extensions use [documented extension tags](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extension-tags). If they later become incorporated into the FamilySearch GEDCOM standard, standard tags will be defined at that time.

Rather than write out URIs in full, we use prefix notation: any URI beginning with one
of the following short prefixes followed by a colon is shorthand for a URI beginning
with the corresponding URI prefix

| Short Prefix | URI Prefix                                          |
|:-------------|:----------------------------------------------------|
| `g7`         | `https://gedcom.io/terms/v7/`                       |
| `ext`        | `https://github.com/glamberson/gedcom-occurrences/` |

## Tags Provided

- `_OCUR` - Occurrence record (independent event with multiple participants)
- `_PART` - Participant in an occurrence (specifies person and role)
- `_OCREF` - Occurrence reference (links person to occurrence)

## Benefits

1. **Single Source of Truth**: Event data stored once, referenced multiple times
2. **Rich Participation**: Multiple people with specific roles
3. **Research Clarity**: Models complex historical events accurately
4. **Tool Compatibility**: Maps cleanly to GRAMPS and GEDCOM X event models
5. **Backward Compatibility**: Can coexist with traditional embedded events

## Status

**Published** - v0.2.0 released

**Registry Submission** - Submitted to [GEDCOM Registry PR #173](https://github.com/FamilySearch/GEDCOM-registries/pull/173)

## See Also

- [Specification](occurrence-extension.md)
- [Glossary](GLOSSARY.md)
- [Compatibility Guide](compatibility.md)
- [Examples](examples/)
- [YAML Definitions](yaml/)
- [Registry-Compliant YAML](registry-yaml/)