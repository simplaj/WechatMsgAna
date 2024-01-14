import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def freq(df):
    # 转换时间戳为日期格式
    df['date'] = pd.to_datetime(df['StrTime']).dt.normalize()

    # 为每个消息创建月份和日期列
    df['month'] = df['date'].dt.to_period('M')
    df['day'] = df['date'].dt.strftime('%Y-%m-%d')  # 使用字符串格式保证标签正确显示

    # 计算每月和每日的消息数量
    monthly_counts = df.groupby('month').size()
    daily_counts = df.groupby('day').size().sort_index()

    # 创建图形大小
    plt.figure(figsize=(15, 10))  # 增加图形大小

    # 绘制每月聊天次数的直方图
    plt.subplot(2, 1, 1)
    monthly_counts.plot(kind='bar', color='skyblue', width=0.8)
    plt.title('Monthly Chat Count Statistics')
    plt.xlabel('Month')
    plt.ylabel('Number of Messages')
    plt.xticks(rotation=45)

    # 绘制每日聊天次数的直方图
    plt.subplot(2, 1, 2)
    daily_counts.plot(kind='bar', color='skyblue', width=0.8)
    plt.title('Daily Chat Count Statistics')
    plt.xlabel('Day')
    plt.ylabel('Number of Messages')

    # 由于日期可能很多，我们可以设置x轴标签显示的间隔
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    if len(daily_counts) > 30:  # 如果数据点超过30个，我们可以显示每15天的标签
        plt.xticks(ticks=np.arange(0, len(daily_counts), 15), labels=daily_counts.index[::15], rotation=45)
    else:  # 如果数据点不多，直接显示所有标签
        plt.xticks(rotation=90)

    # 调整布局
    plt.tight_layout()

    # 保存图像
    plt.savefig('./image/freq.png')


if __name__ == '__main__':
    # 读取数据
    df = pd.read_csv('./data/wechat_chat.csv')
    freq(df)