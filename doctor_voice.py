# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1a: Setup Text to Speech–TTS–model with gTTS (Google Text-to-Speech - free option)
import os
from gtts import gTTS
from pydub import AudioSegment
import subprocess
import platform
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Convert text to speech using Google's gTTS (free service)
    and play it using the appropriate player for the OS
    """
    language="en"
    logging.info(f"Converting text to speech using gTTS and saving to {output_filepath}")
    
    try:
        # Generate the MP3 file
        audioobj = gTTS(
            text=input_text,
            lang=language,
            slow=False
        )
        audioobj.save(output_filepath)
        logging.info("Audio file saved successfully")
        
        # Convert MP3 to WAV
        wav_filepath = output_filepath.replace(".mp3", ".wav")
        logging.info(f"Converting {output_filepath} to {wav_filepath}")
        audio_segment = AudioSegment.from_mp3(output_filepath)
        audio_segment.export(wav_filepath, format="wav")
        logging.info(f"Converted audio saved as {wav_filepath}")
        
        # Play the WAV file based on the operating system
        os_name = platform.system()
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', wav_filepath])
            elif os_name == "Windows":  # Windows
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
            elif os_name == "Linux":  # Linux
                subprocess.run(['aplay', wav_filepath])  # Alternative: use 'mpg123' or 'ffplay'
            else:
                raise OSError("Unsupported operating system")
            logging.info("Audio playback completed")
        except Exception as e:
            logging.error(f"An error occurred while trying to play the audio: {e}")
    except Exception as e:
        logging.error(f"An error occurred while generating speech: {e}")
        return None
    return output_filepath

# Test the function
# input_text = "hi this is sanskar kasoudhan"
# text_to_speech_with_gtts(input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs (higher quality but requires API key)
from elevenlabs import ElevenLabs

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using ElevenLabs (higher quality, requires API key)
    """
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    if not ELEVENLABS_API_KEY:
        logging.warning("ELEVENLABS_API_KEY not found. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath)
    
    logging.info(f"Converting text to speech using ElevenLabs and saving to {output_filepath}")
    
    try:
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        # Generate audio
        audio = client.text_to_speech(
            text=input_text,
            voice="Aria",
            model="eleven_turbo"
        )
        
        # Save the audio to the specified file
        with open(output_filepath, "wb") as audio_file:
            audio_file.write(audio)
        logging.info("Audio file saved successfully")
        
        # Play the audio based on the operating system
        os_name = platform.system()
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', output_filepath])
            elif os_name == "Windows":  # Windows
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
            elif os_name == "Linux":  # Linux
                subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
            else:
                raise OSError("Unsupported operating system")
            logging.info("Audio playback completed")
        except Exception as e:
            logging.error(f"An error occurred while trying to play the audio: {e}")
    except Exception as e:
        logging.error(f"An error occurred with ElevenLabs: {e}")
        logging.info("Falling back to gTTS...")
        return text_to_speech_with_gtts(input_text, output_filepath)
    
    return output_filepath

# Alternative option: Add a free and open-source TTS option like Piper TTS
def text_to_speech_with_piper(input_text, output_filepath, voice_model="en_US-lessac-medium"):
    """
    Optional implementation using Piper TTS (completely open source and runs locally)
    Note: Requires separate installation of Piper TTS and voice models
    """
    try:
        import subprocess
        import tempfile
        
        # Create temporary text file
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(input_text)
            temp_text_path = temp_file.name
        
        # Run piper command
        subprocess.run([
            'piper',
            '--model', voice_model,
            '--output_file', output_filepath,
            '--text_file', temp_text_path
        ])
        
        # Clean up
        os.unlink(temp_text_path)
        
        # Play audio
        os_name = platform.system()
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])
        else:
            raise OSError("Unsupported operating system")
            
        return output_filepath
    except Exception as e:
        logging.error(f"Error using Piper TTS: {e}")
        logging.info("Falling back to gTTS...")
        return text_to_speech_with_gtts(input_text, output_filepath)