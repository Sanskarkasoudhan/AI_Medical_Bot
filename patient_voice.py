# # if you dont use pipenv uncomment the following:
# # from dotenv import load_dotenv
# # load_dotenv()

# #Step1: Setup Audio recorder (ffmpeg & portaudio)
# # ffmpeg, portaudio, pyaudio
# import logging
# import speech_recognition as sr
# from pydub import AudioSegment
# from io import BytesIO

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def record_audio(file_path, timeout=20, phrase_time_limit=None):
#     """
#     Simplified function to record audio from the microphone and save it as an MP3 file.

#     Args:
#     file_path (str): Path to save the recorded audio file.
#     timeout (int): Maximum time to wait for a phrase to start (in seconds).
#     phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
#     """
#     recognizer = sr.Recognizer()
    
#     try:
#         with sr.Microphone() as source:
#             logging.info("Adjusting for ambient noise...")
#             recognizer.adjust_for_ambient_noise(source, duration=1)
#             logging.info("Start speaking now...")
            
#             # Record the audio
#             audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
#             logging.info("Recording complete.")
            
#             # Convert the recorded audio to an MP3 file
#             wav_data = audio_data.get_wav_data()
#             audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
#             audio_segment.export(file_path, format="mp3", bitrate="128k")
            
#             logging.info(f"Audio saved to {file_path}")

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")

# audio_filepath = "patient_voice_test_for_patient.mp3"
# record_audio(file_path=audio_filepath)

# #Step2: Setup Speech to text–STT–model for transcription with Whisper Local
# import os
# import torch
# import whisper

# def transcribe_with_whisper_local(audio_filepath):
#     """
#     Transcribe audio using locally run Whisper model
#     """
#     try:
#         # Convert MP3 to WAV
#         wav_filepath = audio_filepath.replace(".mp3", ".wav")
#         audio_segment = AudioSegment.from_mp3(audio_filepath)
#         audio_segment.export(wav_filepath, format="wav")
        
#         # Load the Whisper model
#         model_size = "base"
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         logging.info(f"Using device: {device}")
#         model = whisper.load_model(model_size, device=device)
        
#         # Transcribe the audio
#         logging.info(f"Transcribing audio file: {wav_filepath}")
#         result = model.transcribe(wav_filepath)
        
#         # Check if transcription result is valid
#         if "text" in result and result["text"].strip():
#             return result["text"]
#         else:
#             logging.error("Transcription failed or returned empty text.")
#             return "Transcription failed or returned empty text."
#     except Exception as e:
#         logging.error(f"An error occurred during transcription: {e}")
#         return f"An error occurred: {e}"

# # Transcribe the recorded audio
# transcribed_text = transcribe_with_whisper_local(audio_filepath)

# # Print the transcribed text
# logging.info(f"Transcribed Text: {transcribed_text}")
# print(f"Transcribed Text: {transcribed_text}")

# If you don't use pipenv, uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# Step 1: Setup Audio Recorder (ffmpeg & portaudio)
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
import torch
import whisper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Define the file path for recorded audio
audio_filepath = "patient_voice_test.mp3"

# Record the audio
#record_audio(file_path=audio_filepath)

# Step 2: Setup Speech-to-Text (STT) using Whisper Local
def transcribe_with_whisper_local(audio_filepath):
    """
    Transcribe audio using a locally run Whisper model with improved debugging.
    """
    try:
        # Convert MP3 to WAV
        wav_filepath = audio_filepath.replace(".mp3", ".wav")
        logging.info(f"Converting {audio_filepath} to {wav_filepath}")
        
        # Ensure ffmpeg is working properly
        try:
            audio_segment = AudioSegment.from_mp3(audio_filepath)
        except Exception as e:
            logging.error(f"Error loading MP3 file: {e}")
            return "Error in MP3 file conversion."

        audio_segment.export(wav_filepath, format="wav")

        # Check if WAV file exists and has a valid duration
        if not os.path.exists(wav_filepath):
            logging.error("WAV file was not created successfully.")
            return "Error: WAV file not created."

        if os.path.getsize(wav_filepath) < 1000:
            logging.error("WAV file is too small, likely an empty recording.")
            return "Error: Empty or corrupt WAV file."

        # Load the Whisper model
        model_size = "base"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Using device: {device}")
        model = whisper.load_model(model_size, device=device)

        # Transcribe the audio
        logging.info(f"Transcribing audio file: {wav_filepath}")
        result = model.transcribe(wav_filepath)

        # Check if transcription result is valid
        if "text" in result and result["text"].strip():
            return result["text"]
        else:
            logging.error("Transcription failed or returned empty text.")
            return "Transcription failed or returned empty text."
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        return f"An error occurred: {e}"

# Transcribe the recorded audio
transcribed_text = transcribe_with_whisper_local(audio_filepath)

# Print the transcribed text
logging.info(f"Transcribed Text: {transcribed_text}")
# print(f"Transcribed Text: {transcribed_text}")
