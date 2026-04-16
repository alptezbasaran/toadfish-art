import scipy.io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import sys
import os

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

    fig, ax = plt.subplots(figsize=(48, 24), dpi=300)
    ax.pcolormesh(t, f / 1000, Sxx_db,
                  shading='gouraud',
                  cmap=cfg['cmap'],
                  vmin=vmin, vmax=vmax,
                  rasterized=True)
    ax.set_ylim(0, 1.75)
    ax.set_xlim(t[0], t[-1])
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(outpath, dpi=300, bbox_inches='tight', pad_inches=0, facecolor=cfg['bg'])
    plt.close()

    from PIL import Image
    im = Image.open(outpath)
    size_mb = os.path.getsize(outpath) / (1024*1024)
    print(f"  {name}: {im.size[0]}x{im.size[1]} ({size_mb:.1f} MB)")

print("Done.")
