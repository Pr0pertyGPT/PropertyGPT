from itertools import combinations
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# read the data from the csv file
file_path = 'src/res_analysis/path_to_save_results.csv' 
# we support the xlsx format,change to csv first
df = pd.read_csv(file_path)

# 选择的列名
selected_columns = ['生成数据_reference规则与生成规则自然语言相似度', # this is the similarity between the reference rule and the generated rule in natural language
                    '生成数据_reference规则函数代码与待测函数代码相似度', # this is the similarity between the reference rule function code and the tested function code in natural language
                    '生成数据_reference规则函数代码与待测函数代码自然语言相似度', # this is the similarity between the reference rule function code and the tested function code in natural language
                    '生成数据_reference规则与生成规则代码相似度',  # this is the similarity between the reference rule and the generated rule in code
                    '生成数据_groundtruth相似度'] # this is the similarity between the ground truth and the generated rule in code
df_selected = df[selected_columns]

# 目标变量
y = df_selected[selected_columns[-1]]

# 函数：计算给定特征组合的性能
def evaluate_feature_set(features):
    X_subset = df_selected[list(features)]
    X_train, X_test, y_train, y_test = train_test_split(X_subset, y, test_size=0.3, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    mde = np.mean(y_test - y_pred)
    adj_r2 = 1 - (1-r2)*(len(y_test)-1)/(len(y_test)-X_subset.shape[1]-1)

    # 归一化权重系数
    normalized_coefficients = model.coef_ / sum(model.coef_)
    return mae, mse, rmse, r2, mape, mde, adj_r2, normalized_coefficients

# 特征组合的所有可能性
all_combinations = []
for r in range(1, len(selected_columns)):
    all_combinations.extend(combinations(selected_columns[:-1], r))

# 评估每种组合
performance = {}
for combination in all_combinations:
    mae, mse, rmse, r2, mape, mde, adj_r2, normalized_coefficients = evaluate_feature_set(combination)
    performance[combination] = (mae, mse, rmse, r2, mape, mde, adj_r2, normalized_coefficients)

# 找到性能最好的特征组合（基于MAE）
best_features = min(performance, key=lambda x: performance[x][0])
best_metrics = performance[best_features]

# Output the results for the best feature combination
print(f"Best feature combination: {best_features}")
print("Performance metrics for the best feature combination:")
print(f"  Mean Absolute Error (MAE): {best_metrics[0]}")
print(f"  Mean Squared Error (MSE): {best_metrics[1]}")
print(f"  Root Mean Squared Error (RMSE): {best_metrics[2]}")
print(f"  Coefficient of Determination (R²): {best_metrics[3]}")
print(f"  Mean Absolute Percentage Error (MAPE): {best_metrics[4]}")
print(f"  Mean Deviation Error (MDE): {best_metrics[5]}")
print(f"  Adjusted R²: {best_metrics[6]}")
print(f"  Normalized Weight Coefficients: {best_metrics[7]}\n")

# Output the evaluation results for all other feature combinations
for combination, metrics in performance.items():
    print(f"Feature combination: {combination}")
    print(f"  Mean Absolute Error (MAE): {metrics[0]}")
    print(f"  Mean Squared Error (MSE): {metrics[1]}")
    print(f"  Root Mean Squared Error (RMSE): {metrics[2]}")
    print(f"  Coefficient of Determination (R²): {metrics[3]}")
    print(f"  Mean Absolute Percentage Error (MAPE): {metrics[4]}")
    print(f"  Mean Deviation Error (MDE): {metrics[5]}")
    print(f"  Adjusted R²: {metrics[6]}")
    print(f"  Normalized Weight Coefficients: {metrics[7]}\n")