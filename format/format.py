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

    def to_txt(self):
        self.auto_newline()
        self.fillspace()
        self.put_index()
        self.put_data()

    def put_index(self):
        print('+','+'.join([(i+self.boarder)*'-' for i in self.colwidth]),'+',sep='')
        print('|','|'.join([''.join(i[0]) for i in self.gt.data]),'|',sep='')
        print('+','+'.join([(i+self.boarder)*'=' for i in self.colwidth]),'+',sep='')

    def auto_newline(self):
        pass
    
    def _calc_best_colwidth(self):
        return [max([len(j) for j in sum(i,[])]) for i in self.gt.data]

    def fillspace(self):
        filled_data = self.gt.data
        align = list(self.gt.align)
        if len(align) < len(filled_data):
            align += (len(filled_data) - len(align)) * [align[-1]]

        for col in range(len(filled_data)):
            filled_data[col] = [[_justify(i,self.colwidth[col]+self.boarder,
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
                    nextline.append('-'*(self.boarder + self.colwidth[col]))
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

# def put_grid(gt, align='c'):
#     gt.autofmt(align=align)
# 
#     # column name first
#     print('+','+'.join([i*'-' for i in gt.colwidth]),'+',sep='')
#     print('|','|'.join([''.join(i[0]) for i in gt.data]),'|',sep='')
#     print('+','+'.join([i*'=' for i in gt.colwidth]),'+',sep='')
# 
#     colcounter = [1] * len(gt.data)
#     indcounter = [0] * len(gt.data)
#     bdrindic = []
#     nextline = []
# 
#     # the remaining parts
#     while(colcounter[0] < len(gt.data[0])):
#         for col in range(len(gt.data)):
#             if indcounter[col] >= len(gt.data[col][colcounter[col]]):
#                 nextline.append('-'*gt.colwidth[col])
#                 colcounter[col] += 1
#                 indcounter[col] = 0
#                 bdrindic.append(True)
#             else:
#                 nextline.append(gt.data[col][colcounter[col]][indcounter[col]])
#                 indcounter[col] += 1
#                 bdrindic.append(False)
#     
#         bdrindic.append(False)
#         print('+' if bdrindic[0] else '|', end='')
#         for col in range(len(gt.data)):
#             print(nextline[col], end='')
#             print('+' if (bdrindic[col] | bdrindic[col+1]) else '|', end='')
#         print()
# 
#         nextline = []
#         bdrindic = []
# 
#     return
