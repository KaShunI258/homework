import pandas as pd

# 读取 'Final_features.csv' 文件
filepath = 'Final_features.csv'
df = pd.read_csv(filepath)

# avg 列
avg_columns = ['attack_scores', 'attack_errors', 'block_effective', 'block_errors',
               'dig_succeeded', 'dig_errors', 'reception_succeeded', 'reception_errors',
               'serve_scores', 'serve_errors']

# 去除 set=0 的行和包含 NaN 值的行
filtered_df = df[df['num_set'] > 0].dropna(subset=avg_columns)

# 按 Country 分组计算平均值
avg_values = filtered_df.groupby('Country')[avg_columns].mean().round(3)

print("平均值:")
print(avg_values)
avg_values.to_csv('avg_values.csv')