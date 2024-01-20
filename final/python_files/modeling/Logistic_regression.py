# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score
# from sklearn.preprocessing import StandardScaler
#
# # 读取数据集
# filepath = 'Final_features.csv'
# df = pd.read_csv(filepath)
#
# # 处理缺失值
# df = df.dropna()
#
# # 定义自变量和因变量
# features = df[['attack_scores', 'attack_errors', 'block_effective', 'block_errors',
#                'dig_succeeded', 'dig_errors', 'reception_succeeded', 'reception_errors',
#                'serve_scores', 'serve_errors']]
# target = df['win_or_lose']
#
# # 划分数据集为训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
#
# # 标准化数据
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)
#
# # 初始化逻辑回归模型
# logreg_model = LogisticRegression()
#
# # 训练模型
# logreg_model.fit(X_train_scaled, y_train)
#
# # 在测试集上进行预测
# y_pred = logreg_model.predict(X_test_scaled)
#
# # 计算模型的预测准确率
# accuracy = accuracy_score(y_test, y_pred)
#
# # 输出预测的正确率
# print("逻辑回归模型的预测准确率:", accuracy)

from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt

filepath = 'Final_features.csv'
df = pd.read_csv(filepath)

feature_columns = ['attack_scores', 'attack_errors', 'block_effective', 'block_errors',
                   'dig_succeeded', 'dig_errors', 'reception_succeeded', 'reception_errors',
                   'serve_scores', 'serve_errors', 'set_efficiency']

df = df.dropna()

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

X_train = train_df[feature_columns]
X_test = test_df[feature_columns]

y_train = train_df['win_or_lose']
y_test = test_df['win_or_lose']

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 创建一个逻辑回归模型
logreg_model = LogisticRegression()

param_grid_logreg = {
    'C': [0.1, 1, 10],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear']
}

grid_search_logreg = GridSearchCV(logreg_model, param_grid_logreg, cv=3)
grid_search_logreg.fit(X_train_scaled, y_train)
best_params_logreg = grid_search_logreg.best_params_

best_logreg_model = grid_search_logreg.best_estimator_
best_logreg_model.fit(X_train_scaled, y_train)

# 在测试集上进行预测
y_pred = best_logreg_model.predict(X_test_scaled)

# 计算其他评估指标
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print("Logistic Regression:")
print("Best Parameters:", best_params_logreg)
print("Accuracy:", accuracy)
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", class_report)

# 可视化参数网格搜索过程
cv_results = pd.DataFrame(grid_search_logreg.cv_results_)[['param_C', 'param_penalty', 'mean_test_score']]
pivot_table = cv_results.pivot_table(index=['param_penalty', 'param_C'], values='mean_test_score')

plt.figure(figsize=(8, 4))
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', cbar=True)
plt.title('GridSearchCV - Mean Test Score for Each Parameter Combination')
plt.tight_layout()
plt.show()