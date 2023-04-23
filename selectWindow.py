import math
import numpy as np
import pandas as pd
import os

root = os.path.dirname(__file__)


def select(time: list, data: list, bandwidth: float, limit: float, mode: str):
    """
    Select best psnr and window size.
    Args:
        :param time: A timetable list.
        :param data: A datatable list.
        :param bandwidth: The throughput.
        :param limit: Time limitation.
        :param mode:
    :returns
        list[tuple(str: windows_size,float: best_psnr)]
    """
    if mode == "all":
        df = {
            '3': pd.read_csv(os.path.join(root, 'psnr3.csv')).to_numpy(),
            '4': pd.read_csv(os.path.join(root, 'psnr4.csv')).to_numpy(),
            '5': pd.read_csv(os.path.join(root, 'psnr5.csv')).to_numpy(),
            '6': pd.read_csv(os.path.join(root, 'psnr6.csv')).to_numpy(),
            '7': pd.read_csv(os.path.join(root, 'psnr7.csv')).to_numpy()
        }
    else:
        # TODO
        df = {'3': pd.read_csv('./psnr3.csv').to_numpy(), '4': pd.read_csv('./psnr4.csv').to_numpy(),
              '5': pd.read_csv('./psnr5.csv').to_numpy(), '6': pd.read_csv('./psnr6.csv').to_numpy(),
              '7': pd.read_csv('./psnr7.csv').to_numpy()}

    total = np.sum([time, [_ / bandwidth for _ in data]], axis=0)
    windows = []
    for i, time in enumerate(total):
        if time <= limit:
            windows.append(i + 3)
    n_frames = []
    for i in windows:
        n_frames.append((str(i), math.floor(total[i - 3] / 30)))
    out = {}
    length = None
    for temp in n_frames:
        avg = []
        for line in df[temp[0]]:
            avg.append(np.mean(line[2:2 + temp[1]]))
        out[temp[0]] = avg
        length = len(avg)
    final_out = []
    for i in range(length):
        compare = []
        for item in out:
            compare.append((item, out[item][i]))
        res = sorted(compare, reverse=True, key=lambda x: x[1])
        final_out.append(res[0])

    return final_out


if __name__ == "__main__":
    t = [20, 20, 30, 40, 50]
    d = [20, 20, 30, 40, 50]
    b = 0.5
    L = 100

    a = select(t, d, b, L, mode='all')
    print(a)
