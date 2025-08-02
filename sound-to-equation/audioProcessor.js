export async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const context = new AudioContext();
  const source = context.createMediaStreamSource(stream);
  const processor = context.createScriptProcessor(2048, 1, 1);

  const samples = [];

  processor.onaudioprocess = (event) => {
    const input = event.inputBuffer.getChannelData(0);
    samples.push(...input);
  };

  source.connect(processor);
  processor.connect(context.destination);

  return new Promise(resolve => {
    setTimeout(() => {
      processor.disconnect();
      source.disconnect();
      resolve({ samples, sampleRate: context.sampleRate });
    }, 3000); // Record for 3 seconds
  });
}
