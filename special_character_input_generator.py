#!python3.6
# -=- encoding: utf-8 -=-
from pathlib import Path


def define_bindings(a):
    # diaeresis or umlauts
    a('"A',              'Ä')
    a('"a',              'ä')
    a('"E',              'Ë')
    a('"e',              'ë')
    a('"I',              'Ï')
    a('"i',              'ï')
    a('"O',              'Ö')
    a('"o',              'ö')
    a('"U',              'Ü')
    a('"u',              'ü')
    a('"Y',              'Ÿ')
    a('"y',              'ÿ')

    # acutes
    a("'A",              'Á')
    a("'a",              'á')
    a("'C",              'Ć')
    a("'c",              'ć')
    a("'E",              'É')
    a("'e",              'é')
    a("'I",              'Í')
    a("'i",              'í')
    a("'O",              'Ó')
    a("'o",              'ó')
    a("'U",              'Ú')
    a("'u",              'ú')
    a("'Y",              'Ý')
    a("'y",              'ý')

    # graves
    a("`A",              'À')
    a("`a",              'à')
    a("`E",              'È')
    a("`e",              'è')
    a("`I",              'Ì')
    a("`i",              'ì')
    a("`O",              'Ò')
    a("`o",              'ò')
    a("`U",              'Ù')
    a("`u",              'ù')

    # tildes
    a('~A',              'Ã')
    a('~a',              'ã')
    a('~N',              'Ñ')
    a('~n',              'ñ')
    a('~O',              'Õ')
    a('~o',              'õ')

    # circumflexes
    a('^A',              'Â')
    a('^a',              'â')
    a('^E',              'Ê')
    a('^e',              'ê')
    a('^I',              'Î')
    a('^i',              'î')
    a('^O',              'Ô')
    a('^o',              'ô')
    a('^U',              'Û')
    a('^u',              'û')

    # carons
    a('vC',              'Č')
    a('vc',              'č')
    a('vS',              'Š')
    a('vs',              'š')
    a('vZ',              'Ž')
    a('vz',              'ž')

    # macrons
    a('^-A',             'Ā')
    a('^-a',             'ā')
    a('^-O',             'Ō')
    a('^-o',             'ō')

    # overrings
    a('oA',              'Å')
    a('oa',              'å')

    # stroked characters
    a('-D',              'Đ')
    a('-d',              'đ')

    # slashed characters
    a('/O',              'Ø')
    a('/o',              'ø')

    # cedillas
    a('?C',              'Ç')
    a('?c',              'ç')
    a('?S',              'Ş')
    a('?s',              'ş')

    # sharp s
    a('ss',              'ß')

    # combined characters
    a('AE',              'Æ')
    a('ae',              'æ')

    # misc letters
    a('alpha',           'α')
    a('beta',            'β')
    a('micro',           'µ')
    a('ohm',             'Ω')
    a('pi',              'π')

    # currency symbols
    a('cent',            '¢')
    a('euro',            '€')
    a('gbp',             '£')
    a('czk',             'Kč')
    a('plz',             'zł')
    a('thb',             '฿')
    a('egp',             'E£')
    a('jpy',             '¥')

    # misc symbols
    # guillemets
    a('< ',              '‹')
    a('> ',              '›')
    a('<<',              '«')
    a('>>',              '»')
    # quotes and double quotes
    a("l'",              '‘')
    a("r'",              '’')
    a('l"',              '“')
    a('r"',              '”')
    # inverted punctuation
    a('? ',              '¿')
    a('! ',              '¡')
    # typographic symbols
    a('section',         '§')
    a('para',            '¶')
    a('...',             '…')
    # IP symbols
    a('copyright',       '©')
    a('registered',      '®')
    a('trademark',       '™')
    # graphic symbols
    a('tick',            '✓')
    a('cross',           '✗')
    a('checkboxcross',   '☒')
    a('checkboxempty',   '☐')
    # maths symbols
    a('+-',              '±')
    a('*x',              '×')
    a('*.',              '·') # aka interpunct
    a('//',              '÷')
    a('<=',              '≤')
    a('>=',              '≥')
    a('degrees',         '°')
    a('superscript1',    '¹')
    a('squared',         '²')
    a('cubed',           '³')

    # whitespace
    # word joiner (a zero width character)
    a(' ',               '⁠')

    # special help link
    a('help',            'HELP')



# create a binding dict
bindings={}
def add_binding(binding,string):
    if binding in bindings: raise Exception(f'duplicate: {binding}={string} and {bindings[binding]}')
    bindings[binding]=string
define_bindings(add_binding)


# build tree of characters
bm={}
for k,v in bindings.items():
    m=bm
    for l in k:
        if l in m:
            m=m[l]
        else:
            m[l]={}
            m=m[l]
    m['']=v


# build help text (in cpython3.6 dicts keep insertion order, in py3.7+ it's a language feature, so help text will be generated in insertion order)
help_text=[]
last=''
for k,v in bindings.items():
    help_text.append(f'{k}={v}\t')
help_text=''.join(help_text)


# output the AHK code
with Path(r'specialCharacterInputBinding.ahk').open('w',encoding='utf-8') as fout:
    fout.write('^\::\n')

    # recursively output conditionals
    def output(prefix,m,depth):
        first=True
        indent='\t'*depth
        else_str=''
        for k,v in sorted(m.items()):
            if k=='':
                if prefix=='help':
                    fout.write(f'{indent}GoSub SpecialCharacterInput_Help\n')
                else:
                    fout.write(f'{indent}Send, {v}\n')
                if len(m)>1:
                    raise Exception(f'overlap: termination of {v} is continued by {m}')
            else:
                escaped_k=k.replace('"','""').replace('`','``').replace('\n','`n')
                if first: fout.write('{}Input, key, L1\n'.format(indent))
                fout.write('{}{}If(key == "{}"){{\n'.format(indent,else_str,escaped_k))
                output(prefix+k,v,depth+1)
                fout.write('{}}}\n'.format(indent))
                first=False
                else_str='Else '
    output('',bm,1)
    fout.write('Return\n')

    # write the help function that pops up a message box when C-\ help is input
    fout.write(f'''
    SpecialCharacterInput_Help:
        Msgbox, 64, SpecialCharacterInput, {help_text}
    Return
    ''')


# and copy to my AHK script dir
AHK_SCRIPT_DIR=Path(r'D:\pe\apps-core\utils\AutoHotkey')
if AHK_SCRIPT_DIR.is_dir():
    # use copy2 to update mod time for pe git repo
    from shutil import copy2
    copy2('specialCharacterInputBinding.ahk',AHK_SCRIPT_DIR)
