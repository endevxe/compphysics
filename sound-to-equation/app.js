import { startRecording } from './audioProcessor.js';
import { plotWaveform, plotFFT, updateSpectrogram, drawSpectrogram, detectPitch } from './waveformVisualizer.js';

let isRecording = false;
let audioContext;
let mediaRecorder;
let recordedChunks = [];
let animationFrame;
let pauseRequested = false;

const recordBtn = document.getElementById('record-btn');
const pauseBtn = document.getElementById('pause-btn');
const downloadAudioBtn = document.getElementById('download-audio');
const downloadWaveformBtn = document.getElementById('download-waveform');

recordBtn.addEventListener('click', async () => {
  if (!isRecording) {
    isRecording = true;
    recordedChunks = [];
    recordBtn.textContent = 'Stop Recording';
    pauseBtn.disabled = false;

    const { context, source, processor, stream } = await startRecording();
    audioContext = context;

    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) recordedChunks.push(e.data);
    };
    mediaRecorder.start();

    const waveformCanvas = document.getElementById('waveform-canvas');
    const fftCanvas = document.getElementById('fft-canvas');
    const spectrogramCanvas = document.getElementById('spectrogram');
    const waveformCtx = waveformCanvas.getContext('2d');
    const fftCtx = fftCanvas.getContext('2d');
    const spectrogramCtx = spectrogramCanvas.getContext('2d');

    const fftSize = 2048;
    const analyser = context.createAnalyser();
    analyser.fftSize = fftSize;
    source.connect(analyser);

    const bufferLength = analyser.frequencyBinCount;
    const timeData = new Uint8Array(bufferLength);
    const freqData = new Uint8Array(bufferLength);
    let spectrogramOffset = 0;

    function draw() {
      if (!isRecording) return;
      if (pauseRequested) {
        animationFrame = requestAnimationFrame(draw);
        return;
      }

      analyser.getByteTimeDomainData(timeData);
      analyser.getByteFrequencyData(freqData);

      plotWaveform(timeData);
      plotFFT(freqData);

      // Pitch detection (simplified)
      const pitch = detectPitch(timeData, context.sampleRate);
      document.getElementById('pitch').textContent = pitch ? `Pitch: ${pitch.toFixed(2)} Hz` : 'Pitch: --';

      // Spectrogram
      updateSpectrogram(spectrogramCtx, freqData, spectrogramOffset);
      spectrogramOffset++;

      animationFrame = requestAnimationFrame(draw);
    }

    draw();

  } else {
    isRecording = false;
    recordBtn.textContent = 'Start Recording';
    pauseBtn.textContent = 'Pause';
    pauseBtn.disabled = true;
    cancelAnimationFrame(animationFrame);

    mediaRecorder.stop();
    audioContext.close();

    const audioBlob = new Blob(recordedChunks, { type: 'audio/webm' });
    const audioUrl = URL.createObjectURL(audioBlob);
    downloadAudioBtn.href = audioUrl;
    downloadAudioBtn.download = 'recording.webm';
  }
});

pauseBtn.addEventListener('click', () => {
  pauseRequested = !pauseRequested;
  pauseBtn.textContent = pauseRequested ? 'Resume' : 'Pause';
});

downloadWaveformBtn.addEventListener('click', () => {
  const canvas = document.getElementById('waveform-canvas');
  const link = document.createElement('a');
  link.download = 'waveform.png';
  link.href = canvas.toDataURL();
  link.click();
});
