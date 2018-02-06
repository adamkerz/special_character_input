#!python3.6
# -=- encoding: utf-8 -=-
import os


AHK_SCRIPT_DIR=r'D:\pe\apps-core\utils\AutoHotkey'


bindings={
    # diaeresis or umlauts
    '"A':'Ä',
    '"a':'ä',
    '"E':'Ë',
    '"e':'ë',
    '"I':'Ï',
    '"i':'ï',
    '"O':'Ö',
    '"o':'ö',
    '"U':'Ü',
    '"u':'ü',
    '"Y':'Ÿ',
    '"y':'ÿ',

    # acutes
    "'A":'Á',
    "'a":'á',
    "'C":'Ć',
    "'c":'ć',
    "'E":'É',
    "'e":'é',
    "'I":'Í',
    "'i":'í',
    "'O":'Ó',
    "'o":'ó',
    "'U":'Ú',
    "'u":'ú',
    "'Y":'Ý',
    "'y":'ý',

    # graves
    "`A":'À',
    "`a":'à',
    "`E":'È',
    "`e":'è',
    "`I":'Ì',
    "`i":'ì',
    "`O":'Ò',
    "`o":'ò',
    "`U":'Ù',
    "`u":'ù',

    # tildes
    '~A':'Ã',
    '~a':'ã',
    '~N':'Ñ',
    '~n':'ñ',
    '~O':'Õ',
    '~o':'õ',

    # circumflexes
    '^A':'Â',
    '^a':'â',
    '^E':'Ê',
    '^e':'ê',
    '^I':'Î',
    '^i':'î',
    '^O':'Ô',
    '^o':'ô',
    '^U':'Û',
    '^u':'û',

    # carons
    'vC':'Č',
    'vc':'č',
    'vS':'Š',
    'vs':'š',
    'vZ':'Ž',
    'vz':'ž',

    # overrings
    'oA':'Å',
    'oa':'å',

    # stroked characters
    '-D':'Đ',
    '-d':'đ',

    # slashed characters
    '/O':'Ø',
    '/o':'ø',

    # cedillas
    '?C':'Ç',
    '?c':'ç',
    '?S':'Ş',
    '?s':'ş',

    # sharp s
    'ss':'ß',

    # combined characters
    'AE':'Æ',
    'ae':'æ',

    # misc letters
    'alpha':'α',
    'beta':'β',
    'micro':'µ',
    'ohm':'Ω',
    'pi':'π',

    # currency symbols
    'cent':'¢',
    'euro':'€',
    'gbp':'£',
    'czk':'Kč',
    'plz':'zł',
    'thb':'฿',
    'egp':'E£',
    'jpy':'¥',

    # misc symbols
    '< ':'‹',
    '> ':'›',
    '>>':'»',
    '>>':'»',
    'l"':'“',
    'r"':'”',
    "l'":'‘',
    "r'":'’',
    '??':'¿',
    '!':'¡',

    '+-':'±',
    '*':'·',
    '//':'÷',
    'degrees':'°',
    'superscript1':'¹',
    'squared':'²',
    'cubed':'³',

    'section':'§',
    'para':'¶',
    '...':'…',

    'copyright':'©',
    'registered':'®',

    'tick':'✓',
    'cross':'✗',
    'checkboxcross':'☒',
    'checkboxempty':'☐',

    # whitespace
    # word joiner (a zero width character)
    ' ':'⁠',

    # special help link
    'help':'HELP',
}


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


# build help text
help_text=[]
last=''
for k,v in bindings.items():
    help_text.append(f'{k}={v}\t')
help_text=''.join(help_text)


# recursively output conditionals
fout=open('specialCharacterInputBinding.ahk','w',encoding='utf-8')
fout.write('^\::\n')
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
fout.write(f'''
SpecialCharacterInput_Help:
	Msgbox, 64, SpecialCharacterInput, {help_text}
Return
''')
fout.close()


# and copy to the AHK script dir
if os.path.isdir(AHK_SCRIPT_DIR):
    # use copy2 to update mod time for pe git repo
    from shutil import copy2
    copy2('specialCharacterInputBinding.ahk',AHK_SCRIPT_DIR)
