import { startRecording } from './audioProcessor.js';
import { plotWaveform, plotFFT } from './waveformVisualizer.js';

document.getElementById('record-btn').addEventListener('click', async () => {
  const { samples, sampleRate } = await startRecording();
  plotWaveform(samples);
  plotFFT(samples, sampleRate);
});
