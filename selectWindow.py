import math
import numpy as np
import pandas as pd
import copy

"""A general prefetch generator.
Ref:
https://stackoverflow.com/questions/7323664/python-generator-pre-fetch
Args:
    generator: Python generator.
    num_prefetch_queue (int): Number of prefetch queue.
"""


def select(time: list, data: list, bandwidth: float, limit: float, mode: str):
    """
    Select best psnr and window size.
    Args:
        :param time: A timetable list.
        :param data: A datatable list.
        :param bandwidth: The throughput.
        :param limit: Time limitation.
    :returns
        list[tuple(str: windows_size,float: best_psnr)]
    """
    df = {'3': pd.read_csv('./psnr3.csv').to_numpy(), '4': pd.read_csv('./psnr4.csv').to_numpy(),
          '5': pd.read_csv('./psnr5.csv').to_numpy(), '6': pd.read_csv('./psnr6.csv').to_numpy(),
          '7': pd.read_csv('./psnr7.csv').to_numpy()}

    total = np.sum([time, [_ / bandwidth for _ in data]], axis=0)
    windows = []
    for i, time in enumerate(total):
        if time <= limit:
            windows.append(i+3)
    n_frames = []
    for i in windows:
        n_frames.append((str(i), math.floor(total[i-3]/30)))
    out = {}
    lenth = None
    for temp in n_frames:
        avg = []
        for line in df[temp[0]]:
            avg.append(np.mean(line[2:2+temp[1]]))
        out[temp[0]] = avg
        lenth = len(avg)
    final_out = []
    for i in range(lenth):
        compare = []
        for item in out:
            compare.append((item,out[item][i]))
        res = sorted(compare,reverse=True,key = lambda x: x[1])
        final_out.append(res[0])

    return final_out

# 数据预处理
# df = {'3': pd.read_csv('./psnr3.csv').to_numpy(), '4': [], '5': [], '6': [],
#       '7': pd.read_csv('./psnr7.csv').to_numpy(),'3_':[],'7_':[]}
# num = 0
# for line_3 in df['3']:
#     num += 1
#     print(num)
#     for line_7 in df['7']:
#         if line_3[0] == line_7[0] and line_3[1] == line_7[1]:
#             new3 = []
#             new4 = []
#             new5 = []
#             new6 = []
#             new7 = []
#             new3[:2] = copy.deepcopy(line_3[:2])
#             new4[:2] = copy.deepcopy(line_3[:2])
#             new5[:2] = copy.deepcopy(line_3[:2])
#             new6[:2] = copy.deepcopy(line_3[:2])
#             new7[:2] = copy.deepcopy(line_3[:2])
#
#             for i, _ in enumerate(line_3[2:]):
#                 new3.append(line_3[2:][i])
#                 new4.append((line_7[2:][i] + 3 * line_3[2:][i]) / 4)
#                 new5.append((line_7[2:][i] + line_3[2:][i]) / 2)
#                 new6.append((3 * line_7[2:][i] + line_3[2:][i]) / 4)
#                 new7.append(line_7[2:][i])
#             df['3_'].append(new3)
#             df['4'].append(new4)
#             df['5'].append(new5)
#             df['6'].append(new6)
#             df['7_'].append(new7)
#             break
#
# df['3_'] = pd.DataFrame(np.array(df['3_']))
# df['4'] = pd.DataFrame(np.array(df['4']))
# df['5'] = pd.DataFrame(np.array(df['5']))
# df['6'] = pd.DataFrame(np.array(df['6']))
# df['7_'] = pd.DataFrame(np.array(df['7_']))
#
# df['3_'].to_csv('psnr3_new.csv', index=False)
# df['4'].to_csv('psnr4.csv', index=False)
# df['5'].to_csv('psnr5.csv', index=False)
# df['6'].to_csv('psnr6.csv', index=False)
# df['7_'].to_csv('psnr7_new.csv', index=False)

t = [20, 20, 30, 40, 50]
d = [20, 20, 30, 40, 50]
b = 0.5
L = 100

select(t, d, b, L,mode='all')
