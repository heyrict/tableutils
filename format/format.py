# -*- coding: utf-8 -*-

from tableutils.wcstring import wcstr
from tableutils.table import *
from math import floor, ceil
import re

class GridTableTextFormatter():
    def __init__(self, gt, boarder=2, maxwidth=90, newline_rate=1, mincolwidth=0):
        self.gt = gt
        self.boarder = boarder
        self._resize_stack = []

        if gt.colwidth: self.colwidth = self.gt.colwidth
        else:
            self.colwidth = self._calc_best_colwidth(maxwidth,newline_rate)
            self._resize(self.colwidth)
        self.colwidth = [max([max([len(k) for k in i]+[mincolwidth]) for i in j]) for j in self.gt.data]
        self.colwidth = [i + self.boarder for i in self.colwidth]

    def to_txt(self, halign='c', valign='c'):
        out = ''
        self.fillspace(halign,valign)
        out += self.put_index()
        out += self.put_data()
        return out

    def put_index(self):
        out = ''
        out += '+'+'+'.join([(i)*'-' for i in self.colwidth])+'+\n'
        out += '|'+'|'.join([''.join(i[0]) for i in self.gt.data])+'|\n'
        out += '+'+'+'.join([(i)*'=' for i in self.colwidth])+'+\n'
        return out

    def _calc_best_colwidth(self, maxwidth=90, newline_rate=1):
        # no newline
        if newline_rate <= 0:
            self.gt.combine_grid()
            return [max([len(i[0]) for i in j]) for j in self.gt.data]
        # maxwidth shouldn't be too small
        if maxwidth < len(self.gt.data) * 5:
            maxwidth = len(self.gt.data) * 5

        # simple static functions
        avg = lambda x: sum(x) / len(x)
        var = lambda x: sum([(i - avg(x))**2 for i in x])

        # useful values
        # length_of_columns
        lc = [len(col) for col in self.gt.data]

        self.gt.combine_grid()

        widths = [[len(self.gt.data[col][i[0]][i[1]]) if i else None
            for i in self.gt.index[col]] for col in range(len(self.gt.index))]
        colwidth = []

        for col in range(len(self.gt.data)):
            scw = sorted([i for i in widths[col] if i])
            diffs = [scw[i] - scw[i-1] for i in range(1,len(scw))]
            if var(scw) > 1000*newline_rate and scw[-1] > maxwidth/len(self.gt.data):
                # calculate threshold
                thresh = 0; prev = -1
                for s in range(len(diffs)):
                    pres = sum([abs(diffs[i] - diffs[s]) for i in range(len(diffs))])
                    if pres > prev:
                        prev = pres
                        thresh = scw[s]
                thresh = int(max(thresh, widths[col][0], maxwidth/len(self.gt.data)))

                colwidth.append(thresh)
            else:
                colwidth.append(scw[-1])

        return colwidth

    def _resize(self, colwidth):
        # change the form to correspond to new threshold
        for col in range(len(colwidth)):
            thresh = colwidth[col]
            if max([len(i) for i in sum(self.gt.data[col],[])]) < thresh:
                continue
            else:
                for item in range(len(self.gt.data[col])):
                    self._resize_push(col, item, _auto_splitline(\
                            wcstr('').join(self.gt.data[col][item]), thresh=thresh))

        self._resize_exec()
        return

    def _resize_push(self, col, item, content):
        self._resize_stack.append((col,item,content))

    def _resize_exec(self):
        origshape = [_count_iter([i[0] for i in j if i]) for j in self.gt.index]

        while len(self._resize_stack) > 0 :
            i = self._resize_stack.pop()
            col = i[0]
            item = i[1]
            content = i[2]
            column_count_to_append = len(content) - origshape[col][item]

            if column_count_to_append <= 0:
                self.gt.data[col][item] = content + (len(self.gt.data[col][item]) - len(content)) * ['']
            else:
                # expand short columns
                current_index = self.gt.index[col].index((item, origshape[col][item]-1))
                to_be_appended_index = current_index + column_count_to_append
                expand_range = 1
                for c in range(len(origshape)):
                    if c == col: continue
                    try:
                        expand_range = max(expand_range, column_count_to_append - self.gt.index[c]\
                                [current_index:to_be_appended_index+1].index(None) + 1)
                    except ValueError:
                        continue

                for c in range(len(origshape)):
                    # handle lastone item error issue
                    try: item_to_expand = self.gt.index[c][current_index + expand_range - 1][0]
                    except: item_to_expand = -1
                    self.gt.data[c][item_to_expand] += ['']*expand_range

                self.gt.data[col][item] = content + (len(self.gt.data[col][item]) - len(content)) * ['']

    def fillspace(self, halign='c', valign='c'):
        filled_data = self.gt.data

        # fill align list
        halign = list(halign)
        if len(halign) < len(filled_data):
            halign += (len(filled_data) - len(halign)) * [halign[-1]]

        valign = list(valign)
        if len(valign) < len(filled_data):
            valign += (len(filled_data) - len(valign)) * [valign[-1]]

        self.halign = halign
        self.valign = valign

        # set align
        for col in range(len(filled_data)):
            for item in range(len(filled_data[col])):
                filled_data[col][item] = _vjustify(filled_data[col][item],
                        valign[col])

        for col in range(len(filled_data)):
            filled_data[col] = [[_justify(i,self.colwidth[col],
                halign[col]) for i in j] for j in filled_data[col]]

        return filled_data

    def put_data(self):
        out = ''
        colcounter = [1] * len(self.gt.data)
        indcounter = [0] * len(self.gt.data)
        bdrindic = []                           #boarder indicator
        nextline = []

        # the remaining parts
        while(colcounter[0] < len(self.gt.data[0])):
            for col in range(len(self.gt.data)):
                if indcounter[col] >= len(self.gt.data[col][colcounter[col]]):
                    nextline.append('-'*(self.colwidth[col]))
                    colcounter[col] += 1
                    indcounter[col] = 0
                    bdrindic.append(True)
                else:
                    nextline.append(self.gt.data[col][colcounter[col]][indcounter[col]])
                    indcounter[col] += 1
                    bdrindic.append(False)

            bdrindic.append(False)
            out += '+' if bdrindic[0] else '|'
            for col in range(len(self.gt.data)):
                out += nextline[col]
                out += '+' if (bdrindic[col] | bdrindic[col+1]) else '|'
            out += '\n'

            nextline = []
            bdrindic = []

        return out

