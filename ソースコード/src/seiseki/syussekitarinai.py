# データベースの読み込み
import pandas as pd
import openpyxl
from datetime import datetime, time
import datetime as dt
import re
import difflib


# 読み込んだexcelのシート名取得
book = openpyxl.load_workbook(
    '../../database/大元のデータベース/IC.xlsx', read_only=True)
# シートを取得
name = book.sheetnames
count = 0
cnt = 0
li = []

with pd.ExcelWriter('kesseki2.xlsx', engine="openpyxl", mode="a") as writer:

    for j in range(len(name)):
        try:
            sheet = book[name[j+1]]
            data = sheet.values
            data = list(data)
            data_df = pd.DataFrame(data[1:], columns=data[0])
            conte = []
            after_diff = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            # lecから始まるものを抽出する
            test = data_df[data_df['lecname'].str.contains('lec')]

            # print(len(test))
            if test['lecname'].nunique() < 10:
                cnt += 1
                print(name[j+1], "を除外:lec数", test['lecname'].nunique())
                li.append(name[j+1])
            
    
        except IndexError:
            break
    
    s = pd.Series(li)
    
    s.to_excel(writer, sheet_name="na")