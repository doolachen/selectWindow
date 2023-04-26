import pandas as pd
import numpy as np
import copy
# 数据预处理
df = {'3': pd.read_csv('./ssim3_ori.csv').to_numpy(), '4': [], '5': [], '6': [],
      '7': pd.read_csv('./ssim7_ori.csv').to_numpy(),'3_':[],'7_':[]}
num = 0
for line_3 in df['3']:
    num += 1
    print(num)
    for line_7 in df['7']:
        if line_3[0] == line_7[0] and line_3[1] == line_7[1]:
            new3 = []
            new4 = []
            new5 = []
            new6 = []
            new7 = []
            new3[:2] = copy.deepcopy(line_3[:2])
            new4[:2] = copy.deepcopy(line_3[:2])
            new5[:2] = copy.deepcopy(line_3[:2])
            new6[:2] = copy.deepcopy(line_3[:2])
            new7[:2] = copy.deepcopy(line_3[:2])

            for i, _ in enumerate(line_3[2:]):
                new3.append(line_3[2:][i])
                new4.append((line_7[2:][i] + 3 * line_3[2:][i]) / 4)
                new5.append((line_7[2:][i] + line_3[2:][i]) / 2)
                new6.append((3 * line_7[2:][i] + line_3[2:][i]) / 4)
                new7.append(line_7[2:][i])
            df['3_'].append(new3)
            df['4'].append(new4)
            df['5'].append(new5)
            df['6'].append(new6)
            df['7_'].append(new7)
            break

df['3_'] = pd.DataFrame(np.array(df['3_']))
df['4'] = pd.DataFrame(np.array(df['4']))
df['5'] = pd.DataFrame(np.array(df['5']))
df['6'] = pd.DataFrame(np.array(df['6']))
df['7_'] = pd.DataFrame(np.array(df['7_']))

df['3_'].to_csv('ssim3.csv', index=False)
df['4'].to_csv('ssim4.csv', index=False)
df['5'].to_csv('ssim5.csv', index=False)
df['6'].to_csv('ssim6.csv', index=False)
df['7_'].to_csv('ssim7.csv', index=False)
