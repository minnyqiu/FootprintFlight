# 读取最新上传的CSV文件
file_path = "FootPrint/merged_data.csv"
df = pd.read_csv(file_path)

# 设定新的起始时间戳
start_timestamp = 1691704563

# 计算时间增量（假设原时间戳是按顺序递增的，计算其间隔）
df['timestamp_diff'] = df['dataTime'].diff().fillna(0).astype(int)

# 重新生成时间戳
df['dataTime'] = start_timestamp + df['timestamp_diff'].cumsum()

# 删除辅助列
df.drop(columns=['timestamp_diff'], inplace=True)

# 保存修改后的文件
updated_file_path = "FootPrint/updated_merged_data.csv"
df.to_csv(updated_file_path, index=False)

# 展示修改后的数据
tools.display_dataframe_to_user(name="Updated Data", dataframe=df)
