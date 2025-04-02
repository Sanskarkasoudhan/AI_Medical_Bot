# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup Gemini API key
import os
import logging

GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")

#Step2: Convert image to required format
import base64
import pathlib

def encode_image(image_path):
    """
    Read image file in binary mode
    Note: Gemini doesn't require base64 encoding, but we'll keep this function
    to maintain compatibility with the rest of the code structure
    """
    with open(image_path, "rb") as image_file:
        return image_file.read()

#Step3: Setup Multimodal LLM 
import google.generativeai as genai

def analyze_image_with_query(query, model, encoded_image):
    """
    Analyze an image with Gemini API
    """
    # Configure the Gemini API
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Select the Gemini Pro Vision model
    gemini_model = genai.GenerativeModel('gemini-1.5-pro')
    
    # Create the content parts: text query and image
    content_parts = [
        query,
        {"mime_type": "image/jpeg", "data": encoded_image}
    ]
    
    # Generate response
    try:
        response = gemini_model.generate_content(content_parts)  # Removed timeout
        return response.text
    except Exception as e:
        logging.error(f"An error occurred while generating content: {e}")
        return "Error: Unable to process the image query."

# def process_inputs(audio_filepath, image_filepath):
#     # Transcribe the audio
#     logging.info(f"Processing audio file: {audio_filepath}")
#     speech_to_text_output = transcribe_with_whisper_local(audio_filepath=audio_filepath)
#     logging.info(f"Transcribed Text: {speech_to_text_output}")

#     # Handle the image input
#     if image_filepath:
#         logging.info(f"Processing image file: {image_filepath}")
#         doctor_response = analyze_image_with_query(
#             query=system_prompt + " " + speech_to_text_output, 
#             encoded_image=encode_image(image_filepath), 
#             model=None  # Model is specified in the function directly for Gemini
#         )
#         logging.info(f"Doctor's Response: {doctor_response}")
#     else:
#         doctor_response = "No image provided for me to analyze"
#         logging.info("No image provided for analysis.")

#     # Generate the doctor's voice response
#     doctor_voice = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3")
#     if doctor_voice and os.path.exists(doctor_voice):
#         logging.info(f"Doctor's voice response saved to: {doctor_voice}")
#     else:
#         logging.error("Failed to generate doctor's voice response.")
#         doctor_voice = None

#     return speech_to_text_output, doctor_response, doctor_voice

# import gradio as gr

# iface = gr.Interface(
#     fn=process_inputs,
#     inputs=[
#         gr.Audio(sources=["microphone"], type="filepath", label="Patient's Voice"),
#         gr.Image(type="filepath", label="Medical Image")
#     ],
#     outputs=[
#         gr.Textbox(label="Speech to Text"),
#         gr.Textbox(label="Doctor's Response"),
#         gr.Audio(type="filepath", label="Doctor's Voice")
#     ],
#     title="AI Doctor with Vision and Voice",
#     description="Upload a medical image and speak into the microphone. The AI doctor will analyze the image and respond with a diagnosis and remedies."
# )