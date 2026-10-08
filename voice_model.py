import os
from transformers import pipeline

class VoiceTranscriber:
    def __init__(self, model_id="openai/whisper-tiny.en"):
        """
        Initializes the lightweight Whisper model for local transcription.
        """
        print(f"Loading speech model: {model_id}...")
        self.pipe = pipeline(
            task="automatic-speech-recognition",
            model=model_id,
            device="cpu"  # Running on CPU as baseline
        )
        print("Model loaded successfully.")

    def transcribe(self, audio_input):
        """
        Transcribes an audio file path or raw audio array into clean English text.
        
        :param audio_input: Filepath (str) or audio array dict from UI
        :return: Clean transcript string
        """
        if not audio_input:
            return ""
        
        result = self.pipe(audio_input)
        # Strip leading/trailing whitespaces to keep the transcript clean
        return result.get("text", "").strip()

if __name__ == "__main__":
    # Test model initialization
    transcriber = VoiceTranscriber()
    print("Setup verified. The model is ready to process audio files.")