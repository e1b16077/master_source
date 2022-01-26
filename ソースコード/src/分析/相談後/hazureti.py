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
hazure = []

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

            if len(data_df) > 3:
                hazure = hazure + data_df['label'].tolist()

            # label_list = label_list + data_df['label'].tolist()

        except IndexError:
            break

# ラベルを複数持つものを修正
# label_list.remove("1,3")
# label_list = label_list + [1, 3]

# label_list.remove("1,4")
# label_list = label_list + [1, 4]

hazure_jisyo = collections.Counter(hazure)

print("labelの確認")
print(hazure_jisyo.keys())



en_label = []
en_value = []
# print(joui1.keys())
# print(kai1.keys())
# print(median1.keys())
# ソート
hazure_sort = sorted(hazure_jisyo.items(), key=lambda x: x[0], reverse=False)


hazure_label = []
hazure_value = []


# タプルからそれぞれデータを抜き出す
for ji in hazure_sort:
    hazure_label.append(ji[0])
    hazure_value.append(ji[1])
print(hazure_label)
print("under ", hazure_value)


over_label = []
over_value = []


# タプルからそれぞれデータを抜き出す

# print(joui_value)

