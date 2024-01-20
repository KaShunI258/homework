import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

def load_avg_matrix(filepath):
    # 读取平均值 csv 文件
    avg_matrix = pd.read_csv(filepath)
    # 将 'Country' 列设置为索引
    avg_matrix.set_index('Country', inplace=True)
    return avg_matrix

def predict_match_result(country1, country2, avg_matrix, model):
    # 获取两个国家的平均值特征
    country1_features = avg_matrix.loc[country1].values.reshape(1, -1)
    country2_features = avg_matrix.loc[country2].values.reshape(1, -1)

    # 使用模型进行预测
    country1_win_prob = model.predict_proba(country1_features)[:, 1][0]
    country2_win_prob = model.predict_proba(country2_features)[:, 1][0]

    return country1_win_prob, country2_win_prob

# 读取原始数据
filepath_original = 'Final_features.csv'
df_original = pd.read_csv(filepath_original)

# 处理缺失值
df_original = df_original.dropna(subset=['win_or_lose'])

# 选择特征和目标变量
features_original = df_original[['attack_scores', 'attack_errors', 'block_effective', 'block_errors',
                                  'dig_succeeded', 'dig_errors', 'reception_succeeded', 'reception_errors',
                                  'serve_scores', 'serve_errors']]
target_original = df_original['win_or_lose']

# 训练SVM模型
scaler_original = StandardScaler()
features_scaled_original = scaler_original.fit_transform(features_original)

svm_model_original = SVC(probability=True)
svm_model_original.fit(features_scaled_original, target_original)

# 读取平均值 csv 文件
filepath_avg_matrix = 'avg_values.csv'
avg_matrix = load_avg_matrix(filepath_avg_matrix)

# 输入两个国家的名字
country1_name = input("请输入第一个国家的名字：")
country2_name = input("请输入第二个国家的名字：")

# 预测比赛结果
country1_win_prob, country2_win_prob = predict_match_result(country1_name, country2_name, avg_matrix, svm_model_original)

# 输出预测结果
print(f"{country1_name} 获胜概率: {country1_win_prob:.4f}")
print(f"{country2_name} 获胜概率: {country2_win_prob:.4f}")
