##########################################################
#  課題ごと #
####################################

# 学生ごとの修正ログ数
# データベースの読み込み
import pandas as pd
import openpyxl
from datetime import datetime, time
import re
import collections
import matplotlib.pyplot as plt

list_a = ["IN"]
# 読み込んだexcelのシート名取得
label_list = []
over = []
under = []
for gakka in list_a:
    book = openpyxl.load_workbook(
        '../../実験用src/' + gakka + '_jikken.xlsx', read_only=True)
    # シートを取得
    name = book.sheetnames
    user_name = []
    sum_label = 0
    flag = 0

    for j in range(len(name)):
        try:
            sheet = book[name[j+1]]
            data = sheet.values
            data = list(data)
            data_df = pd.DataFrame(data[1:], columns=data[0])
            user_name.append(name[j+1])
            count = 0

            if len(data_df) <= 1:
                under = under + data_df['label'].tolist()

            elif len(data_df) > 1:
                over = over + data_df['label'].tolist()

            # label_list = label_list + data_df['label'].tolist()

        except IndexError:
            break

# ラベルを複数持つものを修正
# label_list.remove("1,3")
# label_list = label_list + [1, 3]

# label_list.remove("1,4")
# label_list = label_list + [1, 4]


under_jisyo = collections.Counter(under)
over_jisyo = collections.Counter(over)
print("labelの確認")
print(under_jisyo.keys())
print(over_jisyo.keys())


en_label = []
en_value = []
# print(joui1.keys())
# print(kai1.keys())
# print(median1.keys())
# ソート
under_sort = sorted(under_jisyo.items(), key=lambda x: x[0], reverse=False)
over_sort = sorted(over_jisyo.items(), key=lambda x: x[0], reverse=False)

under_label = []
under_value = []


# タプルからそれぞれデータを抜き出す
for ji in under_sort:
    under_label.append(ji[0])
    under_value.append(ji[1])
print(under_label)
print("under ", under_value)


over_label = []
over_value = []


# タプルからそれぞれデータを抜き出す
for ji in over_sort:
    over_label.append(ji[0])
    over_value.append(ji[1])
print(over_label)
print("over", over_value)
# print(joui_value)


# print(median_value)

# 割合の計算
# length = len(joui)
# joui = list(map(lambda x: x/int(length)*100, joui_value))

# length = len(kai)
# kai = list(map(lambda x: x/int(length)*100, kai_value))

# length = len(median)
# median = list(map(lambda x: x/int(length)*100, median_value))
# print(joui)
# print(median)
# print(kai)
