from tableutils.format.format import *
from tableutils.format.read import *

def read_grid(string, sepline_expr='[+|]-+[+|]', reset_linebreak=False):
    return GridTableReader(sepline_expr=sepline_expr,
            reset_linebreak=reset_linebreak).read(string)


def to_grid(cft, boarder=2):
    return GridTableTextFormatter(cft, boarder=boarder).to_txt()
