from io import BytesIO
from gtts import gTTS


class TextToSpeech:
    def __init__(self):
        pass

    def speak(self, text: str):
        """
        Passes the text string down the pipeline cleanly.
        We let the browser handle the actual voice synthesis natively.
        """
        cleaned = (text or "").strip()
        if not cleaned:
            return None
        return cleaned
