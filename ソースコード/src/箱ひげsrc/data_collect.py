##########################################################
#  授業回毎 #
####################################


# 学生ごとの修正ログ数
# データベースの読み込み
import pandas as pd
import openpyxl
from datetime import datetime, time
print("どの学科にしますか")
a = input()
# 読み込んだexcelのシート名取得
book = openpyxl.load_workbook(
    '../../database/一文字削除後/' + a + '_一文字以下削除済み.xlsx', read_only=True)
# シートを取得
name = book.sheetnames
# log_sum = []
user_name = []
lec_sum = []


for j in range(len(name)):
    try:
        sheet = book[name[j+1]]
        data = sheet.values
        data = list(data)
        data_df = pd.DataFrame(data[1:], columns=data[0])
        user_name.append(name[j+1])
        count = 0

        for _, df_sub in data_df.groupby(['lecname']):
            count = count + 1
        lec_sum.append(count)
    except IndexError:
        break

# log_sum = pd.DataFrame({a + '_sum_log': log_sum})
lec_sum = pd.DataFrame({a + '_lec_sum': lec_sum})
user_name = pd.DataFrame({a + '_use_name': user_name})
lec_sum = user_name.join(lec_sum)

# print(li[1][0:2])
# excelへ出力
if len(lec_sum) > 0:
    with pd.ExcelWriter('data.xlsx', engine="openpyxl", mode="a") as writer:
        lec_sum.to_excel(writer, sheet_name=a)
