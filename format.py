import re

with open('tas_pythonetics/src/tas_pythonetics/paradata.py', 'r') as f:
    lines = f.readlines()

out_lines = []
for line in lines:
    out_lines.append(line.rstrip() + '\n')

with open('tas_pythonetics/src/tas_pythonetics/paradata.py', 'w') as f:
    f.writelines(out_lines)
