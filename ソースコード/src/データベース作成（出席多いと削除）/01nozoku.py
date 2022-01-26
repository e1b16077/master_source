# diff_sumletterが-1,0,1のものを消すプログラム
import pandas as pd
import openpyxl
from datetime import datetime, time
import matplotlib.pyplot as plt

book = openpyxl.load_workbook('IN_after_review.xlsx', read_only=True)
# シートを取得
name = book.sheetnames
jugyou = []
toujitu = []
yokujitu = []
in_1week = []
over_1week = []

pre = 0
after = 0

for j in range(len(name)):
    try:
        sheet = book[name[j+1]]
        data = sheet.values
        data = list(data)
        data_df = pd.DataFrame(data[1:], columns=data[0])
        # data_dfには学生一人一人のデータが順に格納されていく（for文によって）

        data_df = data_df.query(
            'diff_sumletter < -1 or 1 < diff_sumletter')

        if len(data_df) == 0:
            continue

        if len(data_df) > 0:
            with pd.ExcelWriter('01IN.xlsx', engine="openpyxl", mode="a") as writer:
                data_df.to_excel(writer, sheet_name=name[j+1])

    except IndexError:
        break
