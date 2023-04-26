import sys
import os
root = os.path.dirname(sys.argv[0])
for i in range(3, 8):
    psnr = os.path.join(root, f'psnr{i}.csv')
    ssim = os.path.join(root, f'ssim{i}.csv')
    os.remove(psnr)
    os.rename(ssim, psnr)
