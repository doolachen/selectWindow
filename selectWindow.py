import math
import numpy as np
import pandas as pd
import os

root = os.path.dirname(__file__)

def filter_func(df, mode):
    filtered = []
    for row in df:
        if mode in row[0]:
            filtered.append(row)
    return np.array(filtered)

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
        df = {
            '3': filter_func(pd.read_csv(os.path.join(root, 'psnr3.csv')).to_numpy(), mode),
            '4': filter_func(pd.read_csv(os.path.join(root, 'psnr4.csv')).to_numpy(), mode),
            '5': filter_func(pd.read_csv(os.path.join(root, 'psnr5.csv')).to_numpy(), mode),
            '6': filter_func(pd.read_csv(os.path.join(root, 'psnr6.csv')).to_numpy(), mode),
            '7': filter_func(pd.read_csv(os.path.join(root, 'psnr7.csv')).to_numpy(), mode)
        }

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
    best_quality_out = []
    max_window_out = []
    min_window_out = []
    for i in range(length):
        compare = []
        for item in out:
            compare.append((item, out[item][i]))
        res = sorted(compare, reverse=True, key=lambda x: x[1])
        best_quality_out.append((int(res[0][0]), res[0][1]))
        res = sorted(compare, reverse=True, key=lambda x: x[0])
        max_window_out.append((int(res[0][0]), res[0][1]))
        min_window_out.append((int(res[-1][0]), res[-1][1]))

    return best_quality_out, max_window_out, min_window_out, [(int(n_frame[0]), n_frame[1]) for n_frame in n_frames]


if __name__ == "__main__":
    t = [20, 20, 30, 40, 50]
    d = [20, 20, 30, 40, 50]
    b = 0.5
    L = 100

    a = select(t, d, b, L, mode='all')
    print(a)
