tableutils
==========
A simple tool to create/read/edit grid tables

Requirement
-----------
- python3

Installation
------------
Soft-link the whole tableutils folder to python3 dist-package folder.
You may also want to alias `frontend.py` to a new name.

### Linux
```bash
ln -s /path/to/tableutils /path/to/python3/dist-package
# if you don't know where dist-package folder is,
# try `/usr/local/lib/python3/dist-package`
```

### Windows
1. Copy tableutils folder to dist-package in your python folder (C:\Python* by default).
2. Add frontend.py to you path (or just copy it to python's bin\ folder)


Usage
-----
### General Usage

Assume we have a unformatted form file, say `temp.md`:

```
A team    B team
1         0
```
To format it by tableutils frontend, use:
```bash
$ ./frontend.py -Ss temp.md  #convert temp.md from simple table to simple table
 -------- -------- 
  A team   B team  
 -------- -------- 
    1        0
 -------- -------- 
```
```bash
$ ./frontend.py -Sg temp.md  #convert temp.md from simple table to grid table
+--------+--------+
| A team | B team |
+========+========+
|   1    |   0    |
+--------+--------+
```
```bash
$ ./frontend.py -rSg temp.md  
$ # convert temp.md from simple table to grid table and replace temp.md,
$ # equivalent to `$ ./frontend.py -Sg temp.md -o temp.md`.

$ ./frontend.py -cSg temp.md 
$ # convert temp.md from simple table to grid table and copy it to clipboard.
```
### Advanced Usage
Assume we have an unformatted table `temp2.md`:
```
Genre    Name     Score
Girls    Betty    99
-        Belly    98
Boys     Ben      100
-        Paul     95
-        Til      99
```
```bash
$ ./frontend.py -Sg -Hcl temp2.md # convert temp2.md with first align central, others left.
$ # `-` will be recognized as the same grid of the above one.
$ # control align by `-H` flag
+-------+-------+-------+
| Genre |Name   |Score  |
+=======+=======+=======+
|       |Betty  |99     |
| Girls +-------+-------+
|       |Belly  |98     |
+-------+-------+-------+
|       |Ben    |100    |
|       +-------+-------+
| Boys  |Paul   |95     |
|       +-------+-------+
|       |Til    |99     |
+-------+-------+-------+
```




Run `$ ./frontend.py --help` to get extra useful commands.

License
-------
Refer to ![License.md](./License.md).
