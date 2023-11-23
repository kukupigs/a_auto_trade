# -- coding: utf-8 --
""":authors:
    zhuxiaohu
:create_date:
    2023/10/19 18:14
:last_date:
    2023/10/19 18:14
:description:

"""
import numpy as np
import pandas as pd
import talib

from StrategyExecutor.MyTT import *
from StrategyExecutor.common import load_data


def gen_multiple_daily_buy_signal_fix(data, key, value_list):
    """
    产生公共结构的买入信号
    列如:
        涨跌幅大于或者小于固定的值1 3 5等，或者是大于或者小于5 10 20平均数的值
    :param ma_list:
    :param data:
    :return:
    """

    # 产生固定值的区间信号
    if value_list:
        sorted_values = sorted(value_list)

        # 为每个区间创建列
        for i in range(len(sorted_values)):
            if i == 0:
                # 处理小于第一个值的情况
                column_name = f'{key}_小于_{sorted_values[i]}_固定区间_signal'
                data[column_name] = data[key] < sorted_values[i]
            else:
                # 处理区间值
                lower = sorted_values[i - 1]
                upper = sorted_values[i]
                column_name = f'{key}_{lower}_到_{upper}_固定区间_signal'
                data[column_name] = data[key].apply(lambda x: lower <= x < upper)

        # 处理大于最后一个值的情况
        column_name = f'{key}_大于_{sorted_values[-1]}_固定区间_signal'
        data[column_name] = data[key] > sorted_values[-1]

    return data

def gen_multiple_daily_buy_signal_ma(data, key, ma_list):
    """
    产生公共结构的买入信号
    列如:
        涨跌幅大于或者小于固定的值1 3 5等，或者是大于或者小于5 10 20平均数的值
    :param ma_list:
    :param data:
    :return:
    """

    # 产生平均值的区间信号
    if ma_list:
        for value in ma_list:
            column_name = f'{key}_大于_{value}_日均线_signal'
            data[column_name] = data[key] > data[key].rolling(window=value).mean()
            column_name = f'{key}_小于_{value}_日均线_signal'
            data[column_name] = data[key] <= data[key].rolling(window=value).mean()

    # 创建一个空的 DataFrame 用于存储新列
    new_columns = pd.DataFrame(index=data.index)
    # 使用 pd.concat 将新列添加到原始 DataFrame
    data = pd.concat([data, new_columns], axis=1)

    return data

def gen_multiple_daily_buy_signal_max_min(data, key, max_min_list):
    """
    产生公共结构的买入信号
    列如:
        涨跌幅大于或者小于固定的值1 3 5等，或者是大于或者小于5 10 20平均数的值
    :param ma_list:
    :param data:
    :return:
    """
    # 产生极值的信号
    if max_min_list:
        for value in max_min_list:
            # 计算大极值信号并作为新列
            column_name_max = f'{key}_{value}日_大极值signal'
            data[column_name_max] = data[key] == data[key].rolling(window=value).max()

            # 计算小极值信号并作为新列
            column_name_min = f'{key}_{value}日_小极值_signal'
            data[column_name_min] = data[key] == data[key].rolling(window=value).min()
    return data

def gen_basic_daily_buy_signal_1(data):
    """
    收盘值相关买入信号，一个是固定值，另一个是均线，还有新低或者新高
    :param data:
    :return:
    """

    data = gen_multiple_daily_buy_signal_fix(data, '收盘', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_ma(data, '收盘', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_max_min(data, '收盘', [5, 10, 20])
    return data


def gen_basic_daily_buy_signal_2(data):
    """
    换手率相关买入信号，一个是固定值，另一个是均线，还有新低或者新高
    :param data:
    :return:
    """
    data = gen_multiple_daily_buy_signal_fix(data, '换手率', [0.5, 5, 10])
    data = gen_multiple_daily_buy_signal_ma(data, '换手率', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_max_min(data, '换手率', [5, 10, 20])
    return data


def gen_basic_daily_buy_signal_3(data):
    """
    阴线或者阳线
    :param data:
    :return:
    """
    data['实体_阴线_signal'] = data['收盘'] <= data['开盘']
    data['实体_阳线_signal'] = data['收盘'] >= data['开盘']
    return data


def gen_basic_daily_buy_signal_4(data):
    """
    阴线或者阳线
    :param data:
    :return:
    """
    data['日期_新股_100_signal'] = False
    data['日期_老股_100_signal'] = False
    # 将data['新股_100_signal']前100天的值赋值为True
    data.loc[0:100, '日期_新股_100_signal'] = True
    # 将data['老股_100_signal']100天的值赋值为True
    data.loc[100:, '日期_老股_100_signal'] = True
    return data


def gen_basic_daily_buy_signal_5(data):
    """
    开盘值相关买入信号，一个是固定值，另一个是均线，还有新低或者新高
    :param data:
    :return:
    """

    data = gen_multiple_daily_buy_signal_fix(data, '开盘', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_ma(data, '开盘', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_max_min(data, '开盘', [5, 10, 20])
    return data


def gen_basic_daily_buy_signal_6(data):
    """
    最高值相关买入信号，一个是固定值，另一个是均线，还有新低或者新高
    :param data:
    :return:
    """
    data = gen_multiple_daily_buy_signal_fix(data, '最高', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_ma(data, '最高', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_max_min(data, '最高', [5, 10, 20])
    return data


def gen_basic_daily_buy_signal_7(data):
    """
    最低值相关买入信号，一个是固定值，另一个是均线，还有新低或者新高
    :param data:
    :return:
    """
    data = gen_multiple_daily_buy_signal_fix(data, '最低', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_ma(data, '最低', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_max_min(data, '最低', [5, 10, 20])
    return data


def gen_basic_daily_buy_signal_8(data):
    """
    涨跌幅相关买入信号，一个是固定值，另一个是均线，还有新低或者新高
    :param data:
    :return:
    """
    data = gen_multiple_daily_buy_signal_fix(data, '涨跌幅', [-5, 0, 5])
    data = gen_multiple_daily_buy_signal_ma(data, '涨跌幅', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_max_min(data, '涨跌幅', [5, 10, 20])
    return data


def gen_basic_daily_buy_signal_9(data):
    """
    振幅相关买入信号，一个是固定值，另一个是均线，还有新低或者新高
    :param data:
    :return:
    """
    data = gen_multiple_daily_buy_signal_fix(data, '振幅', [2, 5, 10])
    data = gen_multiple_daily_buy_signal_ma(data, '振幅', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_max_min(data, '振幅', [5, 10, 20])
    return data

def gen_basic_daily_buy_signal_10(data):
    """
    MACD相关买入信号，一个是固定值，另一个是均线，还有新低或者新高
    :param data:
    :return:
    """
    MACD, MACD_Signal, MACD_Hist = talib.MACD(data['收盘'], fastperiod=12, slowperiod=26,
                                                                      signalperiod=9)
    data['BAR'] = (MACD - MACD_Signal) * 2
    data = gen_multiple_daily_buy_signal_ma(data, 'BAR', [5, 10, 20])
    data = gen_multiple_daily_buy_signal_max_min(data, 'BAR', [5, 10, 20])
    return data

