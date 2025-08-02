// Hamming window to smooth signal edges
function applyHammingWindow(signal) {
  return signal.map((val, i) => {
    const w = 0.54 - 0.46 * Math.cos((2 * Math.PI * i) / (signal.length - 1));
    return val * w;
  });
}

// Zero-padding to next power of 2
function zeroPadToNextPowerOf2(arr) {
  const len = arr.length;
  const size = Math.pow(2, Math.ceil(Math.log2(len)));
  const padded = new Float32Array(size);
  padded.set(arr);
  return padded;
}

// FFT using built-in AnalyserNode (for visualization only)
export function analyzeAudioBuffer(audioBuffer, fftSize = 2048) {
  const context = new OfflineAudioContext(1, audioBuffer.length, audioBuffer.sampleRate);
  const source = context.createBufferSource();
  source.buffer = audioBuffer;

  const analyser = context.createAnalyser();
  analyser.fftSize = fftSize;
  const freqData = new Uint8Array(analyser.frequencyBinCount);
  const timeData = new Uint8Array(analyser.fftSize);

  source.connect(analyser);
  analyser.connect(context.destination);
  source.start();

  return context.startRendering().then(() => {
    analyser.getByteTimeDomainData(timeData);
    analyser.getByteFrequencyData(freqData);
    return { timeData, freqData };
  });
}

// Converts frequency bin index to Hz
export function binToFrequency(index, sampleRate, fftSize) {
  return (index * sampleRate) / fftSize;
}
