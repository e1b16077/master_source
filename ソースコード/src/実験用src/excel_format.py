##########################################################
#  課題ごと #
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
    '../データベース作成（出席多いと削除）/' + a + '_pure+.xlsx', read_only=True)

# シートを取得
name = book.sheetnames
# log_sum = []
user_name = []
lec_sum = []

with pd.ExcelWriter('IC_jikken.xlsx', engine="openpyxl", mode="a") as writer:
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

            data_df2 = data_df.drop_duplicates(subset=['kadai_a'])
            count_list = []

            # 被っているファイル数をカウントしている
            for i in data_df2.itertuples():
                count_list.append(
                    len(data_df[data_df['kadai_a'] == i.kadai_a]))

            s = pd.Series(count_list, name="ファイル数")

            s = s.reset_index()
            data_df2 = data_df2.reset_index()

            df_s = pd.concat([data_df2, s], axis=1)
            # lec_sum.append(len(data_df))
            df_s['label'] = ''
            df_s = df_s.rename(columns={'kadai_a': '課題名'})
            df_s = df_s[["SID", "time", "kadai", "contents",
                         "sumletter", "diff_sumletter", "loc", "diff_loc", "再編集時期", "ファイル数", "lecname",  "課題名", "label"]]

            if len(df_s) > 0:
                df_s.to_excel(writer, sheet_name=name[j+1])
        except IndexError:
            break
