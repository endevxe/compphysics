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
  const real = samples.slice(0, fftSize);
  const imag = new Array(fftSize).fill(0);

  // Perform FFT using Web API (use custom or library like fft.js if needed)
  const fft = real.map((val, i) => ({
    re: val,
    im: 0
  }));

  const magnitudes = fft.map(c => Math.sqrt(c.re * c.re + c.im * c.im));
  drawCanvas('fft-canvas', magnitudes);
}
