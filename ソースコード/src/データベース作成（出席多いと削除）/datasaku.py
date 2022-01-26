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


for j in range(len(name)):
    try:
        sheet = book[name[j+1]]
        data = sheet.values
        data = list(data)
        data_df = pd.DataFrame(data[1:], columns=data[0])
        conte = []
        after_diff = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# #########################一つ前との文字数や行数のdiffを取っていく
        # diff_subt = []

        # data_df['kadai_b'] = data_df['kadai'].apply(
        #     lambda x: re.sub(r'_.*', '', x))
        # # ここの時点で文字列差分を抽出しておく
        # for _, df_sub in data_df.groupby(['lecname', 'kadai_b']):
        #     print("ここまできた")
        #     print(df_sub)
        #     for i in range(100):
        #         print(i)
        #         if i == 0:
        #             diff_subt.append("")
        #         else:
        #             s1 = str(df_sub.iat[i, 5])
        #             s2 = str(df_sub.iat[i+1, 5])
        #             diff_subt.append(difflib.ndiff(s1.split(), s2.split()))

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
            ['kadai_a', 'lecname'])]).drop('kadai_a', axis=1)

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

        for i in range(13):
            after_diff[i] = df_list[i][df_list[i]["time"] >= class_time[i]]

        ########################################################################################
        # ここの時点で文字数,locのdiffを持ったレビュー後のログ（行）がafter_diff[0-12]に入っている#
        ########################################################################################

        # 変数に該当する行を追加していくと問題は解決する
        for i in range(12):
            after_diff[i+1] = after_diff[i].append(after_diff[i+1])

        # print(after_diff[12])

        # print(after_diff)
        ##############################################################################
        ################ここから再編集時刻に関するコード（効率化が必要）################
        ##############################################################################
        time1 = after_diff[12][after_diff[12]["lecname"] == "lec01"]
        time1 = time1['time'].tolist()
        re_time1 = []
        time2 = after_diff[12][after_diff[12]["lecname"] == "lec02"]
        time2 = time2['time'].tolist()
        re_time2 = []
        time3 = after_diff[12][after_diff[12]["lecname"] == "lec03"]
        time3 = time3['time'].tolist()
        re_time3 = []
        time4 = after_diff[12][after_diff[12]["lecname"] == "lec04"]
        time4 = time4['time'].tolist()
        re_time4 = []
        time5 = after_diff[12][after_diff[12]["lecname"] == "lec05"]
        time5 = time5['time'].tolist()
        re_time5 = []
        time6 = after_diff[12][after_diff[12]["lecname"] == "lec06"]
        time6 = time6['time'].tolist()
        re_time6 = []
        time7 = after_diff[12][after_diff[12]["lecname"] == "lec07"]
        time7 = time7['time'].tolist()
        re_time7 = []
        time8 = after_diff[12][after_diff[12]["lecname"] == "lec08"]
        time8 = time8['time'].tolist()
        re_time8 = []
        time9 = after_diff[12][after_diff[12]["lecname"] == "lec09"]
        time9 = time9['time'].tolist()
        re_time9 = []
        time10 = after_diff[12][after_diff[12]["lecname"] == "lec10"]
        time10 = time10['time'].tolist()
        re_time10 = []
        time11 = after_diff[12][after_diff[12]["lecname"] == "lec11"]
        time11 = time11['time'].tolist()
        re_time11 = []
        time12 = after_diff[12][after_diff[12]["lecname"] == "lec12"]
        time12 = time12['time'].tolist()
        re_time12 = []
        time13 = after_diff[12][after_diff[12]["lecname"] == "lec13"]
        time13 = time13['time'].tolist()
        re_time13 = []

        # list内の時間とレビュー時刻を比較していく
        for t in time1:
            if datetime(2020, 10, 1, 9, 10) <= t <= datetime(2020, 10, 1, 12, 40):
                re_time1.append("授業中")
            elif datetime(2020, 10, 1, 12, 40) < t <= datetime(2020, 10, 1, 23, 59):
                re_time1.append("授業日中")
            elif datetime(2020, 10, 2, 0, 0) <= t <= datetime(2020, 10, 2, 23, 59):
                re_time1.append("翌日")
            elif datetime(2020, 10, 3, 0, 0) <= t <= datetime(2020, 10, 8, 23, 59):
                re_time1.append("一週間以内")
            else:
                re_time1.append("一週間以上")

        for t in time2:
            if datetime(2020, 10, 8, 9, 10) <= t <= datetime(2020, 10, 8, 12, 40):
                re_time2.append("授業中")
            elif datetime(2020, 10, 8, 12, 40) < t <= datetime(2020, 10, 8, 23, 59):
                re_time2.append("授業日中")
            elif datetime(2020, 10, 9, 0, 0) <= t <= datetime(2020, 10, 9, 23, 59):
                re_time2.append("翌日")
            elif datetime(2020, 10, 10, 0, 0) <= t <= datetime(2020, 10, 15, 23, 59):
                re_time2.append("一週間以内")
            else:
                re_time2.append("一週間以上")

        for t in time3:
            if datetime(2020, 10, 15, 9, 10) <= t <= datetime(2020, 10, 15, 12, 40):
                re_time3.append("授業中")
            elif datetime(2020, 10, 15, 12, 40) < t <= datetime(2020, 10, 15, 23, 59):
                re_time3.append("授業日中")
            elif datetime(2020, 10, 16, 0, 0) <= t <= datetime(2020, 10, 16, 23, 59):
                re_time3.append("翌日")
            elif datetime(2020, 10, 17, 0, 0) <= t <= datetime(2020, 10, 22, 23, 59):
                re_time3.append("一週間以内")
            else:
                re_time3.append("一週間以上")

        for t in time4:
            if datetime(2020, 10, 22, 9, 10) <= t <= datetime(2020, 10, 22, 12, 40):
                re_time4.append("授業中")
            elif datetime(2020, 10, 22, 12, 40) < t <= datetime(2020, 10, 22, 23, 59):
                re_time4.append("授業日中")
            elif datetime(2020, 10, 23, 0, 0) <= t <= datetime(2020, 10, 23, 23, 59):
                re_time4.append("翌日")
            elif datetime(2020, 10, 24, 0, 0) <= t <= datetime(2020, 10, 29, 23, 59):
                re_time4.append("一週間以内")
            else:
                re_time4.append("一週間以上")

        for t in time5:
            if datetime(2020, 10, 29, 9, 10) <= t <= datetime(2020, 10, 29, 12, 40):
                re_time5.append("授業中")
            elif datetime(2020, 10, 29, 12, 40) < t <= datetime(2020, 10, 29, 23, 59):
                re_time5.append("授業日中")
            elif datetime(2020, 10, 30, 0, 0) <= t <= datetime(2020, 10, 30, 23, 59):
                re_time5.append("翌日")
            elif datetime(2020, 10, 31, 0, 0) <= t <= datetime(2020, 11, 5, 23, 59):
                re_time5.append("一週間以内")
            else:
                re_time5.append("一週間以上")

        for t in time6:
            if datetime(2020, 11, 12, 9, 10) <= t <= datetime(2020, 11, 12, 12, 40):
                re_time6.append("授業中")
            elif datetime(2020, 11, 12, 12, 40) < t <= datetime(2020, 11, 12, 23, 59):
                re_time6.append("授業日中")
            elif datetime(2020, 11, 13, 0, 0) <= t <= datetime(2020, 11, 13, 23, 59):
                re_time6.append("翌日")
            elif datetime(2020, 11, 14, 0, 0) <= t <= datetime(2020, 11, 19, 23, 59):
                re_time6.append("一週間以内")
            else:
                re_time6.append("一週間以上")

        for t in time7:
            if datetime(2020, 11, 19, 9, 10) <= t <= datetime(2020, 11, 19, 12, 40):
                re_time7.append("授業中")
            elif datetime(2020, 11, 19, 12, 40) < t <= datetime(2020, 11, 19, 23, 59):
                re_time7.append("授業日中")
            elif datetime(2020, 11, 20, 0, 0) <= t <= datetime(2020, 11, 20, 23, 59):
                re_time7.append("翌日")
            elif datetime(2020, 11, 21, 0, 0) <= t <= datetime(2020, 11, 26, 23, 59):
                re_time7.append("一週間以内")
            else:
                re_time7.append("一週間以上")

        for t in time8:
            if datetime(2020, 11, 26, 9, 10) <= t <= datetime(2020, 11, 26, 12, 40):
                re_time8.append("授業中")
            elif datetime(2020, 11, 26, 12, 40) < t <= datetime(2020, 11, 26, 23, 59):
                re_time8.append("授業日中")
            elif datetime(2020, 11, 27, 0, 0) <= t <= datetime(2020, 11, 27, 23, 59):
                re_time8.append("翌日")
            elif datetime(2020, 11, 28, 0, 0) <= t <= datetime(2020, 12, 3, 23, 59):
                re_time8.append("一週間以内")
            else:
                re_time8.append("一週間以上")

        for t in time9:
            if datetime(2020, 12, 3, 9, 10) <= t <= datetime(2020, 12, 3, 12, 40):
                re_time9.append("授業中")
            elif datetime(2020, 12, 3, 12, 40) < t <= datetime(2020, 12, 3, 23, 59):
                re_time9.append("授業日中")
            elif datetime(2020, 12, 4, 0, 0) <= t <= datetime(2020, 12, 4, 23, 59):
                re_time9.append("翌日")
            elif datetime(2020, 12, 5, 0, 0) <= t <= datetime(2020, 12, 10, 23, 59):
                re_time9.append("一週間以内")
            else:
                re_time9.append("一週間以上")

        for t in time10:
            if datetime(2020, 12, 10, 9, 10) <= t <= datetime(2020, 12, 10, 12, 40):
                re_time10.append("授業中")
            elif datetime(2020, 12, 10, 12, 40) < t <= datetime(2020, 12, 10, 23, 59):
                re_time10.append("授業日中")
            elif datetime(2020, 12, 11, 0, 0) <= t <= datetime(2020, 12, 11, 23, 59):
                re_time10.append("翌日")
            elif datetime(2020, 12, 12, 0, 0) <= t <= datetime(2020, 12, 17, 23, 59):
                re_time10.append("一週間以内")
            else:
                re_time10.append("一週間以上")

        for t in time11:
            if datetime(2020, 12, 24, 9, 10) <= t <= datetime(2020, 12, 24, 12, 40):
                re_time11.append("授業中")
            elif datetime(2020, 12, 24, 12, 40) < t <= datetime(2020, 12, 24, 23, 59):
                re_time11.append("授業日中")
            elif datetime(2020, 12, 25, 0, 0) <= t <= datetime(2020, 12, 25, 23, 59):
                re_time11.append("翌日")
            elif datetime(2020, 12, 26, 0, 0) <= t <= datetime(2020, 12, 31, 23, 59):
                re_time11.append("一週間以内")
            else:
                re_time11.append("一週間以上")

        for t in time12:
            if datetime(2021, 1, 7, 9, 10) <= t <= datetime(2021, 1, 7, 12, 40):
                re_time12.append("授業中")
            elif datetime(2021, 1, 7, 12, 40) < t <= datetime(2021, 1, 7, 23, 59):
                re_time12.append("授業日中")
            elif datetime(2021, 1, 8, 0, 0) <= t <= datetime(2021, 1, 8, 23, 59):
                re_time12.append("翌日")
            elif datetime(2021, 1, 9, 0, 0) <= t <= datetime(2021, 1, 14, 23, 59):
                re_time12.append("一週間以内")
            else:
                re_time12.append("一週間以上")

        for t in time13:
            if datetime(2021, 1, 14, 9, 10) <= t <= datetime(2021, 1, 14, 12, 40):
                re_time13.append("授業中")
            elif datetime(2021, 1, 14, 12, 40) < t <= datetime(2021, 1, 14, 23, 59):
                re_time13.append("授業日中")
            elif datetime(2021, 1, 15, 0, 0) <= t <= datetime(2021, 1, 15, 23, 59):
                re_time13.append("翌日")
            elif datetime(2021, 1, 16, 0, 0) <= t <= datetime(2021, 1, 21, 23, 59):
                re_time13.append("一週間以内")
            else:
                re_time13.append("一週間以上")

        # 最後にre_time1,2,3...を連結させてからデータフレームに変換しjoinする。
        re_time1.extend(re_time2)
        re_time1.extend(re_time3)
        re_time1.extend(re_time4)
        re_time1.extend(re_time5)
        re_time1.extend(re_time6)
        re_time1.extend(re_time7)
        re_time1.extend(re_time8)
        re_time1.extend(re_time9)
        re_time1.extend(re_time10)
        re_time1.extend(re_time11)
        re_time1.extend(re_time12)
        re_time1.extend(re_time13)

        # time_df['time'] = final_df[12]['time']
        time_df = pd.DataFrame({'再編集時期': re_time1})
        # time_dfとfinal_df[12]に共通カラムがなかったため、インデックスを振りなおした
        after_diff[12] = after_diff[12].reset_index()

        after_diff[12] = after_diff[12].join(time_df)

        # print(after_diff[12])
# #############################ここから出力########################

        after_diff[12] = after_diff[12][["SID", "time", "lecname", "kadai", "contents",
                                         "sumletter", "diff_sumletter", "loc", "diff_loc", "再編集時期"]]

        # 一つ前との差分情報を追記するプログラムを追加

        if len(after_diff[12]) > 0:
            with pd.ExcelWriter('IN_after_review.xlsx', engine="openpyxl", mode="a") as writer:
                after_diff[12].to_excel(writer, sheet_name=name[j+1])

    except IndexError:
        break
print("除外された人数 ", cnt)
