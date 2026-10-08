import time
from transformers import pipeline

class VoiceTranscriber:
    def __init__(self, model_id="openai/whisper-tiny.en"):
        self.model_id = model_id
        self.pipe = pipeline(
            task="automatic-speech-recognition",
            model=self.model_id,
            device="cpu" 
        )

    def transcribe(self, audio_input, duration_s=0.0):
        """
        Transcribes audio while strictly adhering to the shared contract.
        """
        response = {"ok": False, "data": {}, "errors": []}
        
        # Error: AUDIO_TOO_LONG (> 30s limit)
        if duration_s > 30.0:
            response["errors"].append({"code": "AUDIO_TOO_LONG", "message": "Audio exceeds 30 seconds limit"})
            return response

        # Error: EMPTY_AUDIO
        if not audio_input:
            response["errors"].append({"code": "EMPTY_AUDIO", "message": "No audio or only silence detected"})
            return response

        try:
            start_time = time.perf_counter()
            
            # The pipeline handles 16kHz float32 preprocessing automatically
            result = self.pipe(audio_input)
            text = result.get("text", "").strip()
            
            latency_s = round(time.perf_counter() - start_time, 3)

            if not text:
                response["errors"].append({"code": "EMPTY_AUDIO", "message": "Audio resulted in empty transcript"})
                return response

            # Success
            response["ok"] = True
            response["data"] = {
                "text": text,
                "duration_s": duration_s,
                "model": self.model_id,
                "latency_s": latency_s
            }
            
        except Exception as e:
            # Error: STT_FAILED
            response["errors"].append({"code": "STT_FAILED", "message": str(e)})

        return response

if __name__ == "__main__":
    transcriber = VoiceTranscriber()
    # Mock testing the new contract
    print(transcriber.transcribe("fictional_request.wav", duration_s=5.0))