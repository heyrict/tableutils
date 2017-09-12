from tableutils.format.format import *
from tableutils.format.read import *

def read_grid(string, mode='strict', sepline_expr='[+|]-+[+|]', reset_linebreak=False):
    return GridTableReader(sepline_expr=sepline_expr,
            reset_linebreak=reset_linebreak).read(string)

def read_simple(string, mode='loose', sepline_expr='^[ -]*$', reset_linebreak=False):
    return SimpleTableReader(sepline_expr=sepline_expr,
            reset_linebreak=reset_linebreak).read(string)

def read_pipeline(string, mode='loose', sepline_expr='^[-:|]*$', reset_linebreak=False):
    return PipelineTableReader(sepline_expr=sepline_expr,
            reset_linebreak=reset_linebreak).read(string)


def to_grid(cft, boarder=2, maxwidth=90, newline_rate=1, halign='c', valign='c'):
    return GridTableTextFormatter(cft, boarder=boarder, newline_rate=newline_rate)\
                .to_txt(halign=halign, valign=valign)

def to_simple(cft, halign='c'):
    return SimpleTableTextFormatter(cft).to_txt(halign=halign)

def to_pipeline(cft, halign='c'):
    return PipelineTableTextFormatter(cft).to_txt(halign=halign)
