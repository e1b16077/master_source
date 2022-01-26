import pandas as pd
import openpyxl
from datetime import datetime, time
import re
import math
import matplotlib.pyplot as plt

# test1
kubetunasi_test1 = [0.0, 9.5, 7.5, 0.0, 0.0, 0.0, 9.0, 4.5, 5.0, 0.0, 0.0, 0.0, 9.5, 10.0, 9.5, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.5, 
8.5, 9.5, 10.0, 10.0, 10.0, 10.0, 9.5, 10.0, 9.5, 9.5, 10.0, 9.5, 10.0, 9.0, 10.0, 9.5, 9.5, 10.0, 9.5, 8.5, 9.0, 10.0, 2.5, 9.5, 9.5, 10.0, 9.0, 10.0, 10.0, 9.5, 9.5, 10.0, 9.5, 10.0, 8.0, 9.5, 8.0, 10.0, 10.0, 9.0, 10.0, 9.5, 10.0, 2.0, 7.0, 10.0, 9.5, 10.0, 10.0, 10.0, 9.5, 10.0, 9.0, 7.0, 9.0, 0.0, 9.5, 8.0, 9.0, 9.0, 10.0, 10.0, 10.0, 9.5, 10.0, 10.0, 9.0, 10.0, 9.0, 9.5, 10.0, 8.7, 6.7, 9.3, 10.0, 10.0, 9.3, 10.0, 9.3, 10.0, 10.0, 9.3, 8.0, 10.0, 10.0, 10.0, 7.3, 8.7, 9.3, 9.3, 9.3, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.3, 9.3, 10.0, 10.0, 10.0, 10.0, 10.0, 9.3, 10.0, 10.0, 10.0, 9.3, 9.3, 9.3, 9.3, 10.0, 7.3, 7.3, 10.0, 8.7, 9.3, 10.0, 8.7, 10.0, 4.7, 9.3, 9.3, 8.7, 10.0, 4.7, 10.0, 8.7, 9.3, 10.0, 9.3, 10.0, 10.0, 7.3, 10.0, 9.3, 10.0, 10.0, 8.7, 10.0, 9.3, 10.0, 4.7, 10.0, 10.0, 10.0, 10.0, 8.7, 10.0, 10.0, 10.0, 10.0, 10.0, 9.3, 8.7, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.3, 9.3, 10.0, 9.3, 10.0, 0.0, 9.3, 9.3, 7.3, 9.3, 9.3, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.3, 9.3, 8.7, 9.3, 9.3, 10.0, 9.3, 10.0, 10.0, 10.0, 8.0, 9.3, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 8.7, 8.0, 9.3, 9.3, 8.7, 8.0, 9.3, 10.0, 7.3, 10.0, 10.0, 9.3, 0.0, 9.3, 10.0, 9.3, 9.3, 10.0, 8.7, 8.7, 10.0, 10.0, 8.7, 10.0, 7.3, 0.0, 10.0, 8.0, 6.7, 10.0, 4.7, 7.3, 10.0, 8.7, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 9.3, 9.3, 10.0, 6.7, 9.3, 10.0, 6.7, 10.0, 9.3, 10.0, 9.3, 9.3, 7.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.5, 9.5, 9.5, 7.0]
ikkai_test1 = [8.7, 6.7, 10.0, 10.0, 9.3, 9.3, 10.0, 10.0, 9.3, 10.0, 10.0, 7.3, 9.3, 9.3, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.3, 9.3, 9.3, 10.0, 7.3, 9.3, 10.0, 9.3, 9.3, 10.0, 4.7, 10.0, 9.3, 10.0, 10.0, 10.0, 7.3, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 8.7, 10.0, 10.0, 10.0, 9.3, 8.7, 10.0, 10.0, 10.0, 10.0, 10.0, 9.3, 10.0, 9.3, 10.0, 9.3, 9.3, 9.3, 9.3, 10.0, 10.0, 10.0, 10.0, 9.3, 8.7, 9.3, 9.3, 10.0, 10.0, 8.0, 9.3, 10.0, 8.7, 8.0, 9.3, 8.7, 9.3, 10.0, 10.0, 10.0, 9.3, 0.0, 10.0, 9.3, 8.7, 8.7, 10.0, 8.7, 10.0, 7.3, 0.0, 10.0, 8.0, 6.7, 4.7, 7.3, 10.0, 8.7, 10.0, 10.0, 9.3, 9.3, 9.3, 10.0, 9.3]
tyokkin_test1 = [6.7, 10.0, 9.3, 10.0, 10.0, 9.3, 10.0, 9.3, 10.0, 10.0, 10.0, 10.0, 9.3, 9.3, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 8.7, 10.0, 10.0, 9.3, 8.7, 10.0, 10.0, 
10.0, 9.3, 10.0, 9.3, 9.3, 9.3, 10.0, 10.0, 10.0, 8.7, 9.3, 9.3, 10.0, 9.3, 8.7, 10.0, 9.3, 0.0, 10.0, 9.3, 8.7, 8.7, 7.3, 10.0, 8.0, 6.7, 7.3, 10.0, 9.3, 9.3]

