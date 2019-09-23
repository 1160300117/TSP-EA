import re
import numpy as np

fileaddr = "data/a280.tsp"

file_obejct = open(fileaddr)
# try:
#     for line in file_obejct:
#         print(line)
# finally:
#     file_obejct.close()
name = re.split(r'NAME : |\n', file_obejct.readline())[1]
comment = re.split(r'COMMENT : |\n', file_obejct.readline())[1]
_type = re.split(r'TYPE : |\n', file_obejct.readline())[1]
dimension = int(re.split(r'DIMENSION : |\n', file_obejct.readline())[1])
edge_weight_type = re.split(r'EDGE_WEIGHT_TYPE : |\n', file_obejct.readline())[1]
file_obejct.readline()
print(name, comment, _type, dimension, edge_weight_type)

pos = np.zeros((dimension, 3))
# print(pos)
#line = file_obejct.readline()
for i in range(dimension):
    a = list(filter(None, re.split(r' |\n', file_obejct.readline())))
    pos[i][0] = int(a[0])
    pos[i][1] = int(a[1])
    pos[i][2] = int(a[2])
    print(a)
print(pos)

