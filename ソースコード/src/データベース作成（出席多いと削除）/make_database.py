# -*- coding: utf-8 -*-
import glob
import pathlib
import pandas as pd
import re as re
from datetime import datetime as dt
import datetime as dtdt
import openpyxl
import difflib
import copy
import os
import shutil
import magic
# True
# spyderはutf-8,visual codeはShift-Jis
​
# ファイルの中身読み取り
​
​


def make_lines(path):
    try:
        # ここに本物のバイナリか同課のプログラムを追加
        filetype = magic.from_file(path, mime=True)
        if filetype == 'application/octet-stream' and os.path.getsize(path) > 30:
            return 'error', 'error', 'error'
        # クラスファイルを除く
        if path[-6:] == '.class':
            return 'error', 'error', 'error'
        f = open(path, encoding='utf-8', errors='ignore')
        all_lines = f.readlines()
        lines = ''
        all_letter = 0
        all_loc = 0
        # ファイルの中身，文字数，loc数取得
        lines = ','.join(map(str, all_lines))
        all_loc = len(all_lines)
        for line in all_lines:
            all_letter += len(line)
        f.close()
        return lines, all_letter, all_loc


​
   except magic.magic.MagicException:
        # クラスファイルを除く
        if path[-6:] == '.class':
            return 'error', 'error', 'error'
        f = open(path, encoding='utf-8', errors='ignore')
        all_lines = f.readlines()
        lines = ''
        all_letter = 0
        all_loc = 0
        # ファイルの中身，文字数，loc数取得
        lines = ','.join(map(str, all_lines))
        all_loc = len(all_lines)
        for line in all_lines:
            all_letter += len(line)
        f.close()
        return lines, all_letter, all_loc
        # データのファイル名と時間取得
​
​


def get_date(kadai_path):
    # ファイル名取得
    kadainame = os.path.basename(kadai_path)


​
   # ファイル名の末尾に_が入っている場合
   if kadainame[-1] == '_':
        kadainame = kadainame[:-1]
    fileedit = kadainame.rsplit('_')
    if len(fileedit) > 2:
        print(kadai_path + ' 異常あり')
    elif len(fileedit) == 1:
        print(kadai_path + ' 異常あり')
        return kadainame, 'error'
    # 保存時間取得
    filedate = fileedit[-1][0:4]+'/'+fileedit[-1][4:6]+'/'+fileedit[-1][6:8] + \
        ' '+fileedit[-1][8:10]+':'+fileedit[-1][10:12]+':'+fileedit[-1][12:14]
    filedate = dt.strptime(
        filedate, '%Y/%m/%d %H:%M:%S')  # timeに変換
    return kadainame, filedate
​
# main
​
​


def main():
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 1000)
    ##############################追加######################################
    wb = openpyxl.Workbook()
    wb.save('jyugyou.xlsx')  # excelファイル作成完了
    # 対象となる学科を入力させる
    print('学科を入力してください(b:IS科 c:IN科 q:IC科)')
    gakka = input()
    for user_name in (glob.glob('e1' + gakka + '*')):  # ユーザ名の取得
        # ここでファイルの時間，ファイルの差分，ブロックの情報を格納するdfを初期化
        data_df = pd.DataFrame(
            columns=['SID', 'time', 'lecname', 'kadai', 'contents', 'sumletter', 'loc'])
        # 格納データ初期化
        cnt = 0
        for fnumber in (glob.glob(user_name + '/.log/.history/java20/*')):
            if os.path.isdir(fnumber):  # フォルダーか分析
                # 課題までのPATHを取得
                for kadai_path in (glob.glob(user_name + '/.log/.history/java20/' + os.path.split(fnumber)[1] + '/*')):
                    if os.path.isfile(kadai_path):
                        kadainame, filedate = get_date(kadai_path)
                        if filedate == 'error':
                            # ファイル名に日付がない場合，ここに入る
                            continue
                        # ファイルの中身取得
                        data_nakami, sumletter_num, loc_num = make_lines(
                            kadai_path)
                        if [data_nakami, sumletter_num, loc_num] == ['error', 'error', 'error']:
                            # バイナリになっているとここに入る
                            print(kadai_path + ' バイナリになっている')
                            continue
                        data_df.loc[cnt] = [user_name, filedate, os.path.split(
                            fnumber)[1], kadainame, data_nakami, sumletter_num, loc_num]
                        cnt = cnt + 1
                    else:
                        print(user_name + ' ' + kadai_path + ' フォルダーになっている')
            else:
                kadainame, filedate = get_date(fnumber)
                if filedate == 'error':
                    # ファイル名に日付がない場合，ここに入る
                    continue
                # ファイルの中身取得
                data_nakami, sumletter_num, loc_num = make_lines(kadai_path)
                if [data_nakami, sumletter_num, loc_num] == ['error', 'error', 'error']:
                    # バイナリになっているとここに入る
                    print(kadai_path + ' バイナリになっている')
                    continue
                data_df.loc[cnt] = [user_name, filedate, 'another',
                                    kadainame, data_nakami, sumletter_num, loc_num]
        data_df = data_df.sort_values('time')
        data_df = data_df.reset_index(drop=True)
        with pd.ExcelWriter('jyugyou.xlsx', engine='openpyxl', mode='a') as writer:  # pylint: disable=abstract-class-instantiated
            data_df.to_excel(writer, sheet_name=user_name)
        del data_df

​
   print(user_name + '　終了')
​
​
   # dataall_df.to_excel('./kakikae.xlsx', sheet_name='new_sheet_name')
# 一番最初にはいる場所
if __name__ == '__main__':
    main()
    #############################追加##############################
