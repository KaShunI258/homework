import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
filepath = 'Final_features.csv'
df = pd.read_csv(filepath)

feature_columns = ['attack_scores', 'attack_errors', 'block_effective', 'block_errors',
                   'dig_succeeded', 'dig_errors', 'reception_succeeded', 'reception_errors',
                   'serve_scores', 'serve_errors', 'set_efficiency']

df = df.dropna()

# print(df)

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

X_train = train_df[feature_columns]

X_test = test_df[feature_columns]

# 训练集的标签
y_train = train_df['win_or_lose']

# 测试集的标签
y_test = test_df['win_or_lose']

# 数据标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 创建一个SVM分类器
clf = SVC(probability=True)

param_grid_svm = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'poly', 'rbf'],
    'gamma': ['scale', 'auto']
}
grid_search_svm = GridSearchCV(clf, param_grid_svm, cv=3)
grid_search_svm.fit(X_train_scaled, y_train)
best_params_svm = grid_search_svm.best_params_

# print(best_params_svm)
#  {'C': 10, 'gamma': 'scale', 'kernel': 'linear'}

best_clf = grid_search_svm.best_estimator_
best_clf.fit(X_train_scaled, y_train)

# 11. 在测试集上进行预测
y_pred = best_clf.predict(X_test_scaled)

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print("SVM:")
print("Best Parameters:", best_params_svm)
print("Accuracy:", accuracy)
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", class_report)

import seaborn as sns
cv_results = pd.DataFrame(grid_search_svm.cv_results_)[['param_C', 'param_kernel', 'param_gamma', 'mean_test_score']]
pivot_table = cv_results.pivot_table(index=['param_kernel', 'param_C'], columns='param_gamma', values='mean_test_score')

# 可视化参数网格搜索过程
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', cbar=True)
plt.title('GridSearchCV - Mean Test Score for Each Parameter Combination')
plt.tight_layout()
plt.show()