import scipy.io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.signal import spectrogram
import sys
import os

# Parula colormap (MATLAB default) — sampled control points
_parula_data = [
    [0.2422, 0.1504, 0.6603], [0.2810, 0.1856, 0.7280], [0.2782, 0.2227, 0.7818],
    [0.2534, 0.2651, 0.8308], [0.2147, 0.3187, 0.8639], [0.1802, 0.3714, 0.8786],
    [0.1462, 0.4243, 0.8796], [0.1282, 0.4738, 0.8680], [0.1145, 0.5201, 0.8480],
    [0.0945, 0.5647, 0.8243], [0.0690, 0.6087, 0.7960], [0.0343, 0.6510, 0.7594],
    [0.0139, 0.6887, 0.7088], [0.0722, 0.7190, 0.6445], [0.1623, 0.7420, 0.5654],
    [0.2588, 0.7596, 0.4775], [0.3585, 0.7709, 0.3864], [0.4609, 0.7734, 0.2982],
    [0.5625, 0.7672, 0.2227], [0.6588, 0.7510, 0.1695], [0.7479, 0.7290, 0.1352],
    [0.8293, 0.7028, 0.1066], [0.8960, 0.6769, 0.0624], [0.9468, 0.6546, 0.0340],
    [0.9725, 0.6460, 0.0380], [0.9769, 0.6568, 0.0942], [0.9710, 0.6818, 0.1554],
    [0.9640, 0.7182, 0.2253], [0.9554, 0.7618, 0.3064], [0.9473, 0.8088, 0.3975],
    [0.9555, 0.8604, 0.4878], [0.9764, 0.9178, 0.5741], [0.9933, 0.9773, 0.6576],
]
parula_cmap = LinearSegmentedColormap.from_list('parula', _parula_data, N=256)

COLORMAPS = {
    'inferno':    {'cmap': 'inferno',    'bg': 'black', 'label': 'Inferno'},
    'magma':      {'cmap': 'magma',      'bg': 'black', 'label': 'Magma'},
    'plasma':     {'cmap': 'plasma',     'bg': 'black', 'label': 'Plasma'},
    'viridis':    {'cmap': 'viridis',    'bg': 'black', 'label': 'Viridis'},
    'cividis':    {'cmap': 'cividis',    'bg': 'black', 'label': 'Cividis'},
    'turbo':      {'cmap': 'turbo',      'bg': 'black', 'label': 'Turbo'},
    'hot':        {'cmap': 'hot',        'bg': 'black', 'label': 'Hot'},
    'copper':     {'cmap': 'copper',     'bg': 'black', 'label': 'Copper'},
    'bone':       {'cmap': 'bone',       'bg': 'black', 'label': 'Bone'},
    'ocean':      {'cmap': 'ocean',      'bg': 'black', 'label': 'Ocean'},
    'cubehelix':  {'cmap': 'cubehelix',  'bg': 'black', 'label': 'Cubehelix'},
    'twilight':   {'cmap': 'twilight',   'bg': 'black', 'label': 'Twilight'},
    'coolwarm':   {'cmap': 'coolwarm',   'bg': '#0a0a1a', 'label': 'Cool-Warm'},
    'gnuplot2':   {'cmap': 'gnuplot2',   'bg': 'black', 'label': 'GnuPlot2'},
    'gray':       {'cmap': 'gray',       'bg': 'black', 'label': 'Grayscale'},
    'pink':       {'cmap': 'pink',       'bg': 'black', 'label': 'Pink'},
    'parula':     {'cmap': parula_cmap,  'bg': 'black', 'label': 'Parula'},
}

data = scipy.io.loadmat('/app/y_data.mat')
fs = int(data['fs'].flatten()[0])
y = data['y'].flatten()
y = y / np.max(np.abs(y))

nperseg = 4096
noverlap = int(nperseg * 0.95)
f, t, Sxx = spectrogram(y, fs=fs, nperseg=nperseg, noverlap=noverlap, window='hann')

Sxx_db = 10 * np.log10(Sxx + 1e-12)
freq_mask = f <= 1750
Sxx_db_band = Sxx_db[freq_mask, :]
vmin = np.percentile(Sxx_db_band, 5)
vmax = np.percentile(Sxx_db_band, 99.5)

print(f"Spectrogram data computed: {len(f)} freq bins, {len(t)} time bins")
print(f"Dynamic range: {vmin:.1f} to {vmax:.1f} dB")

# Accept optional filter arg: python create_spectrogram.py inferno magma
requested = sys.argv[1:] if len(sys.argv) > 1 else list(COLORMAPS.keys())

os.makedirs('/app/output', exist_ok=True)

for name in requested:
    if name not in COLORMAPS:
        print(f"  SKIP unknown: {name}")
        continue
    cfg = COLORMAPS[name]
    outpath = f'/app/output/spectrogram_{name}.png'

    # 4K TV resolution: 3840x2160 — use 2:1 aspect → 3840x1920
    fig, ax = plt.subplots(figsize=(19.2, 9.6), dpi=200)
    ax.pcolormesh(t, f / 1000, Sxx_db,
                  shading='gouraud',
                  cmap=cfg['cmap'],
                  vmin=vmin, vmax=vmax,
                  rasterized=True)
    ax.set_ylim(0, 1.75)
    ax.set_xlim(t[0], t[-1])
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(outpath, dpi=200, bbox_inches='tight', pad_inches=0, facecolor=cfg['bg'])
    plt.close()

    from PIL import Image
    im = Image.open(outpath)
    size_mb = os.path.getsize(outpath) / (1024*1024)
    print(f"  {name}: {im.size[0]}x{im.size[1]} ({size_mb:.1f} MB)")

print("Done.")
