# recode_day_difficultとは違いその人が編集時期に関係なくn回（1-13）以上編集していればいい
import pandas as pd
import openpyxl
from datetime import datetime, time
import matplotlib.pyplot as plt
li = ["IS", "IC", "IN"]
# グラフ化するときに必要
# ご本グラフにしたかったらここを調節する
x1 = [1.08, 2.08, 3.08]
x2 = [1.25, 2.25, 3.25]
x3 = [1.42, 2.42, 3.42]
lavel_x = ["授業中", "授業後から７日以内", "８日以上"]
all = [0, 0, 0]

print("何回レビュー後に編集している人を含みますか（1-13まで）デフォルトは1")
target = int(input())  # 要素0をmylistから取り除きたい
for k in range(3):
    # 読み込んだexcelのシート名取得
    book = openpyxl.load_workbook(
        '../../前後差分追加のみ/' + li[k] + '_前後差分追加だけ.xlsx', read_only=True)
    # シートを取得
    name = book.sheetnames
    jugyou = []
    toujitu_in_1week = []
    over_1week = []

    for j in range(len(name)):
        try:
            sheet = book[name[j+1]]
            data = sheet.values
            data = list(data)
            data_df = pd.DataFrame(data[1:], columns=data[0])

            # data_dfには学生一人一人のデータが順に格納されていく（for文によって）
            # # いつ編集しているのかを特定していく
            jugyou.append(
                len(data_df[data_df["再編集時期"] == "授業中"].drop_duplicates(subset=['lecname'])))
            toujitu_in_1week.append(
                len(data_df[(data_df["再編集時期"] == "授業日中") | (data_df["再編集時期"] == "翌日") | (
                    data_df["再編集時期"] == "一週間以内")].drop_duplicates(subset=['lecname'])))
            over_1week.append(
                len(data_df[data_df["再編集時期"] == "一週間以上"].drop_duplicates(subset=['lecname'])))

            # print(jugyou)
        except IndexError:
            break


    jugyou = [item for item in jugyou if item >= target]  # 取り除く＝それ以外を残す
    toujitu_in_1week = [
        item for item in toujitu_in_1week if item >= target]  # 取り除く＝それ以外を残す
    over_1week = [item for item in over_1week if item >=
                  target]  # 取り除く＝それ以外を残す
    # print(toujitu_in_1week)
    print(jugyou)
    all[k] = [len(jugyou), len(toujitu_in_1week), len(over_1week)]
# 1つ目の棒グラフ
print("IS人数", all[0])
print("IC人数", all[1])
print("IN人数", all[2])

# all[i]の中身がリストになっているため下のような特殊な割り方をしている
IS = list(map(lambda x: x/104, all[0]))
IC = list(map(lambda x: x/93, all[1]))
IN = list(map(lambda x: x/80, all[2]))

print("IS割合:", IS)
print("IC割合:", IC)
print("IN割合:", IN)
# 1つ目の棒グラフ
plt.xlabel('実施日時', fontsize=16, fontname="MS Gothic")
plt.ylabel('実施割合', fontsize=16, fontname="MS Gothic")
plt.bar(x1, IS, color='b', width=0.17, label='IS', align="center")
plt.bar(x2, IC, color='g', width=0.17, label='IC', align="center")
plt.bar(x3, IN, color='r', width=0.17, label='IN', align="center")
# 凡例
plt.legend(bbox_to_anchor=(1, 1), loc='upper right',
           borderaxespad=0, fontsize=12)

# X軸の目盛りを置換
plt.xticks([1.25, 2.25, 3.25], lavel_x, fontname="MS Gothic")
plt.show()