data1 = (kubetunasi_test1, ikkai_test1, tyokkin_test1)

# test2
kubetunasi_test2 = [9.0, 9.5, 5.5, 0.0, 0.0, 5.5, 9.5, 2.5, 7.0, 0.0, 0.0, 0.0, 8.0, 10.0, 8.0, 8.5, 9.5, 7.5, 8.5, 10.0, 9.0, 10.0, 7.5, 10.0, 9.5, 10.0, 9.5, 8.5, 8.0, 9.0, 10.0, 10.0, 8.5, 10.0, 10.0, 9.0, 9.5, 8.5, 9.5, 9.5, 9.0, 5.0, 10.0, 9.0, 9.0, 9.5, 7.0, 9.5, 6.0, 10.0, 9.0, 9.5, 9.5, 8.5, 7.5, 10.0, 9.0, 8.0, 9.0, 
9.0, 8.5, 0.0, 6.0, 9.5, 7.5, 9.5, 10.0, 6.0, 9.5, 8.5, 9.5, 0.0, 9.0, 9.5, 7.5, 7.5, 9.0, 9.5, 10.0, 9.0, 10.0, 9.5, 9.5, 0.0, 9.0, 9.0, 10.0, 9.5, 10.0, 10.0, 0.0, 10.0, 9.5, 10.0, 8.0, 9.0, 9.0, 9.0, 8.5, 0.0, 10.0, 8.6, 9.5, 9.5, 7.6, 10.0, 10.0, 10.0, 8.6, 7.6, 6.7, 6.7, 9.0, 10.0, 8.1, 10.0, 9.0, 9.5, 10.0, 9.0, 10.0, 10.0, 10.0, 8.6, 9.5, 9.5, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 8.1, 8.6, 9.5, 7.6, 8.6, 9.5, 9.0, 5.7, 10.0, 9.0, 10.0, 10.0, 9.5, 10.0, 2.9, 9.5, 9.5, 7.1, 10.0, 0.0, 6.2, 9.5, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.5, 10.0, 10.0, 10.0, 9.5, 10.0, 9.5, 9.5, 9.0, 10.0, 9.5, 8.6, 6.2, 9.5, 9.0, 10.0, 10.0, 7.1, 9.0, 9.5, 8.6, 9.5, 10.0, 9.5, 7.6, 9.5, 8.6, 10.0, 10.0, 9.5, 10.0, 0.0, 10.0, 10.0, 8.1, 10.0, 9.5, 9.0, 9.0, 9.5, 9.5, 9.0, 9.5, 9.5, 9.0, 8.6, 6.7, 10.0, 10.0, 8.6, 9.5, 8.6, 10.0, 8.6, 9.0, 9.5, 9.0, 10.0, 9.5, 9.5, 5.2, 7.6, 9.0, 10.0, 9.5, 9.5, 9.5, 
9.5, 10.0, 6.2, 9.5, 10.0, 10.0, 0.0, 7.6, 6.2, 5.7, 9.0, 9.0, 10.0, 10.0, 9.0, 9.5, 9.5, 8.6, 6.7, 9.0, 9.5, 6.7, 8.6, 10.0, 10.0, 10.0, 6.7, 2.9, 1.0, 9.0, 3.3, 9.5, 8.6, 9.5, 9.5, 9.0, 9.5, 8.6, 9.0, 8.6, 10.0, 9.5, 9.5, 9.0, 9.5, 10.0, 10.0, 9.5, 7.5, 7.0, 10.0, 9.5, 7.0, 9.0, 9.0, 9.0, 4.5, 9.0] 
ikkai_test2 = [0.0, 10.0, 9.5, 9.5, 7.6, 10.0, 10.0, 8.6, 7.6, 9.0, 10.0, 8.1, 9.0, 10.0, 9.0, 10.0, 10.0, 8.6, 9.5, 9.5, 10.0, 10.0, 10.0, 10.0, 9.5, 7.6, 8.6, 9.5, 9.0, 10.0, 10.0, 9.5, 9.5, 10.0, 0.0, 6.2, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.5, 9.0, 10.0, 8.6, 6.2, 9.5, 10.0, 7.1, 9.0, 9.5, 8.6, 9.5, 10.0, 9.5, 9.5, 10.0, 10.0, 9.5, 10.0, 10.0, 10.0, 10.0, 9.5, 9.0, 9.0, 9.5, 9.0, 9.5, 8.6, 6.7, 10.0, 10.0, 9.5, 8.6, 9.0, 9.5, 7.6, 9.0, 10.0, 9.5, 9.5, 10.0, 9.5, 10.0, 10.0, 0.0, 6.2, 9.0, 10.0, 10.0, 9.5, 9.5, 8.6, 6.7, 9.0, 9.5, 6.7, 8.6, 10.0, 10.0, 6.7, 2.9, 8.6, 9.5, 9.0, 9.5, 8.6, 10.0, 10.0]
tyokkin_test2 = [0.0, 9.5, 9.5, 10.0, 9.0, 10.0, 8.1, 9.0, 10.0, 9.0, 10.0, 9.5, 10.0, 7.6, 8.6, 9.5, 10.0, 10.0, 6.2, 10.0, 10.0, 9.5, 9.0, 10.0, 8.6, 10.0, 7.1, 9.5, 8.6, 9.5, 9.5, 10.0, 10.0, 10.0, 10.0, 10.0, 9.5, 9.0, 9.5, 9.0, 9.5, 6.7, 9.5, 8.6, 9.0, 9.5, 7.6, 10.0, 9.5, 9.5, 10.0, 9.5, 10.0, 0.0, 6.2, 9.0, 10.0, 9.5, 9.5, 8.6, 10.0, 2.9, 8.6, 9.5, 9.5, 8.6, 10.0]

