let context;
let mediaStream;
let source;
let processor;
let isRecording = false;
let isPaused = false;
let recordedSamples = [];
let recordedChunks = [];

let audioBlob = null;

export async function startRecording() {
  context = new (window.AudioContext || window.webkitAudioContext)();
  mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });

  source = context.createMediaStreamSource(mediaStream);
  processor = context.createScriptProcessor(2048, 1, 1);

  recordedSamples = [];
  recordedChunks = [];
  isRecording = true;
  isPaused = false;

  processor.onaudioprocess = (event) => {
    if (!isRecording || isPaused) return;

    const input = event.inputBuffer.getChannelData(0);
    recordedSamples.push(...input);

    // Save raw audio chunk for blob download later
    const buffer = new Float32Array(input);
    recordedChunks.push(buffer);
  };

  source.connect(processor);
  processor.connect(context.destination);

  return new Promise((resolve) => {
    // Let the app decide when to stop; return live data reference
    resolve({ samples: recordedSamples, sampleRate: context.sampleRate });
  });
}

export function pauseRecording() {
  isPaused = true;
}

export function resumeRecording() {
  isPaused = false;
}

export function stopRecording() {
  isRecording = false;
  processor.disconnect();
  source.disconnect();
  mediaStream.getTracks().forEach(track => track.stop());

  // Convert float32 arrays to 16-bit PCM WAV for download
  audioBlob = exportWAV(recordedSamples, context.sampleRate);
}

export function getAudioBlob() {
  return audioBlob;
}

// -- Helper function to convert to WAV blob --
function exportWAV(samples, sampleRate) {
  const bufferLength = samples.length;
  const wavBuffer = new ArrayBuffer(44 + bufferLength * 2); // 16-bit PCM
  const view = new DataView(wavBuffer);

  function writeString(view, offset, str) {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  }

  // WAV header
  writeString(view, 0, 'RIFF');
  view.setUint32(4, 36 + bufferLength * 2, true);
  writeString(view, 8, 'WAVE');
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true); // PCM format
  view.setUint16(22, 1, true); // Mono
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true); // Block align
  view.setUint16(34, 16, true); // Bits per sample
  writeString(view, 36, 'data');
  view.setUint32(40, bufferLength * 2, true);

  // PCM samples
  for (let i = 0; i < bufferLength; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
  }

  return new Blob([view], { type: 'audio/wav' });
}