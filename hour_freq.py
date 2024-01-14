import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd

# 读取数据
df = pd.read_csv('./data/wechat_chat.csv')

# 转换时间戳为日期时间格式
df['datetime'] = pd.to_datetime(df['StrTime'])

# 提取小时信息
df['hour'] = df['datetime'].dt.hour

# 计算每个小时的消息数量
hourly_counts = df.groupby('hour').size()

# 绘制每小时聊天次数的条形图
plt.figure(figsize=(12, 6))
hourly_counts.plot(kind='bar', color='skyblue', width=0.8)
plt.title('Hourly Chat Count Statistics')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Messages')
plt.xticks(rotation=0)  # 由于小时是0-23，没有重叠的风险，不需要旋转标签

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig('./image/hourly_chat_counts.png')
