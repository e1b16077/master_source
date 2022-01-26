# 学生ごとにレビュー後に取り組んだlec数がtarget回以上のもをグラフ化している
import pandas as pd
import openpyxl
from datetime import datetime, time
import matplotlib.pyplot as plt
li = ["IN"]
# グラフ化するときに必要
# ご本グラフにしたかったらここを調節する
book = openpyxl.load_workbook(
    '../データベース作成（出席多いと削除）/' + li[0] + '_saisyu.xlsx', read_only=True)
# シートを取得
name = book.sheetnames
apeen = []
for j in range(len(name)):
    try:
        sheet = book[name[j+1]]
        data = sheet.values
        data = list(data)
        data_df = pd.DataFrame(data[1:], columns=data[0])

        list_sample = data_df['lecname'].to_list()
        list_sample = list(set(list_sample))
        print(len(list_sample))
        apeen.append(len(list_sample))
    except IndexError:
        break
    # print(jugyou)

plt.rcParams['font.size'] = 15
fig1, ax1 = plt.subplots()
# ax1.set_title('学科ごとのログ数')
ax1.set_xticklabels(['①'], fontname="MS Gothic")

# plt.title("授業に10回以上参加し1つの課題に対して2回以上編集している学生のレビュー後課題編集数の分布",
#           y=-0.23, fontname="MS Gothic")
# plt.title("クラス毎のレビュー後課題実施数",
#           y=-0.23, fontname="MS Gothic")
plt.subplots_adjust(bottom=0.2, top=0.95)

ax1.boxplot(apeen, sym="")
# ax1.boxplot(data2, sym="")
# ax1.boxplot(data3, sym="")
print(apeen)
plt.savefig("300_dpi_scatter.png", format="png", dpi=300)
# plt.show()


# print("IS割合:", IS)
# print("IC割合:", IC)
# print("IN割合:", IN)
# # 1つ目の棒グラフ
# plt.xlabel('実施日時', fontsize=16, fontname="MS Gothic")
# plt.ylabel('実施割合（人数）', fontsize=16, fontname="MS Gothic")
# plt.bar(x1, IS, color='b', width=0.17, label='A', align="center")
# plt.bar(x2, IC, color='g', width=0.17, label='B', align="center")
# plt.bar(x3, IN, color='r', width=0.17, label='C', align="center")
# # 凡例
# plt.legend(bbox_to_anchor=(1, 1), loc='upper right',
#            borderaxespad=0, fontsize=12)

# # X軸の目盛りを置換
# plt.xticks([1.25, 2.25, 3.25], lavel_x, fontname="MS Gothic")
# plt.show()
