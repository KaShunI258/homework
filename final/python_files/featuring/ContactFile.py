import pandas as pd

import os

# 指定下一级文件夹的名称
subfolder_name = 'New_data'
type_name = ['SCORING', 'ATTACK', 'BLOCK', 'SERVE', 'RECEPTION', 'DIG', 'SET']
years = ['2023', '2022', '2021']
# 生成文件路径
filepath = []
for i in range(7):
    for j in range(3):
        filepath.append(os.path.join(subfolder_name, f'Final_{type_name[i]}_{years[j]}.csv'))

"""
0 1 2 SCORING   3 4 5 ATTACK ,.etc
"""

# 读取文件
k = 0
for i in range(0,21,3):
    df1 = pd.read_csv(filepath[i])
    df2 = pd.read_csv(filepath[i+1])
    df3 = pd.read_csv(filepath[i+2])

    df_combined = pd.concat([df1, df2])
    df_combined = pd.concat([df_combined, df3])
    df_combined.to_csv(f'combined_{type_name[k]}.csv',index=False)
    k += 1
    # print(df_combined)