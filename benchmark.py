import csv, json, time, os
import soundfile as sf
import librosa
from transformers import pipeline
from jiwer import wer

MODELS = ["openai/whisper-tiny.en", "openai/whisper-base.en", "openai/whisper-small.en"]
DEVICES = [-1] # -1 = CPU. You can add 0 later to test your GPU.

def load_audio(path):
    audio, sr = sf.read(path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1) # convert to mono
    if sr != 16000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
    return audio.astype("float32")

def clean(t):
    return "".join(c for c in t.lower() if c.isalnum() or c in " /.").strip()

rows = list(csv.DictReader(open("samples/expected.csv")))
results = []

for model in MODELS:
    for dev in DEVICES:
        try:
            print(f"Loading {model} on device {dev}...")
            asr = pipeline("automatic-speech-recognition", model=model, device=dev)
        except Exception as e:
            print("skip", model, dev, e)
            continue
            
        for r in rows:
            audio_path = os.path.join("samples", r["file"])
            if not os.path.exists(audio_path):
                print(f"Missing file: {audio_path}")
                continue
                
            audio = load_audio(audio_path)
            t0 = time.perf_counter()
            text = asr({"raw": audio, "sampling_rate": 16000})["text"]
            lat = time.perf_counter() - t0
            
            results.append({
                "model": model, 
                "device": dev, 
                "file": r["file"],
                "wer": wer(clean(r["expected_transcript"]), clean(text)),
                "latency_s": round(lat, 3),
                "rtf": round(lat / (len(audio) / 16000), 3),
                "text": text,
            })

os.makedirs("docs/results", exist_ok=True)
json.dump(results, open("docs/results/whisper_results.json", "w"), indent=2)
print("Benchmark complete. Results saved to docs/results/whisper_results.json")