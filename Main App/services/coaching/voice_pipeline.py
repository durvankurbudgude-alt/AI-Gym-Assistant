import time
import streamlit as st

class VoicePipeline:
    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts
        self.last_spoken_at = 0

    def _find_form_issue(self, exercise, metrics):
        if not metrics:
            return None
            
        if "issue" in metrics:
            return metrics["issue"]
            
        # Check if a custom injected milestone message was passed directly from main.py
        if "custom_message" in metrics:
            return metrics["custom_message"]

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
        # Determine contextual issues or milestone strings
        issue = self._find_form_issue(exercise, metrics)
        now = time.time()

        # Check if this is a high-priority workout event
        is_major_event = event in ["workout_started", "set_completed", "workout_completed", "rep_milestone"]

        # If it's a minor check but no posture problem was identified, skip
        if not is_major_event:
            if not issue:
                return None
            # Rate limit minor form voice drops to once every 5 seconds
            if now - self.last_spoken_at < 5:
                return None
            
        # Fallback if no specific string was built but event must talk
        if not issue:
            issue = f"The user is progressing through the {exercise} routine."

        # Pass context clean to your Groq core engine using its correct method name
        try:
            # We check if your LLM module has give_feedback, otherwise fallback to generate_response
            if hasattr(self.llm, "give_feedback"):
                text = self.llm.give_feedback(event, issue)
            else:
                text = self.llm.generate_response(event, exercise, metrics)
                
            if not text:
                return None

            # Generate the raw audio bytes using your gTTS backend
            voice = self.tts.speak(text)
            
            self.last_spoken_at = now
            return voice, text
            
        except Exception as e:
            print(f"Voice Pipeline Execution Error: {e}")
            return None
