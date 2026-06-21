import io
from gtts import gTTS

class TextToSpeech:
    def __init__(self):
        pass

    def speak(self, text: str):
        """
        Generates genuine MP3 audio bytes using gTTS.
        """
        cleaned = (text or "").strip()
        if not cleaned:
            return None
        
        try:
            # Create an in-memory byte stream buffer
            fp = io.BytesIO()
            tts = gTTS(text=cleaned, lang='en', tld='com')
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()  # Returns raw mp3 bytes cleanly
        except Exception as e:
            print(f"gTTS Generation failed: {e}")
            return None
