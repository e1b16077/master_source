# データベースの読み込み
import pandas as pd
import openpyxl
from datetime import datetime, time
import datetime as dt
import re
import difflib


# 読み込んだexcelのシート名取得
book = openpyxl.load_workbook(
    '../../database/大元のデータベース/IN.xlsx', read_only=True)
# シートを取得
name = book.sheetnames
count = 0
cnt = 0
class_time = [datetime(2020, 10, 1, 9, 10), datetime(
    2020, 10, 8, 9, 10), datetime(2020, 10, 15, 9, 10), datetime(2020, 10, 22, 9, 10),
    datetime(2020, 10, 29, 9, 10), datetime(
        2020, 11, 12, 9, 10), datetime(2020, 11, 19, 9, 10),
    datetime(2020, 11, 26, 9, 10), datetime(
        2020, 12, 3, 9, 10), datetime(2020, 12, 10, 9, 10),
    datetime(2020, 12, 24, 9, 10), datetime(2021, 1, 7, 9, 10), datetime(2021, 1, 14, 9, 10)]


def diff(df, key1, key2):
    df[key1] = df[key1] - df[key1].shift()
    df[key2] = df[key2] - df[key2].shift()
    return df


with pd.ExcelWriter('IN_test_last.xlsx', engine="openpyxl", mode="a") as writer:

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
                continue
            # time列にmicrosecondが小数点以下999999や000001などがあるためそれらを四捨五入
            data_df["time"] = pd.to_datetime(data_df["time"])
            data_df["time"] = data_df["time"].dt.round("1s")

            # 時間でソートし元のsumletterを残しておく
            data_df = data_df.sort_values('time')
            hinan_sumletter = data_df["sumletter"]
            hinan_loc = data_df["loc"]

            # # 各授業回のデータを格納している
            # kadai名から_より前のものの列を追加する
            data_df['kadai_a'] = data_df['kadai'].apply(
                lambda x: re.sub(r'_.*', '', x))

            result = pd.concat([diff(df_sub, 'sumletter', 'loc') for _, df_sub in data_df.groupby(
                ['kadai_a', 'lecname'])])

            # 保険
            # result = pd.concat([diff(df_sub, 'sumletter', 'loc') for _, df_sub in data_df.groupby(
            #     ['kadai_a', 'lecname'])]).drop('kadai_a', axis=1)

            # sumletterをdiff_sumletterに変更しdiff_sumletterのnullを0にする。からのソート
            result = result.rename(
                columns={'sumletter': 'diff_sumletter', 'loc': 'diff_loc'})
            result["diff_sumletter"] = result["diff_sumletter"].fillna(0)
            result["diff_loc"] = result["diff_loc"].fillna(0)
            result = result.sort_values('time')
            result = result.join(hinan_sumletter)
            result = result.join(hinan_loc)

    # ######################### result内のcontentsのカンマを削除
            for i in result["contents"]:
                if len(str(i)) > 0:
                    i = str(i).replace("\n,", "\n")
                    conte.append(i)
                else:
                    # 最初は\nにしていた
                    conte.append("")

            result = result.drop('contents', axis=1)
            df_conte = pd.DataFrame(conte, columns=['contents'])
            df_conte = df_conte.replace("None", "")
            result["contents"] = df_conte

    # #####################ここでresultのclass_time以下のものを抽出しなければいけない
    # ステップ1:lec毎に抽出
    # ステップ2:lec毎にclass_time以降に始めているものを抽出
    # ステップ3:appendする(final)

            # 各授業回のデータを格納している
            lec1_data = result[result["lecname"] == "lec01"]
            lec2_data = result[result["lecname"] == "lec02"]
            lec3_data = result[result["lecname"] == "lec03"]
            lec4_data = result[result["lecname"] == "lec04"]
            lec5_data = result[result["lecname"] == "lec05"]
            lec6_data = result[result["lecname"] == "lec06"]
            lec7_data = result[result["lecname"] == "lec07"]
            lec8_data = result[result["lecname"] == "lec08"]
            lec9_data = result[result["lecname"] == "lec09"]
            lec10_data = result[result["lecname"] == "lec10"]
            lec11_data = result[result["lecname"] == "lec11"]
            lec12_data = result[result["lecname"] == "lec12"]
            lec13_data = result[result["lecname"] == "lec13"]

            # lec毎のデータをdf_listに格納している
            df_list = [globals()[f'lec{i+1}_data'] for i in range(13)]

            # 汚いけどコード追加
            # df_list['kadai_a'] = df_list['kadai'].apply(
            #     lambda x: re.sub(r'_.*', '', x))
            all_tail = []
            for i in range(13):
                after_diff[i] = df_list[i][df_list[i]["time"] < class_time[i]]

                for _, df_sub in after_diff[i].groupby(['kadai_a', 'lecname']):
                    all_tail.append(df_sub.tail(1))

            # 全てをつなげる
            firstLoop = True
            for d in all_tail:
                if firstLoop:
                    f_data = d
                    firstLoop = False
                else:
                    f_data = pd.concat([f_data, d])

            print(f_data)
            ########################################################################################
            # ここの時点で文字数,locのdiffを持ったレビュー後のログ（行）がafter_diff[0-12]に入っている#
            ########################################################################################

    #         # time_df['time'] = final_df[12]['time']
    #         time_df = pd.DataFrame({'再編集時期': re_time1})
    #         # time_dfとfinal_df[12]に共通カラムがなかったため、インデックスを振りなおした
    #         after_diff[12] = after_diff[12].reset_index()

    #         after_diff[12] = after_diff[12].join(time_df)

    #         # print(after_diff[12])
    # # #############################ここから出力########################

            f_data = f_data[["SID", "time", "lecname", "kadai", "contents",
                                            "sumletter", "diff_sumletter", "loc", "diff_loc"]]

            # 一つ前との差分情報を追記するプログラムを追加

            if len(f_data) > 0:
                f_data.to_excel(writer, sheet_name=name[j+1])
            print(name[j+1])
        except IndexError:
            break
