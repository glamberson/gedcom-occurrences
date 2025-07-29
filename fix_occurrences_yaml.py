#!/usr/bin/env python3
import yaml
import os
import sys

def fix_yaml_file(filepath):
    """Fix YAML formatting issues in occurrences files"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix the specific issues:
    # 1. Fix extension tags indentation
    content = content.replace('extension tags:\n- ', 'extension tags:\n  - ')
    
    # 2. Fix specification indentation
    content = content.replace('specification:\n- ', 'specification:\n  - ')
    
    # 3. Remove blank lines in the middle of sentences in specifications
    lines = content.split('\n')
    in_spec = False
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if line.strip() == 'specification:':
            in_spec = True
            fixed_lines.append(line)
        elif in_spec and line.strip() and not line.startswith(' '):
            # End of specification section
            in_spec = False
            fixed_lines.append(line)
        elif in_spec and i > 0 and line.strip() == '' and i < len(lines) - 1:
            # Skip blank lines in the middle of specification
            next_line = lines[i + 1] if i < len(lines) - 1 else ''
            if next_line.strip() and next_line.startswith('  '):
                continue  # Skip this blank line
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Join and ensure proper formatting
    content = '\n'.join(fixed_lines)
    
    # Parse and rewrite to ensure proper YAML structure
    try:
        data = yaml.safe_load(content)
        
        # Ensure specification text doesn't have embedded newlines
        if 'specification' in data and len(data['specification']) > 1:
            spec_text = data['specification'][1]
            # Remove double newlines and clean up
            spec_text = ' '.join(line.strip() for line in spec_text.split('\n') if line.strip())
            data['specification'][1] = spec_text
        
        # Write back with proper formatting
        with open(filepath, 'w') as f:
            f.write('%YAML 1.2\n---\n')
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            f.write('...\n')
        
        print(f"Fixed: {filepath}")
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == '__main__':
    # Fix all structure files
    structure_files = [
        'registry-yaml/structure/_OCUR.yaml',
        'registry-yaml/structure/_OCREF.yaml',
        'registry-yaml/structure/_PART.yaml',
        'registry-yaml/structure/_PRESENCE.yaml',
        'registry-yaml/structure/_ATTR.yaml'
    ]
    
    for filepath in structure_files:
        if os.path.exists(filepath):
            fix_yaml_file(filepath)
        else:
            print(f"File not found: {filepath}")