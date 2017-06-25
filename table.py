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
    '''
    def __init__(self, data=[[]], colwidth=None, align='c'):
        self.data = data
        self.colwidth = colwidth
        self.align = align
