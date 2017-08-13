#!/usr/bin/env python3

import re
import json
from argparse import ArgumentParser, FileType
from jinja2 import Environment


p = ArgumentParser()
p.add_argument('template', type=FileType(), help='path to index.md jinja template')
p.add_argument('docsjson', type=FileType(), help='path to docs.json')
args = p.parse_args()

env = Environment()
docs = json.load(args.docsjson)
tmpl = env.from_string(args.template.read())


def highlight_symbols(value):
    return re.sub(r'(#t)', r'`\1`', value)

def func(name):
    data = docs[name]
    return tmpl_func.render(
        signature=data['Signature'],
        returns=data['Returns'],
        example=data['Example']
    )

env.globals['func'] = func
env.filters['hl'] = highlight_symbols

tmpl_func = env.from_string('''
### `{{signature}}`

**Returns:** {{returns | hl}}

```makefile
{{example}}
```
''')



print(tmpl.render())
