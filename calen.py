import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
from calendar import monthrange, month_name
import numpy as np
from datetime import datetime
import matplotlib.colors as mcolors

# 读取数据
df = pd.read_csv('./data/wechat_chat.csv')

# 转换时间戳为日期格式
df['date'] = pd.to_datetime(df['StrTime']).dt.date

# 计算每个日期的消息数量
date_counts = df.groupby('date').size()
date_counts.index = pd.to_datetime(date_counts.index)

# 获取年份
years = pd.to_datetime(df['StrTime']).dt.year.unique()  # 假设所有数据都在同一年

# 创建热力图的颜色映射
colors = ["#ffffff", "#ffcccc", "#ff9999", "#ff6666", "#ff3333", "#ff0000"]
cmap = mcolors.LinearSegmentedColormap.from_list("count_cmap", colors)
norm = mcolors.Normalize(vmin=0, vmax=date_counts.max())

# 创建一个新的图形，子图数量为年份数量 x 12（每年12个月）
fig, axes = plt.subplots(len(years) * 3, 4, figsize=(20, len(years) * 5), dpi=400)  # 调整子图布局

# 循环处理每个年份和每个月
for y_index, year in enumerate(years):
    for i in range(12):
        month = i + 1
        ax = axes[y_index * 3 + i // 4, i % 4]  # 计算当前子图的位置
        first_weekday, num_days = monthrange(year, month)
        dates = ["" for _ in range(first_weekday)] + list(range(1, num_days + 1))
        while len(dates) < 42:
            dates.append("")
        data = np.array([date_counts.get(pd.Timestamp(year, month, day), 0) if isinstance(day, int) else 0 for day in dates])
        ax.imshow(data.reshape(6, 7), cmap=cmap, norm=norm)
        ax.set_title(f'{month_name[month]} {year}')
        ax.set_xticks([])
        ax.set_yticks([])
        for ind, date in enumerate(dates):
            ax.text(ind % 7, ind // 7, str(date) if date else "", ha='center', va='center', fontsize=6)

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig(f'./image/calendar.png')