data2 = (kubetunasi_test2, ikkai_test2, tyokkin_test2)

# test3
kubetunasi_test3 = [0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 10.0, 5.5, 9.0, 8.5, 9.0, 10.0, 10.0, 7.0, 0.0, 0.0, 9.5, 10.0, 9.0, 10.0, 8.0, 8.0, 9.0, 9.0, 9.5, 9.0, 8.0, 9.5, 9.0, 9.0, 3.0, 7.0, 4.5, 0.0, 0.0, 9.5, 5.0, 0.0, 5.0, 6.0, 8.5, 7.0, 9.5, 8.5, 8.0, 8.5, 8.0, 6.5, 9.5, 0.0, 9.0, 8.0, 7.0, 7.5, 0.0, 0.0, 8.5, 5.5, 2.5, 9.5, 6.0, 9.5, 0.0, 4.0, 0.0, 5.5, 9.5, 9.5, 10.0, 9.5, 10.0, 5.0, 2.5, 1.0, 10.0, 9.0, 0.0, 6.0, 4.0, 8.0, 6.5, 10.0, 7.0, 0.0, 6.0, 8.5, 10.0, 4.5, 4.5, 6.0, 4.0, 7.5, 0.0, 8.3, 0.6, 0.6, 0.0, 2.8, 9.4, 0.0, 10.0, 8.9, 6.7, 10.0, 0.0, 10.0, 10.0, 0.0, 7.8, 7.8, 10.0, 10.0, 10.0, 10.0, 10.0, 9.4, 9.4, 8.9, 9.4, 9.4, 10.0, 8.9, 10.0, 0.0, 0.0, 10.0, 10.0, 3.9, 9.4, 9.4, 10.0, 9.4, 1.7, 3.3, 8.9, 4.4, 1.1, 7.8, 10.0, 0.0, 9.4, 0.0, 10.0, 0.0, 9.4, 8.9, 0.0, 10.0, 0.0, 1.1, 0.0, 2.2, 8.3, 10.0, 10.0, 10.0, 9.4, 10.0, 9.4, 10.0, 10.0, 7.8, 6.7, 6.7, 9.4, 1.1, 7.8, 9.4, 9.4, 10.0, 6.7, 8.9, 9.4, 8.9, 9.4, 9.4, 10.0, 8.9, 10.0, 10.0, 3.3, 10.0, 0.6, 10.0, 5.6, 7.8, 8.9, 0.0, 8.3, 0.0, 8.9, 8.3, 0.0, 9.4, 10.0, 8.9, 8.9, 8.9, 8.9, 9.4, 0.0, 9.4, 8.3, 0.0, 0.0, 9.4, 10.0, 10.0, 9.4, 8.3, 9.4, 8.3, 9.4, 1.1, 10.0, 4.4, 10.0, 9.4, 10.0, 1.1, 8.3, 10.0, 10.0, 10.0, 9.4, 8.3, 9.4, 10.0, 7.2, 8.9, 10.0, 9.4, 3.9, 10.0, 8.9, 7.2, 0.0, 0.0, 10.0, 7.8, 10.0, 7.2, 8.9, 0.0, 0.0, 10.0, 3.9, 0.6, 9.4, 9.4, 10.0, 9.4, 8.3, 7.2, 10.0, 7.2, 0.0, 0.0, 10.0, 8.9, 8.3, 9.4, 9.4, 8.9, 7.2, 10.0, 0.0, 10.0, 8.9, 10.0, 9.4, 8.3, 6.5, 5.5, 9.0, 8.5, 8.0, 8.0, 10.0, 6.5, 5.5, 7.5, 6.0]
ikkai_test3 = [0.0, 8.3, 0.6, 0.0, 2.8, 0.0, 10.0, 8.9, 6.7, 10.0, 10.0, 0.0, 7.8, 10.0, 10.0, 10.0, 9.4, 9.4, 8.9, 9.4, 0.0, 0.0, 10.0, 3.9, 9.4, 1.7, 3.3, 8.9, 4.4, 0.0, 9.4, 9.4, 8.9, 10.0, 0.0, 1.1, 2.2, 8.3, 10.0, 10.0, 9.4, 10.0, 10.0, 10.0, 9.4, 7.8, 9.4, 10.0, 6.7, 8.9, 9.4, 9.4, 10.0, 8.9, 10.0, 10.0, 3.3, 10.0, 10.0, 7.8, 8.9, 0.0, 8.3, 8.9, 8.3, 9.4, 10.0, 8.9, 8.9, 8.9, 9.4, 9.4, 0.0, 0.0, 9.4, 10.0, 9.4, 8.3, 9.4, 9.4, 1.1, 8.3, 10.0, 10.0, 8.3, 9.4, 7.2, 8.9, 10.0, 9.4, 10.0, 7.2, 0.0, 10.0, 10.0, 7.2, 8.9, 0.0, 0.0, 10.0, 3.9, 0.6, 9.4, 10.0, 9.4, 8.3, 0.0, 8.9, 8.3, 9.4, 7.2, 10.0, 8.3]
tyokkin_test3 = [8.3, 10.0, 8.9, 6.7, 10.0, 10.0, 9.4, 0.0, 9.4, 4.4, 9.4, 10.0, 0.0, 2.2, 10.0, 10.0, 9.4, 10.0, 7.8, 9.4, 10.0, 8.9, 10.0, 10.0, 7.8, 8.9, 8.9, 9.4, 10.0, 8.9, 8.9, 10.0, 8.3, 10.0, 8.9, 10.0, 9.4, 10.0, 8.9, 0.0, 0.0, 9.4, 8.3, 8.9, 10.0]

data3 = (kubetunasi_test1 + kubetunasi_test2 + kubetunasi_test3, ikkai_test1 + ikkai_test2 + ikkai_test3, tyokkin_test1 + tyokkin_test2 + tyokkin_test3)




plt.rcParams['font.size'] = 15
fig1, ax1 = plt.subplots()
# ax1.set_title('学科ごとのログ数')
ax1.set_xticklabels(['①', '②',
                     '③'], fontname="MS Gothic")

# plt.title("授業に10回以上参加し1つの課題に対して2回以上編集している学生のレビュー後課題編集数の分布",
#           y=-0.23, fontname="MS Gothic")
# plt.title("クラス毎のレビュー後課題実施数",
#           y=-0.23, fontname="MS Gothic")
plt.subplots_adjust(bottom=0.2, top=0.95)

# ax1.boxplot(data1, sym="")
# ax1.boxplot(data2, sym="")
ax1.boxplot(data3, sym="")

plt.savefig("300_dpi_scatter.png", format="png", dpi=300)
plt.show()
