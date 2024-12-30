
import edge_tts
import asyncio

async def text_to_speech(text, output_file, voice):
    """Converts text to speech using edge-tts and saves the audio as an MP3 file."""
    
    # Initialize the TTS service with the provided voice
    communicate = edge_tts.Communicate(text, voice)
    
    # Convert the text to speech and save it to the output file
    await communicate.save(output_file)




async def speakers(json_data):
    reply_list=[]
    for interviewer in json_data:

        text=interviewer['message']
        id=interviewer['id']
        if id==0:
            output_file="AUDIOS/0.mp3"
            await text_to_speech(text, output_file,voice="en-US-BrianNeural")
            reply_list.append(output_file)
            

        if id==1:
            output_file="AUDIOS/1.mp3"
            await text_to_speech(text, output_file,voice="en-IN-NeerjaExpressiveNeural")
            reply_list.append(output_file)

        if id==2:
            output_file="AUDIOS/2.mp3"
            await text_to_speech(text, output_file,voice="en-US-ChristopherNeural")
            reply_list.append(output_file)
    return reply_list