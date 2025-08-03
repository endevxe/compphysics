function drawCanvas(canvasId, data, label = 'Value') {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);
  ctx.strokeStyle = '#00ffd5';
  ctx.beginPath();

  const step = Math.floor(data.length / width);
  for (let i = 0; i < width; i++) {
    const value = data[i * step] || 0;
    const y = height / 2 - value * height / 2;
    ctx.lineTo(i, y);
  }

  ctx.stroke();
}

export function plotWaveform(samples) {
  drawCanvas('waveform-canvas', samples);
}

export function plotFFT(samples, sampleRate) {
  const fftSize = 1024;
  const fftData = samples.slice(0, fftSize);
  const windowed = applyHammingWindow(fftData);

  // Basic DFT (not optimized)
  const magnitudes = new Array(fftSize / 2).fill(0);
  for (let k = 0; k < fftSize / 2; k++) {
    let re = 0, im = 0;
    for (let n = 0; n < fftSize; n++) {
      const angle = (2 * Math.PI * k * n) / fftSize;
      re += windowed[n] * Math.cos(angle);
      im -= windowed[n] * Math.sin(angle);
    }
    magnitudes[k] = Math.sqrt(re * re + im * im);
  }

  drawCanvas('fft-canvas', magnitudes);
}

export function plotSpectrogram(samples, sampleRate) {
  const canvas = document.getElementById('spectrogram-canvas');
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  const fftSize = 256;
  const hopSize = 128;
  const rows = Math.floor(samples.length / hopSize) - 1;

  const spectrogram = [];

  for (let r = 0; r < rows; r++) {
    const start = r * hopSize;
    const frame = samples.slice(start, start + fftSize);
    const windowed = applyHammingWindow(frame);

    const row = [];
    for (let k = 0; k < fftSize / 2; k++) {
      let re = 0, im = 0;
      for (let n = 0; n < fftSize; n++) {
        const angle = (2 * Math.PI * k * n) / fftSize;
        re += windowed[n] * Math.cos(angle);
        im -= windowed[n] * Math.sin(angle);
      }
      const mag = Math.sqrt(re * re + im * im);
      row.push(mag);
    }
    spectrogram.push(row);
  }

  const maxVal = Math.max(...spectrogram.flat());
  ctx.clearRect(0, 0, width, height);

  for (let y = 0; y < spectrogram.length; y++) {
    const row = spectrogram[y];
    for (let x = 0; x < row.length; x++) {
      const val = row[x] / maxVal;
      const color = `hsl(${(1 - val) * 260}, 100%, ${val * 100}%)`;
      ctx.fillStyle = color;
      ctx.fillRect(x, height - y, 1, 1);
    }
  }
}

// Optional windowing for better frequency analysis
function applyHammingWindow(data) {
  const N = data.length;
  return data.map((val, n) => val * (0.54 - 0.46 * Math.cos((2 * Math.PI * n) / (N - 1))));
}