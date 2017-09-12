# -*- coding: utf-8 -*-

from wcstring import wcstr
import re

class PipelineTable(object):
    '''
    Pipeline Table Object.

    Attributes
    ----------
    data : 2-dimension list
        1st dimension indicates the column
        2nd dimension indicates the index, with combined
            indexes grouped in a list
    colwidth : list of int
        set width of every column
    '''
    def __init__(self, data=[[]], colwidth=None):
        self.data = data
        self.align = None
        if colwidth and len(data) == len(colwidth):
            self.colwidth = colwidth
        else:
            self.colwidth = [max([len(''.join(i)) for i in data])]

    def autofmt(self, boader=2, maxwidth=76, align='c'):
        if len(data) > len(align):
            align = align + align[-1] * (len(data) - len(align))
        self.align = align
        self.space_fill(align=align)

    def space_fill(self, align='c'):
        for col in range(len(self.data)):
            for ind in range(len(self.data[col])):
                if align[col] == 'l':
                    self.data[col][ind] = [wcstr(i).ljust(self.colwidth[col])
                            for i in self.data[col][ind]]
                if align[col] == 'r':
                    self.data[col][ind] = [wcstr(i).rjust(self.colwidth[col])
                            for i in self.data[col][ind]]
                else:
                    self.data[col][ind] = [wcstr(i).center(self.colwidth[col])
                            for i in self.data[col][ind]]


def read_pipeline(string, mode='strict'):
    '''
    Read a pipeline table.

    Parameters
    ----------
    string : str
        a string containing a pipeline table
    '''
    # differentiate wordlines and separating lines
    lines = [wcstr(i) for i in string.split('\n') if re.findall('^ *\|?.+\|? *',i)]
    seplines = [i for i in range(len(lines)) if re.findall(' *\|?[-:|]+\|? *',lines[i])]
    wordlines = [i for i in range(len(lines)) if i not in seplines]

    if len(seplines) != 1:
        raise ValueError("Multiple seplines detected") if len(seplines)>1 \
                else ValueError("No sepline detected")
    sepline = seplines[0]

    coldata = [[i for i in re.split(r"(?<!\\)\|", j) if i.strip()] for j in wordlines]
    colcount = len(coldata[0])

    # Check column length
    for i in len(coldata):
        if len(coldata[i]) < colcount:
            coldata[i].extend([""]*(colcount - len(coldata[i])))
        elif len(colcount[i]) > colcount:
            raise ValueError("Length of columns of data is larger than header")

    coldata = list(zip(*coldata))
    print(coldata)
    return PipelineTable(data=coldata)


def put_pipeline(pt, align='c'):
    '''
    Put down a pipeline table.

    Parameters
    ----------
    pt : PipelineTable
    align : str or iterable containing align characters
        'l' : left-aligned
        'r' : right-aligned
        'c' : centered
    '''
    pt.autofmt(align=align)

    # column name first
    print('|','|'.join([''.join(i[0]) for i in pt.data]),'|',sep='')
    print('|','|'.join([i*'-' for i in pt.colwidth]),'|',sep='')

    colcounter = [1] * len(pt.data)
    indcounter = [0] * len(pt.data)
    bdrindic = []
    nextline = []

    # the remaining parts
    while(colcounter[0] < len(pt.data[0])):
        for col in range(len(pt.data)):
            if indcounter[col] >= len(pt.data[col][colcounter[col]]):
                nextline.append('-'*pt.colwidth[col])
                colcounter[col] += 1
                indcounter[col] = 0
                bdrindic.append(True)
            else:
                nextline.append(pt.data[col][colcounter[col]][indcounter[col]])
                indcounter[col] += 1
                bdrindic.append(False)

        bdrindic.append(False)
        print('|', end='')
        for col in range(len(pt.data)):
            print(nextline[col], end='')
            print('|', end='')
        print()

        nextline = []
        bdrindic = []

    return
