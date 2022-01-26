##########################################################
#  全クラス
####################################


# 学生ごとの修正ログ数
# データベースの読み込み
import pandas as pd
import openpyxl
from datetime import datetime, time
import re
import matplotlib.pyplot as plt

book = openpyxl.load_workbook(
    'data_pure+.xlsx', read_only=True)

# シートを取得
name = book.sheetnames
# log_sum = []
user_name = []
lec_sum = []

linking_list = []
class_name = ["IS", "IC", "IN"]

for j in range(len(name)):
    try:
        sheet = book[name[j+1]]
        data = sheet.values
        data = list(data)
        data_df = pd.DataFrame(data[1:], columns=data[0])
        user_name.append(name[j+1])
        count = 0

        a = data_df[class_name[j] + "_lec_sum"].to_list()
        # print(a)

        linking_list.append(a)

    except IndexError:
        break
print(linking_list)
IS = linking_list[0]
IC = linking_list[1]
IN = linking_list[2]

sum = IS + IC + IN

print(sum)
print(len(sum))

plt.rcParams['font.size'] = 15
fig1, ax1 = plt.subplots()
# ax1.set_title('学科ごとのログ数')
ax1.set_xticklabels(['全クラス合計（N=212）'], fontname="MS Gothic")

# plt.title("授業に10回以上参加し1つの課題に対して2回以上編集している学生のレビュー後課題編集数の分布",
#           y=-0.23, fontname="MS Gothic")
plt.title("全クラス合計のレビュー後課題実施数",
          y=-0.23, fontname="MS Gothic")
plt.subplots_adjust(bottom=0.2, top=0.95)

ax1.boxplot(sum, sym="")
plt.savefig("300_dpi_scatter.png", format="png", dpi=300)
plt.show()
