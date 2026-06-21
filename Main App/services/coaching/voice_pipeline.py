import time
import streamlit as st


class VoicePipeline:
    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts
        self.last_spoken_at = 0

    def _find_form_issue(self, exercise, metrics):
        if "issue" in metrics:
            return metrics["issue"]

        if exercise == "Squats":
            depth = metrics.get("depth_status", "")
            back_angle = metrics.get("back_angle", 180)
            
            if depth == "TOO HIGH":
                return "The user's squat is not deep enough — knees are not bending sufficiently."

            if isinstance(back_angle, (int, float)) and back_angle < 130:
                return "The user is leaning too far forward during the squat."

        elif exercise == "Push-ups":
            alignment = metrics.get("body_alignment", "")
            hip_status = metrics.get("hip_status", "")
            
            if alignment == "Poor Form":
                return "The user's body is not straight during the push-up."

            if hip_status == "SAGGING":
                return "The user's hips are sagging down during the push-up."

            if hip_status == "PIKED UP":
                return "The user's hips are too high — lower them to form a straight line."

        elif exercise == "Biceps Curls (Dumbbell)":
            swing = metrics.get("swing_status", "")
            shoulder = metrics.get("shoulder_status", "")
            
            if swing == "SWINGING":
                return "The user is swinging their torso during the curl — keep the body still."

            if shoulder == "ELBOW DRIFTING":
                return "The user's elbow is drifting away from their side during the curl."

        elif exercise == "Shoulder Press":
            back_arch = metrics.get("back_arch_status", "")
            extension = metrics.get("extension_status", "")
            
            if back_arch == "Excessive Arch":
                return "The user is arching their lower back excessively during the press."

            if back_arch == "Slight Arch":
                return "Slight back arch detected — encourage the user to brace their core."

        elif exercise == "Lunges":
            balance = metrics.get("balance_status", "")
            
            if balance == "OFF BALANCE":
                return "The user is losing balance during the lunge — feet should be hip-width apart."

        return None
    
    def process_event(self, event, exercise, metrics):
        print("=" * 60)
        print("VOICE EVENT:", event)
        print("EXERCISE:", exercise)
        print("METRICS:", metrics)

        issue = self._find_form_issue(exercise, metrics)

        print("ISSUE FOUND:", issue)
    def process_event(self, event, exercise, metrics):
        issue = self._find_form_issue(exercise, metrics)

        now = time.time()

        is_major_issue = event in ["workout_started", "set_completed", "workout_completed"]

        if not is_major_issue:
            if not issue:
                return None
            
            if now - self.last_spoken_at < 5:
                return None
            
        text = self.llm.give_feedback(event, issue)
        voice = self.tts.speak(text)

        self.last_spoken_at = now

        return voice, text
    

def autoplay_audio(audio_text):
    """
    FIXED: Uses a data URI embedded inside an un-refreshable sandboxed iframe.
    This prevents Streamlit's 0.25s main loop rerun from cutting off the browser's speech engine.
    """
    if not audio_text:
        return
    
    # Clean string format for JavaScript injection
    safe_text = str(audio_text).replace('"', '\\"').replace('\n', ' ')
    
    # Unique ID to force re-evaluation on new feedback text
    import time
    unique_id = int(time.time() * 1000)
    
    # We embed the text-to-speech script inside a self-contained document string
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head><script>
        window.onload = function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel(); // clear previous queues
                var utterance = new SpeechSynthesisUtterance("{safe_text}");
                utterance.rate = 1.1;
                window.speechSynthesis.speak(utterance);
            }}
        }};
    </script></head>
    <body></body>
    </html>
    """
    
    # Convert html to inline base64 data src so it loads independently of Streamlit's layout engine
    import base64
    b64_html = base64.b64encode(html_code.encode('utf-8')).decode('utf-8')
    
    # Render the sandboxed frame in the sidebar
    st.components.v1.html(
        f'<iframe src="data:text/html;base64,{b64_html}" width="0" height="0" style="display:none; border:none;"></iframe>',
        height=0,
    )
