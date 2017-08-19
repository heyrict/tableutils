tableutils
==========
A simple tool to create/read/edit grid tables and multi-line tables.

Dependencies
-----------
**require**
- python3

**recommend**
- pandoc

Installation
------------
No wheels yet.

Please soft-link the whole tableutils folder to python3 dist-package folder.
You may also want to alias `frontend.py` to a new name.

### Linux or Unix-like systems
```bash
$ ln -s /path/to/tableutils /path/to/python3/dist-package
$ # alias somename="/path/to/tableutils/frontend.py"
$
$ # if you don't know where dist-package folder is,
$ # try `/usr/local/lib/python3/dist-package`
$ # or  `/usr/lib/python3/dist-package`
```

### Windows
1. Copy tableutils folder to site-packages in your python folder (C:\Python* by default).
2. Add `frontend.py` to you path (or just copy it to python's bin\ folder)

Usage
-----
### General Usage

Assume we have a unformatted form file, say `temp.md`:

```
A team    B team
1         0
```
Note that all fields are separated by tabs or **over two** spaces.

To format it by tableutils frontend, use:
```bash
$ ./frontend.py -Ss temp.md  #convert temp.md from simple table to simple table (Format it).
 -------- -------- 
  A team   B team  
 -------- -------- 
    1        0
 -------- -------- 
```
```bash
$ ./frontend.py -Sg temp.md  #convert temp.md from simple table to grid table.
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
#### Grid Combination
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
Note: Only support grid combination of non-first row vertical siblings.

#### Automatical Line-change
```bash
$ ./frontend.py -Sg -%0.5 #(experimental)automatically add newline to long grids
Name     Sex      Class       Score    Comments
Rose     Female     1        100     I love you John
John      Male        1        100      I love you Rose
AlexanderII     Male     4    0      I am the greatest person ever on the world!!!
^D
+-------------+--------+-------+-------+-----------------+
|    Name     |  Sex   | Class | Score |    Comments     |
+=============+========+=======+=======+=================+
|    Rose     | Female |   1   |  100  | I love you John |
+-------------+--------+-------+-------+-----------------+
|    John     |  Male  |   1   |  100  | I love you Rose |
+-------------+--------+-------+-------+-----------------+
|             |        |       |       | I am the greate |
| AlexanderII |  Male  |   4   |   0   | st person ever  |
|             |        |       |       | on the world!!! |
+-------------+--------+-------+-------+-----------------+
```
#### Blank Grids
Try add `na` or `nan` to your simple table as a blank-grid indicator.
```bash
$ ./frontend.py -Sg
Name    Score
Rose    100
John    na
^D
+------+-------+
| Name | Score |
+======+=======+
| Rose |  100  |
+------+-------+
| John |       |
+------+-------+
```

### Extra Usage
Run `$ ./frontend.py --help` to get extra useful commands.

License
-------
Refer to ![LICENSE.md](./LICENSE.md).
