# Shannon Art Project

## Overview
Artistic visualizations of audio data for an art show exhibition.

## Source Data
- **File**: `y_data.mat` (MATLAB format)
- **Variable `y`**: Raw audio signal, 480,049 samples, float64
- **Variable `fs`**: Sample rate = 48,000 Hz
- **Variable `chunkDur`**: 10 seconds
- **Duration**: 10.00 seconds, single channel

## Outputs

### Audio Files
| File | Description |
|------|-------------|
| `output/shannon_10s.wav` | Full-band audio, 24-bit PCM, 48 kHz |
| `output/shannon_10s_1750hz.wav` | Low-pass filtered to 0-1750 Hz, 24-bit PCM, 48 kHz |

### Spectrogram
| File | Description |
|------|-------------|
| `output/spectrogram_art.png` | Artistic spectrogram, 14400x7200 px (48"x24" at 300 DPI) |

**Spectrogram parameters**:
- Frequency range: 0 - 1,750 Hz
- Window: Hann, 4096 samples
- Overlap: 95% (3891 samples)
- Dynamic range: ~48 dB (5th-99.5th percentile within band)
- Colormap: inferno
- No axes/labels — clean art piece

## Web Page
- **GitHub Pages**: [alptezbasaran.github.io/toadfish-art](https://alptezbasaran.github.io/toadfish-art/)
- **Remote**: `https://github.com/alptezbasaran/toadfish-art`
- `index.html` — full-screen spectrogram with play/loop audio controls, info modal, QR overlay
- `assets/qr.svg` — QR code pointing to the live page
- `Dockerfile.web` — nginx container for local testing
- `.github/workflows/deploy.yml` — GitHub Pages deployment

## Pipeline
All processing runs in Docker (`shannon-art` image). Scripts:
- `create_audio.py` — generates WAV files (full-band + 1750 Hz filtered)
- `create_spectrogram.py` — generates the artistic spectrogram
- `generate_qr.py` — generates QR code SVG

### Build & Run (processing)
```bash
docker build -t shannon-art .
docker run --rm -v $(pwd):/app shannon-art python3 /app/create_audio.py
docker run --rm -v $(pwd):/app shannon-art python3 /app/create_spectrogram.py
```

### Local web preview
```bash
docker build -f Dockerfile.web -t toadfish-art .
docker run --rm -p 8080:80 toadfish-art
# Open http://localhost:8080
```
