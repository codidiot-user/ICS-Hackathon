import sounddevice as sd
import soundfile as sf
import os

def record_sample(filename, duration=6.0, sample_rate=16000):
    print(f"\n🎤 Recording for {duration} seconds... Please speak now.")
    
    # Record audio: 1 channel (mono), 16kHz
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Wait until the recording is finished
    
    print("✅ Recording finished.")
    
    # Save the file as a 16-bit WAV file in the samples folder
    filepath = os.path.join("samples", filename)
    sf.write(filepath, audio_data, sample_rate, subtype='PCM_16')
    print(f"💾 Saved to {filepath}")

if __name__ == "__main__":
    # List of the first 4 samples to record based on your expected.csv
    samples = [
        "A01_quiet_logesh.wav",
        "A02_quiet_logesh.wav",
        "A03_quiet_logesh.wav",
        "A04_quiet_logesh.wav"
    ]
    
    os.makedirs("samples", exist_ok=True)
    
    for sample in samples:
        input(f"\nPress Enter to start recording {sample}...")
        record_sample(sample, duration=6.0)