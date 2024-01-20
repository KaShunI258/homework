import pandas as pd

# 把七种表格按顺序读出
type_name = ['SCORING', 'ATTACK', 'BLOCK', 'SERVE', 'RECEPTION', 'DIG', 'SET']
years = ['2023', '2022', '2021']
df = []
for i in range(7):
    df.append(pd.read_csv(f'combined_{type_name[i]}.csv'))

filepath = 'Final_features.csv'

"""
选出有预测能力的特征列，包括以下特征：
每小局数据(11列)：
'attack_scores', 'attack_errors', 'block_effective'(scored and touch) , 'block_errors', 
'dig_succeeded', 'dig_errors', 'reception_succeeded', 'reception_errors',
'serve_scored', 'serve_errors', 'set_efficiency'(Point/Total),
每小局元信息(4列)：
'num_race', 'num_set', 'Country', 'win_or_lose'
"""
# 先构造包含这些特征列的新DataFrame。
feature_columns = ['num_race', 'num_set','Country', 'win_or_lose',
                   'attack_scores', 'attack_errors', 'block_effective' , 'block_errors',
                   'dig_succeeded', 'dig_errors', 'reception_succeeded', 'reception_errors',
                   'serve_scores', 'serve_errors', 'set_efficiency'
                   ]

features = pd.DataFrame(data=None, columns=feature_columns)


# 每种原始表格中需要的数据
selected_columns1 = ['Point', 'Errors', 'num_set', 'num_race', 'Country', 'win_or_lose']
selected_columns2 = ['Point', 'Errors', 'Touches', 'num_set', 'num_race', 'Country']
selected_columns3 = ['Point', 'Errors', 'num_set', 'num_race', 'Country']
selected_columns4 = ['Successful', 'Errors', 'num_set', 'num_race', 'Country']
selected_columns5 = ['Digs', 'Errors', 'num_set', 'num_race', 'Country']
selected_columns6 = ['Point', 'Total', 'num_set', 'num_race', 'Country']

# 统计Attack_scores 和 attack_errors (每小局)
# 需要ATTACK中的point 和 Errors

selected_columns = selected_columns1
# 现在 df[1] 中 'Point' 和 'Errors' 列应该只包含数字

df[1] = df[1][selected_columns].astype({'Point': int, 'Errors': int})

features_original = df[1].groupby(['num_race', 'num_set', 'Country'], as_index=False).agg({'Point':'sum', 'Errors':'sum', 'win_or_lose':'median'})
# print(list(features_original)[:10])

features['num_set'] = features_original['num_set']
features['num_race'] = features_original['num_race']
features['Country'] = features_original['Country']
features['attack_scores'] = features_original['Point']
features['attack_errors'] = features_original['Errors']
features['win_or_lose'] = features_original['win_or_lose']


# 统计block_effective'(scored and touch)和'block_errors'
df[2] = df[2][selected_columns2].astype({'Point': int, 'Errors': int, 'Touches':int})

df[2]['efficiency'] = 0
features_original2 = df[2].groupby(['num_race', 'num_set', 'Country'], as_index=False).agg({'Point':'sum', 'Errors':'sum','Touches':'sum'})  # 新建 efficiency 列并计算和})
features_original2['efficiency'] = features_original2['Point'] + features_original2['Touches']
features['block_effective'] = features_original2['efficiency']
features['block_errors'] = features_original2['Errors']

# print(features[:20]['block_effective'])


# 统计'serve_scored'和'serve_errors'
df[3] = df[3][selected_columns3].astype({'Point': int, 'Errors': int})

features_original3 = df[3].groupby(['num_race', 'num_set', 'Country'], as_index=False).agg({'Point':'sum', 'Errors':'sum'})

features['serve_scores'] = features_original3['Point']
features['serve_errors'] = features_original3['Errors']
# print(features[:20]['serve_errors'])

# 统计'reception_succeeded'和'reception_errors'
df[4] = df[4][selected_columns4].astype({'Successful': int, 'Errors': int})

features_original4 = df[4].groupby(['num_race', 'num_set', 'Country'], as_index=False).agg({'Successful':'sum', 'Errors':'sum'})

features['reception_succeeded'] = features_original4['Successful']
features['reception_errors'] = features_original4['Errors']
# print(features[:20]['reception_succeeded'])


# 统计'dig_succeeded'和'dig_errors'
df[5] = df[5][selected_columns5].astype({'Digs': int, 'Errors': int})

features_original5 = df[5].groupby(['num_race', 'num_set', 'Country'], as_index=False).agg({'Digs':'sum', 'Errors':'sum'})

features['dig_succeeded'] = features_original5['Digs']
features['dig_errors'] = features_original5['Errors']

# 统计set_efficiency
df[6] = df[6][selected_columns6].astype({'Point': int, 'Total': int})

df[6]['efficiency'] = 0
features_original6 = df[6].groupby(['num_race', 'num_set', 'Country'], as_index=False).agg({'Point':'sum', 'Total':'sum'})  # 新建 efficiency 列并计算和})
features_original6['efficiency'] = features_original6['Point'] / features_original6['Total']
features['set_efficiency'] = features_original6['efficiency'].round(3)

features.to_csv(filepath, index=False)