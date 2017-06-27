# -*- coding: utf-8 -*-

class ColumnFreeTable(object):
    '''
    Table Object.
    
    Attributes
    ----------
    data : 2-dimension list
        1st dimension indicates the column
        2nd dimension indicates the index, with combined
            indexes grouped in a list
    colwidth : list of int
        Width of every column
    index : list
        every element is a list (indicating a column)
        with (colindex, indindex) tuples
    '''
    def __init__(self, data=[[]], colwidth=None, align='c'):
        self.data = data
        self.colwidth = colwidth
        self.align = align
        self.calc_index()

    def calc_index(self):
        self.index = []
        for col in range(len(self.data)):
            colindex = 0
            self.index.append([])
            for ind in self.data[col]:
                self.index[col] += [(colindex, i)
                    for i in range(len(ind))] + [None]
                colindex += 1
