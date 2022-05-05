import os
import subprocess
import numpy as np
import pandas as pd
from tqdm import tqdm


# child = subprocess.check_output('su2_cfd inv_NACA0012.cfg', cwd=r'C:\Users\23844\Desktop\SU2-master\QuickStart', shell=True)
# print(child)
# 获取cfg文件
def create_cfg(mesh_name):
    f = open('inv_NACA0012.cfg', 'r', encoding='utf-8')
    f1 = open('./Meshes/'+ mesh_name[:-4] + '.cfg', 'w', encoding='utf-8')
    lines = f.readlines()
    for i in range(len(lines)):
        if '2032c.su2' in lines[i]:
            new_line = lines[i].replace('2032c.su2', mesh_name)
            lines[i] = new_line
        elif 'CONV_FILENAME= history' in lines[i]:
            new_line = lines[i].replace('CONV_FILENAME= history', 'CONV_FILENAME= ' + mesh_name[:-4] + '_history')
            lines[i] = new_line
        elif 'VOLUME_FILENAME= flow' in lines[i]:
            new_line = lines[i].replace('VOLUME_FILENAME= flow', 'VOLUME_FILENAME= ' + mesh_name[:-4] + '_flow')
            lines[i] = new_line

    f1.writelines(lines)
    f.close()
    f1.close()

# file_list = os.listdir("./Meshes")
# np.savetxt("./Meshes/1.txt", file_list, fmt="%s")
file_list = np.loadtxt("./Meshes/1.txt", dtype=str)
for mesh_name in tqdm(file_list, desc='CL_CD_CFD'):
    # create_cfg(mesh_name)
    child = subprocess.check_output('su2_cfd ' + mesh_name[:-4] + '.cfg', cwd='./Meshes', shell=True)
    print(str(child, encoding='gbk'))
