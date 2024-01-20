import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

filepath = 'Final_features.csv'

# 读取数据集
df = pd.read_csv(filepath)

# 处理缺失值
df = df.dropna(subset=['win_or_lose'])

# 选择特征和目标变量
features = df[['attack_scores', 'attack_errors', 'block_effective', 'block_errors',
               'dig_succeeded', 'dig_errors', 'reception_succeeded', 'reception_errors',
               'serve_scores', 'serve_errors']]
target = df['win_or_lose']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 创建K最近邻分类器
knn_classifier = KNeighborsClassifier()

# 设置网格搜索参数
param_grid_knn = {
    'n_neighbors': [3, 5, 7, 9],
    'weights': ['uniform', 'distance'],
    'p': [1, 2]
}

# 执行网格搜索
grid_search_knn = GridSearchCV(knn_classifier, param_grid_knn, cv=3)
grid_search_knn.fit(X_train_scaled, y_train)

# 获取最佳模型和参数
best_knn_model = grid_search_knn.best_estimator_
best_params_knn = grid_search_knn.best_params_

# 在测试集上进行预测
y_pred = best_knn_model.predict(X_test_scaled)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)

# 计算其他评估指标
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print("K-Nearest Neighbors Classifier:")
print("Best Parameters:", best_params_knn)
print("Accuracy:", accuracy)
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", class_report)

# 可视化参数网格搜索过程
cv_results = pd.DataFrame(grid_search_knn.cv_results_)[['param_n_neighbors', 'param_weights', 'param_p', 'mean_test_score']]
pivot_table = cv_results.pivot_table(index=['param_weights', 'param_n_neighbors'], columns='param_p', values='mean_test_score')

plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', cbar=True)
plt.title('GridSearchCV - Mean Test Score for Each Parameter Combination')
plt.tight_layout()
plt.show()
