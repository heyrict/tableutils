# -*- coding: utf-8 -*-

from tableutils.wcstring import wcstr
from tableutils.table import *
import re

class GridTableTextFormatter():
    def __init__(self, gt, boarder=2):
        self.gt = gt
        self.boarder = boarder

        if gt.colwidth: self.colwidth = self.gt.colwidth
        else: self.colwidth = self._calc_best_colwidth()
        self.colwidth = [i + self.boarder for i in self.colwidth]

    def to_txt(self):
        self.fillspace()
        self.put_index()
        self.put_data()

    def put_index(self):
        print('+','+'.join([(i)*'-' for i in self.colwidth]),'+',sep='')
        print('|','|'.join([''.join(i[0]) for i in self.gt.data]),'|',sep='')
        print('+','+'.join([(i)*'=' for i in self.colwidth]),'+',sep='')

    def _calc_best_colwidth(self, join_lines=True, maxwidth=90):
        # simple static functions
        avg = lambda x: sum(x) / len(x)
        std = lambda x: sum([(i - avg(x))**2 for i in x])

        # useful values
        # length_of_columns
        lc = [len(col) for col in self.gt.data]

        for col in range(len(self.gt.data)):
            self.gt.data[col] = [[wcstr('').join(i)] + [''] * (len(i) - 1)
                 for i in self.gt.data[col]]

        widths = [[len(self.gt.data[col][i[0]][i[1]]) if i else None
            for i in self.gt.index[col]] for col in range(len(self.gt.index))]
        colwidth = []

        for col in range(len(self.gt.data)):
            scw = sorted([i for i in widths[col] if i])
            diffs = [scw[i] - scw[i-1] for i in range(1,len(scw))]
            if std(scw) > 100 and scw[-1] > maxwidth/len(self.gt.data): 
                # calculate threshold
                thresh = 0; prev = -1
                for s in range(len(diffs)):
                    pres = sum([abs(diffs[i] - diffs[s]) for i in range(len(diffs))])
                    if pres > prev:
                        prev = pres
                        thresh = scw[s]
                thresh = int(max(thresh, widths[col][0], maxwidth/len(self.gt.data)))

                # change the form to correspond to new threshold
                origlen = [len(i) for i in self.gt.data[col]]
                self.gt.data[col] = [_auto_splitline(wcstr('').join(i), thresh=thresh)
                        for i in self.gt.data[col]] 
                self.gt.data[col] = [self.gt.data[col][i] + ['']*(origlen[i]-len(self.gt.data[col][i]))
                        * ((origlen[i]-len(self.gt.data[col][i]))>0)
                        for i in range(len(self.gt.data[col]))]
                preslen = [len(i) for i in self.gt.data[col]]
                colwidth.append(thresh)
            else:
                colwidth.append(scw[-1])

        #print(widths, colwidth, sep='\n')
        return colwidth

    def fillspace(self):
        filled_data = self.gt.data
        align = list(self.gt.align)
        if len(align) < len(filled_data):
            align += (len(filled_data) - len(align)) * [align[-1]]

        for col in range(len(filled_data)):
            filled_data[col] = [[_justify(i,self.colwidth[col],
                align[col]) for i in j] for j in filled_data[col]]

        return filled_data

    def put_data(self):
        colcounter = [1] * len(self.gt.data)
        indcounter = [0] * len(self.gt.data)
        bdrindic = []
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
            print('+' if bdrindic[0] else '|', end='')
            for col in range(len(self.gt.data)):
                print(nextline[col], end='')
                print('+' if (bdrindic[col] | bdrindic[col+1]) else '|', end='')
            print()

            nextline = []
            bdrindic = []


def _justify(string, width, align='c'):
    if align == 'l':
        return wcstr(string.ljust(width))
    elif align == 'r':
        return wcstr(string.rjust(width))
    else:
        return wcstr(string.center(width))


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
