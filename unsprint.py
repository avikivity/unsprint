#!/usr/bin/python3

import sys
import re

def printf_to_fmt(x):
    out = ''
    i = 0;
    while i < len(x):
        def get():
            nonlocal i
            if i >= len(x):
                raise Exception('Trailing %: ' + x)
            c = x[i]
            i += 1
            return c
        c = get()
        if c == '%':
            c = get()
            if c in ('s', 'f', 'd'):
                out += '{}'
                continue
            raise Exception('Format not understood: ' + x)
        elif c == '{':
            out += '{{'
        else:
            out += c
    return out

regex = re.compile(r'\b(s?print\s*\(|fprint\s*\(\s*(\w+)\s*,\s*)(\s*")((?:[^"]|\\")+)',
                   re.DOTALL)
    
def unsprint(text):
    def replace(m):
        call = m.group(1)
        if call.startswith('fprint'):
            call = 'fmt::format_to(' + m.group(2) + ', '
        elif call.startswith('sprint'):
            call = 'format('
        else:
            call = 'fmt::format_to(std::cout, '
        format = m.group(4)
        format = printf_to_fmt(format)
        return call + m.group(3) + format + '"'
    return re.sub(regex, replace, text)

for fname in sys.argv[1:]:
    x = unsprint(open(fname).read())
    open(fname, 'w').write(x)
