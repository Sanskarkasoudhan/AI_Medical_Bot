# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#VoiceBot UI with Gradio
import os
import gradio as gr
import logging

from brain_doctor import encode_image, analyze_image_with_query
from patient_voice import record_audio, transcribe_with_whisper_local
from doctor_voice import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

#load_dotenv()

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):
    # Transcribe the audio
    logging.info(f"Processing audio file: {audio_filepath}")
    speech_to_text_output = transcribe_with_whisper_local(audio_filepath=audio_filepath)
    logging.info(f"Transcribed Text: {speech_to_text_output}")

    # Handle the image input
    if image_filepath:
        logging.info(f"Processing image file: {image_filepath}")
        doctor_response = analyze_image_with_query(
            query=system_prompt + " " + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model=None  # Model is specified in the function directly for Gemini
        )
        logging.info(f"Doctor's Response: {doctor_response}")
    else:
        doctor_response = "No image provided for me to analyze"
        logging.info("No image provided for analysis.")

    # Generate the doctor's voice response
    doctor_voice = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3")
    if doctor_voice and os.path.exists(doctor_voice):
        logging.info(f"Doctor's voice response saved to: {doctor_voice}")
    else:
        logging.error("Failed to generate doctor's voice response.")
        doctor_voice = None

    if not os.path.exists(doctor_voice):
        logging.error(f"Generated audio file not found: {doctor_voice}")
        doctor_voice = None

    # Log the final outputs
    logging.info(f"Final Outputs: Speech to Text: {speech_to_text_output}, Doctor's Response: {doctor_response}, Doctor's Voice: {doctor_voice}")

    return speech_to_text_output, doctor_response, doctor_voice


# Update the Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Patient's Voice"),
        gr.Image(type="filepath", label="Medical Image")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(type="filepath", label="Doctor's Voice")
    ],
    title="AI Doctor with Vision and Voice",
    description="Upload a medical image and speak into the microphone. The AI doctor will analyze the image and respond with a diagnosis and remedies."
)

iface.launch(debug=True)