class SimpleTableTextFormatter(GridTableTextFormatter):
    def __init__(self, gt, no_symbol=False, newline_rate=0, *args, **kwargs):
        self.no_symbol = no_symbol
        gt.combine_grid()
        super(SimpleTableTextFormatter, self).__init__(gt,
                newline_rate=newline_rate, *args, **kwargs)

    def put_index(self):
        out = ''
        out += ' '+' '.join([(i)*'-' for i in self.colwidth])+' \n'
        out += ' '+' '.join([''.join(i[0]) for i in self.gt.data])+' \n'
        out += ' '+' '.join([(i)*'-' for i in self.colwidth])+' \n'
        return out

    def put_data(self):
        out = ''
        colcounter = [1] * len(self.gt.data)
        indcounter = [0] * len(self.gt.data)
        nextline = []

        # the remaining parts
        while(colcounter[0] < len(self.gt.data[0])):
            for col in range(len(self.gt.data)):
                if indcounter[col] >= len(self.gt.data[col][colcounter[col]]):
                    nextline.append(' '*(self.colwidth[col]))
                    colcounter[col] += 1
                    indcounter[col] = 0
                else:
                    t = self.gt.data[col][colcounter[col]][indcounter[col]]
                    if self.no_symbol: nextline.append(t)
                    else: nextline.append(t if t.strip() else _justify('-',self.colwidth[col]))
                    indcounter[col] += 1

            out += ' '
            for col in range(len(self.gt.data)):
                out += nextline[col]
                out += ' '
            out += '\n'

            nextline = []
            bdrindic = []

        out = '\n'.join([i if not re.findall('^[ -]+$',i) else '' for i in out.split('\n')])
        out = out.rstrip() + '\n'
        out += ' '+' '.join([(i)*'-' for i in self.colwidth])+' \n'
        return out

    def to_txt(self, halign='c', valign='u'):
        for col in range(len(self.gt.data)):
            for item in range(len(self.gt.data[col])):
                t = self.gt.data[col][item]
                if ''.join(t) == '': self.gt.data[col][item] = ['na'] + [''] * (len(t)-1)
        return super(SimpleTableTextFormatter, self).to_txt(halign, valign)


