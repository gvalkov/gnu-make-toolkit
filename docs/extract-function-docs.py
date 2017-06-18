#!/usr/bin/env python3

import sys
import json


def find_sections(lines):
    section = []
    in_section = False

    for line in lines:
        line = line.strip()

        if line.startswith('# >--') and line.endswith('->'):
            section[:] = []
            in_section = True
            continue

        if line.startswith('# <--') and line.endswith('-<'):
            in_section = False
            yield section
            continue

        if in_section:
            section.append(line.replace('# ', '', 1))


def find_parts(lines):
    parts = {}
    for line in lines:
        if not line.startswith(' '):
            part = parts.setdefault(line.rstrip(':'), [])
        else:
            part.append(line.strip())
    return parts


res = {}
for section in find_sections(sys.stdin):
    parts = find_parts(section)
    fname = parts['Function'][0].split()[0]
    res[fname] = parts


print(json.dumps(res, indent=2))
