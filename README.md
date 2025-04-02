# AI Doctor 2.0 - Vision and Voice Medical Assistant

An AI-powered medical assistant that can see and hear. This project combines vision AI to analyze medical images and voice AI to communicate naturally with patients.

## 🔍 Overview

AI Doctor 2.0 is a multimodal AI medical assistant that can:

- Process patient voice input through a microphone
- Analyze medical images to identify potential conditions
- Generate doctor-like responses for medical concerns
- Speak responses aloud in natural voice

The system uses Google's Gemini for multimodal reasoning, WhisperAI for speech recognition, and offers multiple text-to-speech options.

## 🛠️ Technologies

- **AI Models**:
  - Google Gemini Pro Vision (multimodal LLM)
  - Whisper (local speech-to-text)
  - gTTS, ElevenLabs, and Piper (text-to-speech)
  
- **Frameworks & Libraries**:
  - Gradio (UI interface)
  - Python (core language)
  - OpenCV (image processing)
  - NumPy, PIL (image handling)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Sanskarkasoudhan/AI_Medical_Bot.git
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here  # Optional, will use gTTS if not provided
```

## 🏃‍♀️ Usage

1. Run the Gradio app:
```bash
python gradio_app.py
```

2. Open your browser and go to:
```
http://127.0.0.1:7860
```

3. Use the interface to:
   - Record audio through your microphone
   - Upload a medical image
   - Get both text and spoken responses from the AI Doctor

## 📁 Project Structure

```
├── brain_of_the_doctor.py        # Handles image analysis with Gemini
├── voice_of_the_patient.py       # Handles audio recording and transcription
├── voice_of_the_doctor.py        # Handles text-to-speech conversion
├── gradio_app.py                 # Gradio UI integration
└── README.md                     # Project documentation
```

## 📘 Component Details

### Brain of the Doctor (Gemini Vision)
- Processes images to identify medical conditions
- Analyzes both images and text context together
- Provides medical analysis based on visual data

### Voice of the Patient (Whisper)
- Records audio from microphone
- Transcribes speech to text locally using Whisper models
- Processes patient questions or concerns

### Voice of the Doctor (TTS)
- Converts AI-generated text responses to natural speech
- Supports multiple TTS options:
  - gTTS (Google Text-to-Speech, free)
  - ElevenLabs (premium voice quality, requires API key)
  - Piper TTS (optional, fully local & open source)

### Gradio UI
- Provides intuitive interface for patient interaction
- Handles input/output between components
- Displays transcriptions, responses, and plays audio

## 📋 Requirements

- Python 3.8+
- FFmpeg (for audio processing)
- Microphone and speakers
- Internet connection for Gemini API
- GPU recommended for faster local Whisper processing

## 🔒 Privacy & Ethics

This application is designed for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

All patient data is processed locally when possible, with only necessary information sent to external APIs for analysis.

## 🔄 Alternative Models

The project is designed to be modular. You can swap components:

- **For Vision**: Replace Gemini with other multimodal models
- **For Speech-to-Text**: Use other local STT models
- **For Text-to-Speech**: Try different TTS options.


