# 各ラベルにどの程度の人数がいるのかをカウントする


# 学生ごとの修正ログ数
# データベースの読み込み
import pandas as pd
import openpyxl
from datetime import datetime, time
import re
print("どの学科にしますか")
a = input()
# 読み込んだexcelのシート名取得
book = openpyxl.load_workbook(
    a + '_jikken.xlsx', read_only=True)

# シートを取得
name = book.sheetnames
# log_sum = []
user_name = []
lec_sum = []
c1 = 0
c2 = 0
c3 = 0
c4 = 0
c5 = 0
c6 = 0
c71 = 0
c72 = 0
c8 = 0

for j in range(len(name)):
    try:
        sheet = book[name[j+1]]
        data = sheet.values
        data = list(data)
        data_df = pd.DataFrame(data[1:], columns=data[0])
        user_name.append(name[j+1])
        count = 0
        # print(data_df)
        # print(data_df[data_df['label'] == 1])
        if len(data_df[data_df['label'] == 1]) > 0:
            c1 += 1

        if len(data_df[data_df['label'] == 2]) > 0:
            c2 += 1

        if len(data_df[data_df['label'] == 3]) > 0:
            c3 += 1

        if len(data_df[data_df['label'] == 4]) > 0:
            c4 += 1

        if len(data_df[data_df['label'] == 5]) > 0:
            c5 += 1

        if len(data_df[data_df['label'] == 6]) > 0:
            c6 += 1

        if len(data_df[data_df['label'] == 71]) > 0:
            c71 += 1

        if len(data_df[data_df['label'] == 72]) > 0:
            c72 += 1

        if len(data_df[data_df['label'] == 8]) > 0:
            c8 += 1
    except IndexError:
        break
print("1,2,3,4,5,6,71,72,8")
print(c1, c2, c3, c4, c5, c6, c71, c72, c8)

print("1,2,3,4,5,6")
print(c1, c2 + c3 + c4, c6, c72, c8, c5 + c71 )