class PipelineTableTextFormatter(GridTableTextFormatter):
    def __init__(self, gt, no_symbol=False, newline_rate=0, boarder=0, *args, **kwargs):
        self.no_symbol = no_symbol
        self.halign = None
        gt.combine_grid()
        super(PipelineTableTextFormatter, self).__init__(gt, boarder=boarder,
                newline_rate=newline_rate, mincolwidth=2, *args, **kwargs)

    def put_index(self):
        out = ''
        out += '|'+'|'.join([''.join(i[0]) for i in self.gt.data])+'|\n'
        if self.halign == None:
            out += '|'+'|'.join([(i)*'-' for i in self.colwidth])+'|\n'
        else:
            out += '|'+'|'.join([':'+(self.colwidth[i]-1)*'-' if self.halign[i]=='l'
                else (':'+(self.colwidth[i]-2)*'-'+':' if self.halign[i]=='c'
                    else (self.colwidth[i]-1)*'-'+':')
                for i in range(len(self.colwidth))])+'|\n'
        return out

    def put_data(self):
        out = ''
        colcounter = [1] * len(self.gt.data)
        indcounter = [0] * len(self.gt.data)
        nextline = []

        # the remaining parts
        while(colcounter[0] < len(self.gt.data[0])):
            for col in range(len(self.gt.data)):
                if indcounter[col] >= len(self.gt.data[col][colcounter[col]]):
                    nextline.append(' '*(self.colwidth[col]))
                    colcounter[col] += 1
                    indcounter[col] = 0
                else:
                    t = self.gt.data[col][colcounter[col]][indcounter[col]]
                    if self.no_symbol: nextline.append(t)
                    else: nextline.append(t if t.strip() else _justify('-',self.colwidth[col]))
                    indcounter[col] += 1

            out += '|'
            for col in range(len(self.gt.data)):
                out += nextline[col]
                out += '|'
            out += '\n'

            nextline = []
            bdrindic = []

        out = '\n'.join([i for i in out.split('\n') if not re.findall('^[ |-]+$',i) ])
        out = out.rstrip() + '\n'
        return out

    def to_txt(self, halign='c', valign='u'):
        for col in range(len(self.gt.data)):
            for item in range(len(self.gt.data[col])):
                t = self.gt.data[col][item]
                if ''.join(t) == '': self.gt.data[col][item] = ['na'] + [''] * (len(t)-1)
        return super(PipelineTableTextFormatter, self).to_txt(halign, valign)

def _justify(string, width, halign='c'):
    if halign == 'l':
        return wcstr(string.ljust(width))
    elif halign == 'r':
        return wcstr(string.rjust(width))
    else:
        return wcstr(string.center(width))

def _vjustify(item, valign='u'):
    itemlen = len(item)
    itemdata = [i for i in item if i]
    emptylen = itemlen - len(itemdata)

    if valign == 'u':
        return itemdata + emptylen * ['']
    elif valign == 'd':
        return emptylen * [''] + itemdata
    else:
        return floor(emptylen/2) * [''] + itemdata + ceil(emptylen/2) * ['']

def _auto_splitline(line, thresh=78, symbols=';:,.，。'):
    length = len(line)
    if length < thresh: return [line]
    halfsep = [int(length/(length//thresh+1)*(i+1)) for i in range(length//thresh)]
    if symbols:
        preferred_sep = sorted(list(set(i.end()-1 for i
            in re.finditer(r'['+symbols+']+[^\n]',line.dupstr())))+halfsep+[length])
    else:
        preferred_sep = list(range(length))

    th = thresh
    prev = th
    out = []
    for s in preferred_sep:
        while s > th:
            out.append(line[:prev-length])
            line = line[prev-length:]
            th += thresh
            prev = th
        else: prev = s

    out.append(line)

    return out


def _count_iter(it):
    '''
    count item in a given iterator.

    Parameters
    ----------
    string : iterable

    Examples
    --------
    >>> count_iter([1,1,2,2,2,3])
    {1: 2, 2: 3, 3: 1}

    >>> count_iter(['a','a','b','b','b','c'])
    {'a': 2, 'c': 1, 'b': 3}

    '''
    d = dict()
    allitems = set(it)
    for i in allitems:
        d[i] = it.count(i)
    return d
