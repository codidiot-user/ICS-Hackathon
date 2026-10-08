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
    os.makedirs("samples", exist_ok=True)
    
    samples = {
        "A01_quiet_logesh.wav": 10.0,
        "A02_quiet_logesh.wav": 9.0,
        "A03_quiet_logesh.wav": 8.0,
        "A04_quiet_logesh.wav": 8.0,
    }
    
    # Notice the .items() and duration=duration here
    for filename, duration in samples.items():
        input(f"\nPress Enter to start recording {filename} ({duration} seconds)...")
        record_sample(filename, duration=duration)
