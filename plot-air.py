#!/usr/bin/env python3
# vim: sta:et:sw=4:ts=4:sts=4

import sys
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

if len(sys.argv) > 1:
    filename = str(sys.argv[1])
else:
    filename = 'measurements.csv'

# headers = ['Name', 'Age', 'Marks']
#  Hum_0', ' Temp0', '  Hum_LT', ' Temp_LT',
#       '  Hum_RB', ' Temp_RB', ' H20_Meas', ' H2O_Pump '],
df = pd.read_csv(filename, delimiter=',') # , low_memory=False) # 'marks.csv', names=headers)
#x, y = df.Hum_0.min(), df.Hum_0.max()
# 50.31 51.8
# pm2_5 >>> df.pm2_5.max()
df.plot(x='timestamp', y=['pm2_5','pm10'])
#146.4 0.7
#df['H0S'] = (df.Hum_0 - x) / (y - x)
#df['1/H0S'] = 5.0 / (df.Hum_0 - 45.0)

#df.plot(x='timestamp', y=['1/H0S', '1/T0S', 'HLT','1/TLT', '1/HRB','1/TRB'])
#df.plot(x='timestamp', y=['1/H0S', '1/T0S', 'HLT','1/TLT', '1/HRB','1/TRB', 'HRT','1/TRT'])
#df.plot(x='timestamp', y=['1/H0S', '1/T0S', 'HLT','1/TLT', '1/TRB', 'HRT','1/TRT'])
plt.show()

