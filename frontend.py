#!/usr/bin/env python3
import optparse,pyperclip,sys,os

from tableutils import *

class string():
    def __init__(self,*args,sep=' ',end='\n'):
        self.content = sep.join([str(i) for i in args])+end

    def read(self):
        return self.content

    def write(self,*args,sep=' ',end=''):
        self.content += sep.join([str(i) for i in args])+end


def main():
    opt = optparse.OptionParser()
    opt.add_option('-o','--output',dest='output',default=None,help='name of the outputfile.')
    opt.add_option('-v','--vim',dest='vim_edit',action='store_true',default=False,help='edit by vim')
    opt.add_option('-r','--in-place',dest='in_place',default=False,action='store_true',help='replace the file')
    #opt.add_option('-s','--squeeze',dest='squeeze',default=False,action='store_true',help='squeeze the form')
    opt.add_option('-n','--replace-na',dest='replace_na',default=False,action='store_true',help='replace na values by spaces (WARNING: THIS OPTION WILL PROBABLY MAKE OUTPUT UNCOMPATIBLE)')
    opt.add_option('-H',dest='halign',default='c',help='horizonal align: [l,c,r]')
    opt.add_option('-V',dest='valign',default='c',help='vertical align: [u,c,d]')

    opt.add_option('-%',dest='sq',default=1,help='squeeze rate for grid output')

    opt.add_option('-c','--to-clipboard',dest='to_clipboard',action='store_true',default=False,help='redirect output to clipboard')
    opt.add_option('-C','--from-clipboard',dest='from_clipboard',action='store_true',default=False,help='redirect input from clipboard')

    opt.add_option('-S','--from-simple',dest='from_format',default='simple',action='store_const',const='simple')
    opt.add_option('-s','--to-simple',dest='to_format',default='simple',action='store_const',const='simple')
    opt.add_option('-G','--from-grid',dest='from_format',action='store_const',const='grid')
    opt.add_option('-g','--to-grid',dest='to_format',action='store_const',const='grid')

    (options,args) = opt.parse_args()
    inp = args
    data = None
    mode = 'a'

    # input
    if len(inp) > 1: print('Error: More than one arguments passed'); return
    elif len(inp) == 0:
        instr = string()

        # get input
        if options.from_clipboard:
            instr.write(pyperclip.paste())
        elif options.vim_edit:
            try:
                os.system('touch /tmp/tableutils_edit.md')
                os.system('vim /tmp/tableutils_edit.md')
            except Exception as e: print('Error: No vim editor available'); return;
            with open('/tmp/tableutils_edit.md','r') as f:
                instr.write(f.read())
            #os.remove('/tmp/tableutils_edit.md')
        else:
            r = str(sys.stdin.readline())
            while r:
                instr.write(r)
                r = str(sys.stdin.readline())

        #try: data = df_format_read(instr.read(),replace_na=options.replace_na)
        try:
            if options.from_format == 'simple':
                data = read_simple(instr.read())
            elif options.from_format == 'grid':
                data = read_grid(instr.read())
            else:
                raise ValueError('From-format %s invalid'%options.from_format)
        except Exception as e: print(e); return

    else:
        with open(inp[0]) as f:
            #try: data = df_format_read(f.read(),replace_na=options.replace_na)
            try:
                if options.from_format == 'simple':
                    data = read_simple(f.read())
                elif options.from_format == 'grid':
                    data = read_grid(f.read())
                else:
                    raise ValueError('From-format %s invalid'%options.from_format)
            except Exception as e: print(e);return

    # output
    if options.in_place:
        mode = 'w'
        if options.vim_edit: options.output = '/tmp/tableutils_edit.md'
        elif len(inp)==0:
            print('Error: no file found for replace');return
        elif len(inp)>1:
            print('Error: More than one arguments passed');return
        if not options.output:
            options.output = inp[0]

    outstr = string()
    if options.to_clipboard == True:
        if options.to_format == 'grid':
            outstr.write(to_grid(data, halign=options.halign, valign=options.valign))
        elif options.to_format == 'simple':
            outstr.write(to_simple(data,no_symbol=options.replace_na, halign=options.halign))
        pyperclip.copy(outstr.read())
    else:
        if options.to_format == 'grid':
            outstr.write(to_grid(data, halign=options.halign, valign=options.valign, newline_rate=float(options.sq)))
        elif options.to_format == 'simple':
            outstr.write(to_simple(data,no_symbol=options.replace_na, halign=options.halign))

        if options.output:
            with open(options.output,mode) as f:
                f.write(outstr.read())
        else:
            print(outstr.read())

    return 0


if __name__=='__main__':
    main()
