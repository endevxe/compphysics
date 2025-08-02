let audioContext, analyser, dataArray, sourceNode, recorder;
let recording = false;
let chunks = [];

const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const micIcon = document.getElementById("mic-icon");
const equationBox = document.getElementById("equation");
const canvas = document.getElementById("waveform");
const canvasCtx = canvas.getContext("2d");

canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

startBtn.addEventListener("click", async () => {
  if (recording) return;
  recording = true;
  chunks = [];

  audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

  sourceNode = audioContext.createMediaStreamSource(stream);
  analyser = audioContext.createAnalyser();
  analyser.fftSize = 2048;

  const bufferLength = analyser.fftSize;
  dataArray = new Uint8Array(bufferLength);

  sourceNode.connect(analyser);

  recorder = new MediaRecorder(stream);
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.onstop = () => {
    const blob = new Blob(chunks);
    analyzeAudio(blob);
  };
  recorder.start();

  micIcon.classList.add("active");
  drawWaveform(); // start drawing
});

stopBtn.addEventListener("click", () => {
  if (!recording) return;
  recording = false;
  recorder.stop();
  micIcon.classList.remove("active");
});

function drawWaveform() {
  if (!recording) return;

  requestAnimationFrame(drawWaveform);

  analyser.getByteTimeDomainData(dataArray);

  canvasCtx.fillStyle = "#111";
  canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

  canvasCtx.lineWidth = 2;
  canvasCtx.strokeStyle = "#00ff88";
  canvasCtx.beginPath();

  const sliceWidth = canvas.width / dataArray.length;
  let x = 0;

  for (let i = 0; i < dataArray.length; i++) {
    const v = dataArray[i] / 128.0; // Normalize
    const y = (v * canvas.height) / 2;

    if (i === 0) {
      canvasCtx.moveTo(x, y);
    } else {
      canvasCtx.lineTo(x, y);
    }
    x += sliceWidth;
  }

  canvasCtx.lineTo(canvas.width, canvas.height / 2);
  canvasCtx.stroke();
}

function analyzeAudio(blob) {
  const reader = new FileReader();
  reader.onload = () => {
    audioContext.decodeAudioData(reader.result, (buffer) => {
      const channelData = buffer.getChannelData(0);
      const fftData = fft(channelData);
      const freqPeaks = findPeaks(fftData);
      const equation = convertToEquation(freqPeaks);
      equationBox.textContent = equation;
    });
  };
  reader.readAsArrayBuffer(blob);
}

function fft(buffer) {
  // Simple FFT stub - replace with real lib like DSP.js or similar
  const N = buffer.length;
  const freq = new Float32Array(N);
  for (let i = 0; i < N; i++) freq[i] = Math.abs(buffer[i]);
  return freq;
}

function findPeaks(fftData) {
  const peaks = [];
  for (let i = 1; i < fftData.length - 1; i++) {
    if (fftData[i] > fftData[i - 1] && fftData[i] > fftData[i + 1]) {
      peaks.push({ index: i, amplitude: fftData[i] });
    }
  }
  return peaks.slice(0, 5); // Top 5 peaks
}

function convertToEquation(peaks) {
  let equation = "f(t) = ";
  peaks.forEach((p, i) => {
    const freq = (p.index * audioContext.sampleRate) / analyser.fftSize;
    const amp = (p.amplitude * 10).toFixed(2);
    equation += `${amp}·sin(2π·${freq.toFixed(1)}t)`;
    if (i < peaks.length - 1) equation += " + ";
  });
  return equation;
}