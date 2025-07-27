# Occurrence Extension Glossary

This glossary defines terms specific to the GEDCOM 7 Occurrence Extension.

## Extension Information
- **Repository Name**: `gedcom-occurrences` (proposed)
- **URI Prefix**: `https://gedcom.io/terms/v7/`
- **Contact**: https://github.com/gedcom-occurrences

## Terms and Definitions

### _OCUR (Occurrence)
- **Type**: Record
- **URI**: `https://gedcom.io/terms/v7/_OCUR`
- **Definition**: An independent, top-level record representing something that occurred involving one or more participants
- **Etymology**: From "occurrence" - chosen to distinguish from GEDCOM's embedded "event" (EVEN)
- **Purpose**: Enable shared events without duplication
- **Origin**: Combines concepts from GEDCOM X events and GRAMPS event model

### _PART (Participant)
- **Type**: Structure
- **URI**: `https://gedcom.io/terms/v7/_PART`
- **Definition**: Identifies a participant in an occurrence along with their role
- **Payload**: Pointer to INDI or FAM record
- **Superstructure**: _OCUR only
- **Purpose**: Specify who participated and how

### _OCREF (Occurrence Reference)
- **Type**: Structure  
- **URI**: `https://gedcom.io/terms/v7/_OCREF`
- **Definition**: A reference from a person or family to an occurrence they participated in
- **Payload**: Pointer to _OCUR record
- **Superstructures**: INDI, FAM
- **Purpose**: Allow individuals to reference shared occurrences

### TYPE (under _OCUR)
- **Definition**: The type of occurrence (Census, Marriage, Burial, etc.)
- **Cardinality**: {1:1} - Required
- **Values**: Same as GEDCOM 7 event types plus custom values

### ROLE (under _PART/_OCREF)
- **Definition**: The role played by the participant in the occurrence
- **Cardinality**: {0:1} - Optional but recommended
- **Values**: See Controlled Vocabulary below

## Controlled Vocabulary

### Standard Roles
| Role | Definition | Typical Usage |
|------|------------|---------------|
| Principal | Primary person in the occurrence | Birth, death, most events |
| Witness | Person who observed/testified | All event types |
| Officiator | Person who performed ceremony | Marriage, baptism, burial |
| Bride | Female marriage participant | Marriage |
| Groom | Male marriage participant | Marriage |
| Spouse | Gender-neutral marriage participant | Marriage, census |
| Child | Child participant | Baptism, adoption |
| Parent | Parent participant | Birth, baptism |
| Godparent | Spiritual parent | Baptism, confirmation |
| Informant | Person providing information | Death, birth |
| Beneficiary | Person receiving benefit | Will, probate |
| Heir | Person inheriting | Probate |
| Head | Head of household | Census |
| Household | Household member | Census |
| Boarder | Non-family resident | Census |
| Servant | Household servant | Census |
| Guardian | Legal guardian | Various |
| Ward | Person under guardianship | Various |

### Custom Roles
- Any string value not in the standard vocabulary
- Should be descriptive and consistent
- May be localized

## Concepts

### Occurrence vs Event
- **Occurrence (_OCUR)**: Independent record that can be referenced
- **Event (EVEN)**: Embedded structure within a person/family record

### Participant vs Person
- **Participant**: A person/family IN an occurrence with a specific role
- **Person**: The individual record (INDI) being referenced

### Reference vs Participation
- **Reference (_OCREF)**: FROM a person TO an occurrence
- **Participation (_PART)**: Within occurrence, pointing TO a person

## Usage Patterns

### Shared Occurrence Pattern
```
_OCUR ← _OCREF ← INDI
  ↓
_PART → INDI
```

### Compatibility Pattern
```
INDI
 ├── EVEN (for legacy systems)
 └── _OCREF (for occurrence-aware systems)
```

### Role Precedence
When both _PART and _OCREF specify roles:
1. _OCREF role takes precedence (person's perspective)
2. _PART role is occurrence's perspective
3. Log warning if they differ significantly

## Related Terms

### From GEDCOM 7 Core
- **EVEN**: Generic event structure
- **TYPE**: Event/occurrence type specifier
- **DATE**: When something happened
- **PLAC**: Where something happened
- **SOUR**: Source citation
- **NOTE**: Additional information

### From Other Extensions
- **_EVID**: Evidence reference (Evidence Extension)
- **_SOUR**: Source derivation (Citation Extensions)
- **_ANAL**: Analysis document (Research Extension)

## Implementation Notes

### Cardinalities
- `_OCUR._PART`: {0:M} - Multiple participants
- `INDI._OCREF`: {0:M} - Multiple occurrence references
- `_OCUR.TYPE`: {1:1} - Required
- `_PART.ROLE`: {0:1} - Optional but recommended

### Validation Rules
1. Every _OCREF must point to a valid _OCUR
2. Every _PART must point to a valid INDI or FAM
3. _OCUR should have at least one _PART
4. TYPE is required for all _OCUR records

### Best Practices
1. Include ROLE for all participants
2. Use standard role vocabulary when applicable
3. Provide NOTE for custom roles
4. Maintain consistency between _PART and _OCREF