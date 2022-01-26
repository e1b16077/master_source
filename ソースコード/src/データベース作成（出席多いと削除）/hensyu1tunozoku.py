##########################################################
# 編集文字数一文字以下を削除したデータベースの中で1つの課題に対して編集が一度しか行われなかったものを削除する
####################################


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
    '01' + a + '.xlsx', read_only=True)
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

        # kadai名から_より前のものの列を追加する
        data_df['kadai_a'] = data_df['kadai'].apply(
            lambda x: re.sub(r'_.*', '', x))

        # 全てを大文字化（後から削除可能）
        data_df['kadai_a'] = data_df['kadai_a'].str.upper()

        # print('削除前\n', data_df["lecname"])

        # 大まかな流れとしては、kadai_aでグループ化して、それの長さが1以下の場合削除
        copy_df = data_df
        copy_df = copy_df.drop(copy_df.iloc[0:].index)
        # print(copy_df)
        for _, df_sub in data_df.groupby(['kadai_a', 'lecname']):
            if len(df_sub) > 1:
                copy_df = pd.concat([copy_df, df_sub])

        copy_df = copy_df.sort_values(['lecname', 'time'])

        # print("削除後\n", copy_df["lecname"].reset_index())

        copy_df = copy_df[["SID", "time", "lecname", "kadai", "contents",
                           "sumletter", "diff_sumletter", "loc", "diff_loc", "再編集時期"]]

        if len(copy_df) > 0:
            with pd.ExcelWriter('IN_saisyu.xlsx', engine="openpyxl", mode="a") as writer:
                copy_df.to_excel(writer, sheet_name=name[j+1])

    except IndexError:
        break
