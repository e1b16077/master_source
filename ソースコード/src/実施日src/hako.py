import pandas as pd
import openpyxl
from datetime import datetime, time
import re
import math
import matplotlib.pyplot as plt

# test1
IS = [2, 7, 1, 4, 3, 7, 2, 1, 2, 3, 4, 2, 2, 3, 2, 2, 3, 4, 2, 4, 1, 3, 1, 7, 1, 5, 2, 5, 5, 2, 4, 1, 2, 1, 3, 3, 4, 1, 2, 4, 1, 2, 2, 2, 1, 3, 3, 1, 4, 1,
      5, 2, 2, 2, 4, 2, 5, 6, 3, 3, 6, 1, 4, 1, 6, 1, 2, 2, 3, 1, 1, 2, 2, 1, 3, 2, 2, 2, 3, 3, 3, 4, 4, 1, 5, 1]
IC = [1, 4, 3, 1, 2, 2, 6, 4, 2, 5, 1, 4, 3, 4, 7, 4, 2, 1, 3, 2, 1, 1, 6, 1, 1, 2, 2, 2, 4, 3, 3, 2, 2, 2, 6, 2, 3, 3, 2, 3, 2, 1, 1, 3, 4, 2, 1, 3, 7, 4,
      2, 3, 2, 4, 4, 5, 9, 3, 1, 7, 4, 2, 1, 1, 4, 4, 3, 5, 6, 1, 5, 4, 1, 2, 5, 7, 2, 2]
IN = [1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 2, 1, 2, 3, 2, 2, 1, 2, 1, 3, 1, 1, 1, 3, 2, 1, 3, 1, 1, 2, 1, 2, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 1, 2, 1,
      1, 1, 4, 1, 1, 1, 2, 2, 2, 1]

data1 = (IS, IC, IN)


plt.rcParams['font.size'] = 15
fig1, ax1 = plt.subplots()
# ax1.set_title('学科ごとのログ数')
ax1.set_xticklabels(['クラスA(N=86)', 'クラスB(N=78)',
                     'クラスC(N=60)'], fontname="MS Gothic")

plt.subplots_adjust(bottom=0.2, top=0.95)

ax1.boxplot(data1, sym="")
# ax1.boxplot(data2, sym="")
# ax1.boxplot(data3, sym="")

plt.savefig("300_dpi_scatter.png", format="png", dpi=300)
plt.show()
