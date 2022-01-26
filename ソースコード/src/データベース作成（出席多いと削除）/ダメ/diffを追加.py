# データベースの読み込み
import pandas as pd
import openpyxl
from datetime import datetime, time
import datetime as dt
import re
import difflib


# 読み込んだexcelのシート名取得
book = openpyxl.load_workbook(
    '../../database/大元のデータベース/IS.xlsx', read_only=True)
# シートを取得
name = book.sheetnames
count = 0
cnt = 0


for j in range(len(name)):
    try:
        sheet = book[name[j+1]]
        data = sheet.values
        data = list(data)
        data_df = pd.DataFrame(data[1:], columns=data[0])
        diff_subt = []

        data_df['kadai_b'] = data_df['kadai'].apply(
            lambda x: re.sub(r'_.*', '', x))
        # ここの時点で文字列差分を抽出しておく

        for _, df_sub in data_df.groupby(['lecname', 'kadai_b']):
            copy_df = df_sub
            # リストの初期化
            diff_subt.clear()

            for i in range(1000):
                try:
                    if i == 0:
                        diff_subt.append("")
                    else:
                        s1 = str(df_sub.iat[i-1, 5])
                        output1 = s1.split("\n,")

                        #########
                        # ここの時点で改行が適切に入っていることが確認された、ので改行をZAVAなどの文字列に置き換え差分を計算した後、改行\nに戻したら適切にできるのでは
                        s2 = str(df_sub.iat[i, 5])
                        output2 = s2.split("\n,")

                        d = difflib.Differ()
                        diff = d.compare(output1, output2)

                        # diff_su = '\n'.join(diff)
                        diff = '\n'.join(diff)

                        diff_subt.append(diff)

                except IndexError:
                    # diff_subt.append("")
                    break
            file_diff = pd.DataFrame(diff_subt, columns=["変更箇所"])
            copy_df = copy_df.reset_index()
            result = copy_df.join(file_diff)

            if count == 0:
                count += 1
                copy = result
                copy = copy_df.drop(copy_df.iloc[0:].index)

            copy = pd.concat([copy, result])

        if len(copy) > 0:
            with pd.ExcelWriter('IS_new.xlsx', engine="openpyxl", mode="a") as writer:
                copy.to_excel(writer, sheet_name=name[j+1])
        print(j)

    except IndexError:
        break
