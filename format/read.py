# -*- coding: utf-8 -*-

from tableutils.wcstring import wcstr
from tableutils.table import *
import re

class ColumnFreeTableReader(object):
    def __init__(self, sepline_expr='^[+-|]+$', reset_linebreak=False):
        self.sepline_expr = sepline_expr
        self.reset_linebreak = reset_linebreak

    def is_sepline(self, linestring):
        return bool(re.findall(self.sepline_expr, linestring))


class SimpleTableReader(ColumnFreeTableReader):
    def __init__(self, mode=None, *args, **kwargs):
        '''
        Parameters
        ----------
        mode : str
            strict : align-strict pandoc multi-line table
            loose  : align-loose table
        '''
        super(SimpleTableReader, self).__init__(*args, **kwargs)
        self.sepline_expr = '^[ -]*$'
        self.mode = mode

    def read(self, string):
        self.lines = [wcstr(i).strip() for i in string.split('\n')]

        if self.mode == None:
            if sum([bool(re.findall('^\s*-[- ]+-$', i)) for i in self.lines]) > 0:
                self.mode = "loose"
            else: self.mode = "strict"

        if self.mode == "strict":
            pass
        elif self.mode == "loose":
            return self.read_loose()
        else:
            raise ValueError('mode %s is not supported'%self.mode)

    def read_strict(self,vertical_split=[]):
        pass
    
    def read_loose(self):
        lines = [i.strip() for i in self.lines if not re.findall('^[ -]*$',i)]
        columns = re.split(' {2,}',lines[0])
        collen = len(columns)
        data = [re.split(' {2,}',i) for i in lines]
        data = [[j for j in i if j] for i in data]

        colcounter = [-1]*collen
        coldata = [[[]] for i in range(collen)]

        for i in range(len(data)):
            for c in range(collen):
                try:
                    if data[i][c] in '-|':
                        coldata[c][colcounter[c]] += ['','']
                        continue
                    else:
                        colcounter[c] += 1
                        if colcounter[c] != 0: coldata[c].append([])

                    if data[i][c] in ['na','nan','NA']:
                        coldata[c][colcounter[c]].append('')
                    else:
                        coldata[c][colcounter[c]].append(data[i][c])
                except:
                    colcounter[c] += 1
                    coldata[c].append([])
                    coldata[c][colcounter[c]].append('')

        return ColumnFreeTable(data=coldata)


class GridTableReader(ColumnFreeTableReader):
    def __init__(self, mode='strict', *args, **kwargs):
        super(GridTableReader, self).__init__(*args, **kwargs)
        self.mode = mode

    def read(self, string):
        self.lines = [wcstr(i).strip() for i in string.split('\n')]
        self.lines = [i for i in self.lines if i]

        seplines = [i for i in range(len(self.lines))
                if self.is_sepline(self.lines[i])]
        wordlines = [i for i in range(len(self.lines))
                if i not in seplines]

        vs = self._get_vertical_sep(seplines=seplines)

        if self.mode == 'strict': 
            return self.read_strict(vertical_split=vs)
        elif self.mode == 'loose':
            return self.read_loose(vertical_split=vs)
        else:
            raise ValueError('mode %s is not supported'%self.mode)

    def read_strict(self, vertical_split=[]):
        vs = vertical_split

        collen = len(vs) - 1
        colwidth=[vs[i+1] - vs[i] - 3 for i in range(collen)]

        colcounter = [-1] * collen
        coldata = [[] for i in range(collen)]

        # read lines
        for line in self.lines[:-1]:
            for col in range(collen):
                if self.reset_linebreak:
                    if re.findall('[-=]+',line[vs[col]+1:vs[col+1]]):
                        coldata[col].append([])
                        colcounter[col] += 1
                    else:
                        coldata[col][colcounter[col]].append(wcstr(''))
                        coldata[col][colcounter[col]][0] += line[vs[col]+1:vs[col+1]].strip()
                else:
                    if re.findall('[-=]+',line[vs[col]+1:vs[col+1]]):
                        coldata[col].append([])
                        colcounter[col] += 1
                    else:
                        coldata[col][colcounter[col]].append(line[vs[col]+1:vs[col+1]].strip())

        if self.reset_linebreak:
            return ColumnFreeTable(data=coldata)
        else:
            return ColumnFreeTable(data=coldata, colwidth=colwidth)


    def read_loose(self, vertical_split=[]):
        pass


    def _get_vertical_sep(self, seplines=[]):
        # get vertical separates
        vs = [False] * len(self.lines[seplines[0]])

        for i in seplines:
            i = self.lines[i]
            for j in range(len(i)):
                vs[j] |= (i[j]=='+')
        vsn = []
        for i in range(len(vs)):
            if vs[i]: vsn.append(i)

        return vsn
