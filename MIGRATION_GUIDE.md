# Migration Guide: Container-Only Model

## Overview

This guide helps you migrate from the old dual-storage model to the new container-only model for the gedcom-occurrences extension.

## What's Changing

### Old Model (Dual Storage)
```gedcom
# Participant data in BOTH places
0 @O1@ _OCUR
1 _PART @I1@
2 ROLE Head       # Here
2 AGE 45y         # Here
2 NOTE Farmer     # Here
2 SOUR @S1@       # Here

0 @I1@ INDI
1 _OCREF @O1@
2 ROLE Head       # AND here
2 AGE 45y         # AND here
```

### New Model (Container-Only)
```gedcom
# Event data only in _OCUR
0 @O1@ _OCUR
1 TYPE Census
1 DATE 1850
1 PLAC Boston
1 _PART @I1@      # Simple reference only

# Participant data only in _OCREF
0 @I1@ INDI
1 _OCREF @O1@
2 ROLE Head       # All participant
2 AGE 45y         # data goes
2 NOTE Farmer     # here now
2 SOUR @S1@
```

## Migration Steps

### Step 1: Identify Files Using Old Structure

Look for GEDCOM files with `_PART` structures containing substructures:
```bash
grep -l "_PART.*ROLE\|_PART.*AGE\|_PART.*NOTE\|_PART.*SOUR" *.ged
```

### Step 2: Manual Migration Process

For each occurrence with participant data:

1. **Keep in _OCUR**: TYPE, DATE, PLAC, event-level NOTE, event-level SOUR
2. **Move to _OCREF**: ROLE, AGE, participant NOTE, participant SOUR
3. **Simplify _PART**: Keep only as pointer

### Step 3: Automated Migration Script

```python
#!/usr/bin/env python3
# migrate_occurrences.py

import re

def migrate_gedcom(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    output = []
    in_part = False
    part_data = {}
    current_part_ref = None
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Detect _PART structure
        if re.match(r'^\d+ _PART @\w+@', line):
            in_part = True
            current_part_ref = re.search(r'@(\w+)@', line).group(1)
            part_data[current_part_ref] = {'substructs': []}
            output.append(line)
            
        # Collect _PART substructures
        elif in_part and re.match(r'^\d+ \w+', line):
            level = int(line[0])
            if level == 2:  # Substructure of _PART
                part_data[current_part_ref]['substructs'].append(line)
                # Don't output these - we'll move them
            else:
                in_part = False
                output.append(line)
                
        # Detect _OCREF and add moved data
        elif re.match(r'^\d+ _OCREF @\w+@', line):
            output.append(line)
            # Add the stored participant data here
            ocur_ref = re.search(r'@(\w+)@', line).group(1)
            # Find matching participant data
            for part_ref, data in part_data.items():
                if part_ref in data.get('ocur_refs', []):
                    for substruct in data['substructs']:
                        output.append(substruct)
                        
        else:
            output.append(line)
            
        i += 1
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(output))

# Usage
migrate_gedcom('old_file.ged', 'new_file.ged')
```

## Examples

### Before Migration
```gedcom
0 @O1@ _OCUR
1 TYPE Census
1 DATE 5 JUN 1850
1 PLAC Boston, MA
1 _PART @I1@
2 ROLE Head
2 AGE 45y
2 NOTE Listed as farmer
2 SOUR @S1@
3 PAGE Line 15
1 _PART @I2@
2 ROLE Spouse
2 AGE 42y

0 @I1@ INDI
1 NAME John /Smith/
1 _OCREF @O1@
2 ROLE Head
2 AGE 45y

0 @I2@ INDI
1 NAME Mary /Smith/
1 _OCREF @O1@
2 ROLE Spouse
2 AGE 42y
```

### After Migration
```gedcom
0 @O1@ _OCUR
1 TYPE Census
1 DATE 5 JUN 1850
1 PLAC Boston, MA
1 _PART @I1@
1 _PART @I2@

0 @I1@ INDI
1 NAME John /Smith/
1 _OCREF @O1@
2 ROLE Head
2 AGE 45y
2 NOTE Listed as farmer
2 SOUR @S1@
3 PAGE Line 15

0 @I2@ INDI
1 NAME Mary /Smith/
1 _OCREF @O1@
2 ROLE Spouse
2 AGE 42y
```

## Validation

After migration, verify:

1. **No data in _PART** except the reference:
   ```bash
   grep -A2 "_PART" migrated.ged
   ```

2. **All participant data in _OCREF**:
   ```bash
   grep -A5 "_OCREF" migrated.ged
   ```

3. **No duplicate ROLE/AGE** between structures

## Special Cases

### Case 1: Data Only in _PART
If old file has data only in _PART (no _OCREF), create _OCREF structures:
```gedcom
# Add to individual:
1 _OCREF @O1@
2 ROLE Head       # Moved from _PART
2 AGE 45y         # Moved from _PART
```

### Case 2: Conflicting Data
If _PART and _OCREF have different values:
- Use _OCREF value (person's perspective)
- Document conflict in NOTE

### Case 3: Family Participation
Same rules apply for FAM records:
```gedcom
0 @F1@ FAM
1 _OCREF @O1@
2 ROLE Family
2 NOTE Entire family attended
```

## Benefits After Migration

1. **No synchronization issues**
2. **Clear data ownership**
3. **GRAMPS compatibility**
4. **Simpler validation**
5. **Better performance**

## Support

For questions or issues:
- Open an issue at https://github.com/glamberson/gedcom-occurrences/issues
- Check examples/ directory for reference implementations