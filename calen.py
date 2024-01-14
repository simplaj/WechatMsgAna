import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from calendar import monthrange, day_name, month_name
import numpy as np
from datetime import datetime

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

# 循环处理每个月
for year in years:
    # 准备绘制
    fig, axes = plt.subplots(3, 4, figsize=(15, 6), dpi=400)  # 为每个月分配一个子图
    for i, ax in enumerate(axes.flatten()):
        month = i + 1
        # 获取该月的天数和第一天是周几
        first_weekday, num_days = monthrange(year, month)
        # 创建该月的日期列表
        dates = ["" for _ in range(first_weekday)] + list(range(1, num_days + 1))
        # 填充剩余的空间，以使所有子图具有相同的格式
        while len(dates) < 42:
            dates.append("")
        # 创建热力图数据
        # print(year, month)
        # print(date_counts.get(f'{year}-{month}-01', 0)
        data = np.array([date_counts.get(pd.Timestamp(year, month, day), 0) if isinstance(day, int) else 0 for day in dates])
        # print(data.reshape(6, 7))

        # 绘制热力图
        ax.imshow(data.reshape(6, 7), cmap=cmap, norm=norm)
        # 设置子图的标题为月份
        ax.set_title(month_name[month])
        # 隐藏坐标轴
        ax.set_xticks([])
        ax.set_yticks([])
        # 在每个单元格中标记日期
        for ind, date in enumerate(dates):
            ax.text(ind % 7, ind // 7, date, ha='center', va='center', fontsize=8)

    # 调整布局
    plt.tight_layout()
    # 保存图像
    plt.savefig(f'./image/calendar{year}.png')
    plt.close(fig)
