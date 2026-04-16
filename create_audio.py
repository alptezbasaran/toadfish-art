import scipy.io
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

data = scipy.io.loadmat('/app/y_data.mat')
fs = int(data['fs'].flatten()[0])
y = data['y'].flatten()

# Normalize to [-1, 1] for WAV output
y_norm = y / np.max(np.abs(y))

# Full-band audio
sf.write('/app/output/shannon_10s.wav', y_norm, fs, subtype='PCM_24')
print(f"WAV (full): {len(y_norm)} samples, {fs} Hz, {len(y_norm)/fs:.2f}s, 24-bit PCM")

# Low-pass filtered audio (0 - 1750 Hz)
sos = butter(8, 1750, btype='low', fs=fs, output='sos')
y_lp = sosfilt(sos, y_norm)
y_lp = y_lp / np.max(np.abs(y_lp))  # Re-normalize after filtering

sf.write('/app/output/shannon_10s_1750hz.wav', y_lp, fs, subtype='PCM_24')
print(f"WAV (0-1750 Hz): {len(y_lp)} samples, {fs} Hz, {len(y_lp)/fs:.2f}s, 24-bit PCM")
