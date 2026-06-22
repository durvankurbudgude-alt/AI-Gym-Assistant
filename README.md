# 🏋️‍♂️ AI Real-time GYM Coach

An interactive, multi-threaded computer vision application that provides real-time posture tracking, automatic repetition counting, and proactive, context-aware AI voice coaching via low-latency LLM inference pipelines.

---

## 🚀 Features

* **Real-time Kinematic Tracking:** Extracts 33 foundational body topology landmarks via MediaPipe Pose to compute exact anatomical joint angles (e.g., knee extension depth, elbow flexion).
* **Low-Latency Live Video Streaming:** Implements `streamlit-webrtc` to handle high-performance, asynchronous webcam processing loops without stalling the browser main UI thread.
* **Proactive Voice Coaching Pipeline:** Integrates Groq LLM API with an efficient Text-to-Speech (TTS) module to generate real-time voice prompts based on current performance milestones.
* **Browser Autoplay Optimization:** Streams generated audio dynamically using localized base64 HTML5 audio element injection to prevent canvas/video re-render conflicts.
* **Local Data Analytics:** Logs workout history (total reps, sets completed, and duration) securely into an SQLite3 relational data tier with Pandas aggregation.

---

## 🛠️ Tech Stack

* **Frontend Framework:** Streamlit
* **Computer Vision & Processing:** MediaPipe Pose, OpenCV, `streamlit-webrtc`
* **AI Orchestration & Inference:** Groq API (LLM Coach Engine)
* **Audio Engineering:** gTTS / Text-to-Speech Engine, Base64 Streaming
* **Database Management:** SQLite3, Pandas

---

## 📂 Project Architecture

```text
AI_GYM_COACH/
├── Main App/
│   └── main.py                 # Core application controller and UI layout
├── services/
│   ├── auth/
│   │   └── login_wall.py       # User authentication barrier
│   ├── coaching/
│   │   ├── llm.py              # Groq API context configuration logic
│   │   ├── tts.py              # Text-to-Speech raw byte conversion
│   │   └── voice_pipeline.py   # Event orchestration pipeline
│   ├── config/
│   │   └── workout_config.py   # Exercise bounds and standard options
│   ├── persistence/
│   │   └── exercise_repository.py # SQLite database CRUD wrappers
│   ├── state/
│   │   └── session_defaults.py # Streamlit SessionState safety locks
│   ├── tracking/
│   │   └── metrics.py          # State-sync wrappers from video context
│   └── vision/
│       └── exercise_video_processor.py # MediaPipe background execution thread
├── static/
│   ├── style.css               # Personalized UI layout styling
│   └── AdobeClean.otf          # Specialized local application font
├── .env                        # Local environment secrets storage
├── requirements.txt            # Application Python dependency manifest
└── packages.txt                # System-level dependencies for deployment



⚙️ Supported Exercise Profiles
The system computes specialized algorithmic checks for different movements:

Squats: Monitors hip/knee angles for optimal depth while checking spinal curvature via back alignment.

Push-ups: Tracks core rigidity, hip positioning heights, and elbow flexion values.

Biceps Curls: Measures elbow angle swings and flags momentum cheating via shoulder isolation states.

Shoulder Press: Evaluates arm extension ranges and hyper-arched lower back positioning.

Lunges: Analyzes front-knee terminal extension and stability balancing parameters.

📦 Installation & Setup
1. Clone the Repository
Bash
git clone https://github.com/durvankurbudgude-alt/AI-Gym-Assistant.git
cd AI-Gym-Assistant
2. Set Up a Virtual Environment
Bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Secrets
Create a .env file in the root directory of the project:

Code snippet
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
5. Run the Application
Bash
streamlit run "Main App/main.py"
☁️ Deployment Guide (Streamlit Cloud)
Commit and push your code repository cleanly to GitHub.

Log into the Streamlit Cloud Dashboard and choose New App.

Point the application settings to your target branch and set the Main file path to Main App/main.py.

Go to Advanced Settings ➡️ Secrets and paste your API key inside the TOML configurations pane:

Ini, TOML
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
Click Deploy! 🚀
