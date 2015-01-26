import string

def scrubhtml(s):
    s=s.replace('&','&amp;') # do this first or else things will really break
    r={
        '<'     : '&lt;',
        '>'     : '&gt;',
        '"'     : '&quot;',
        "'"     : '&#39;',
        '\n'    : ' ',
        '`'     : '&#96;',
        '!'     : '&#33;',
        '@'     : '&#64;',
        '$'     : '&#36;',
        '%'     : '&#37;',
        '('     : '&#40;',
        ')'     : '&#41;',
        '='     : '&#61;',
        '+'     : '&#43;',
        '{'     : '&#123;',
        '}'     : '&#124;',
        '['     : '&#91;',
        ']'     : '&#93;'
    }

    for c in r:
        s = s.replace(c,r[c])

    return s


if __name__ == '__main__':
    print scrubhtml(raw_input('String: '))

