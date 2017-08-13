#!/usr/bin/env python3

import re
import sys
import json
import fileinput
import collections


def find_sections(lines):
    '''Extract lines between '# ---+->' and '# ---+-<' markers.'''
    section = []
    in_section = False

    for line in lines:
        line = line.strip()

        if line.startswith('# ---') and line.endswith('->'):
            section[:] = []
            in_section = True
            continue

        if line.startswith('# ---') and line.endswith('-<'):
            in_section = False
            yield '\n'.join(section)
            continue

        if in_section:
            section.append(line.replace('# ', '', 1))


def split_section(section):
    '''Return a mapping of section keys (i.e. 'Function:') to the
    lines contained between those keys'''
    keys = {}
    for line in section.splitlines():
        m = re.match(r'(\w+):(?:\s+(.*))?', line)
        if m:
            key, val = m.groups()
            key = keys.setdefault(key, [])

            if val:
                key.append(val)
        else:
            key.append(line.strip())
    return {k: '\n'.join(v) for k, v in keys.items()}


sections = find_sections(fileinput.input())
sections = map(split_section, sections)

result = collections.OrderedDict()
for section in sections:
    key = re.match(r'([\w_-]+)\(?', section['Function']).group(1)
    section['Signature'] = section['Function']
    del section['Function']
    result[key] = section

json.dump(result, sys.stdout, indent=True)
