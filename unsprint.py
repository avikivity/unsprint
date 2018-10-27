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
            if c == '%':
                out += c
                continue
            stuff = ''
            while c not in 'xXcugodsfep':
                stuff += c
                c = get()
            if c != 's':
                stuff += c
            if stuff:
                if len(stuff) >= 2 and stuff[-2] in 'lL':
                    stuff = stuff[:-2] + stuff[-1]
                elif len(stuff) >= 3 and stuff[-3:-2] == 'll':
                    stuff = stuff[:-3] + stuff[-1]
                if stuff[-1] == 'u':
                    stuff = stuff[:-1] + 'd'
            if stuff:
                stuff = ':' + stuff
            out += '{' + stuff + '}'
            continue
        elif c == '{':
            out += '{{'
        else:
            out += c
    return out

regex = re.compile(r'(?<!fmt::)\b(s?print\s*\(|fprint\s*\(\s*(\w+)\s*,\s*)\s*"((?:[^"]|\\")+)',
                   re.DOTALL)
    
def unsprint(text):
    def replace(m):
        call = m.group(1)
        if call.startswith('fprint'):
            call = 'fmt_print(' + m.group(2) + ', '
        elif call.startswith('sprint'):
            call = 'format('
        else:
            call = 'fmt::print('
        format = m.group(3)
        format = printf_to_fmt(format)
        return call + '"' + format
    return re.sub(regex, replace, text)

for fname in sys.argv[1:]:
    x = unsprint(open(fname).read())
    open(fname, 'w').write(x)
