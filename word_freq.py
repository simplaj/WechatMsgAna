import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import jieba
import numpy as np
from matplotlib import cm
from matplotlib.font_manager import FontProperties
from wordcloud import WordCloud
from pystopwords import stopwords as SP


def word(df):
    stopwords = set(list(SP()) + ['哈哈哈', '哈哈哈哈', '老师', '刚刚', '一点'])

    # 设置全局字体为中文字体
    plt.rcParams['font.sans-serif'] = ['SimSun']

    # 筛选出Type为1的聊天记录
    df_type_1 = df[df['Type'] == 1]

    # 准备数据
    sender_messages = df_type_1[df_type_1['IsSender'] == 1]['StrContent'].dropna().astype(str).tolist()
    receiver_messages = df_type_1[df_type_1['IsSender'] == 0]['StrContent'].dropna().astype(str).tolist()

    # 使用jieba进行分词
    sender_words = [word for msg in sender_messages for word in jieba.lcut(msg) if len(word) > 1 and word not in stopwords]
    receiver_words = [word for msg in receiver_messages for word in jieba.lcut(msg) if len(word) > 1 and word not in stopwords]

    total_words = sender_words + receiver_words

    # 创建文本
    text = " ".join(total_words)

    # 生成词云
    wordcloud = WordCloud(font_path='SIMSUN.TTC', background_color="white").generate(text)

    # 显示词云
    fig = plt.figure(dpi=400)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('./image/wordcloud.png')
    plt.clf()

    # 计算词频
    sender_word_counts = Counter(sender_words)
    receiver_word_counts = Counter(receiver_words)

    # 获取词频最高的50个词
    sender_top_50_counts = sender_word_counts.most_common(50)
    receiver_top_50_counts = receiver_word_counts.most_common(50)

    # 计算特异性指数
    def calculate_specificity(word, sender_count, receiver_count):
        return (sender_count - receiver_count) / (sender_count + receiver_count + 1e-5)

    # 计算每个词的特异性指数
    sender_specificity_indices = {}
    receiver_specificity_indices = {}
    for word, _ in set(sender_top_50_counts + receiver_top_50_counts):
        s_c = sender_word_counts.get(word, 0)
        r_c = receiver_word_counts.get(word, 0)
        sender_specificity_indices[word] = calculate_specificity(
            word,
            s_c,
            r_c
        )
        receiver_specificity_indices[word] = calculate_specificity(
            word,
            r_c,
            s_c
        )

    # 获取每组的最高特异性指数的前50个词，按特异性指数排序
    sender_top_50 = sorted(sender_specificity_indices.items(), key=lambda x: x[1], reverse=True)[:50]
    receiver_top_50 = sorted(receiver_specificity_indices.items(), key=lambda x: x[1], reverse=True)[:50]

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams['axes.unicode_minus']=False 

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    sender_words, sender_values = zip(*sender_top_50)
    receiver_words, receiver_values = zip(*receiver_top_50)
    # 获取颜色映射
    sender_cmap = cm.get_cmap('Blues')
    receiver_cmap = cm.get_cmap("Reds")

    # 取前50个词的特异性指数最小值和最大值
    sender_min, sender_max = min(sender_values), max(sender_values)
    receiver_min, receiver_max = min(receiver_values), max(receiver_values)

    # 发送者条形图
    colors = [sender_cmap((value-sender_min)/(sender_max-sender_min)) for value in sender_values]
    ax1.barh(sender_words, sender_values, color=colors)
    ax1.invert_yaxis() 
    ax1.set_title("Tian's Top 50", fontsize=15)
    ax1.set_xlabel('Index(%)', fontsize=13)

    # 接收者条形图
    colors = [receiver_cmap((value-receiver_min)/(receiver_max-receiver_min)) for value in receiver_values]
    ax2.barh(receiver_words, receiver_values, color=colors)
    ax2.invert_yaxis()
    ax2.set_title("Lin's Top 50", fontsize=15)
    ax2.set_xlabel('Index(%)', fontsize=13)

    plt.tight_layout()
    save_path = './image/word.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    
if __name__ == '__main__':
    # 读取数据
    df = pd.read_csv('./data/wechat_chat.csv')
    word(df)
    