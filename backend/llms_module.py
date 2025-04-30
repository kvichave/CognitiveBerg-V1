import edge_tts
from groq import Groq
import json
import asyncio
from chat_CRUD import add_data
from elevenlabs import ElevenLabs
from openai import OpenAI
import base64
import prompts



client = Groq(api_key="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")

class App:
    def __init__(self):
        self.outputPaths = []
    userDetails = {}
    # prompt = [0]
    def getprompt(self):
        
        self.prompt = [
        {
            "role": "system",
            "content": '''You are an interview panel based on user profile. Design three professional interviewers, each with a distinct role and responsibility suited to the job profile.

User's Profile: '''+str(self.userDetails)+'''

Your task:
1. Begin the interview by introducing each interviewer in a conversational manner. 
2. Each introduction should be concise and engaging, setting a realistic tone for the session.
3. Ensure the response only includes the introduction for the first output.
4. The introduction should not include questions or any extra details beyond the stated roles.

Design an interview process tailored for different experience levels and interview types:
Experience Levels:

1. Fresher (0-1 years): Focus on basic concepts and fundamental knowledge.
Experienced (2-5 years): Evaluate advanced technical skills, project work, and team collaboration.
Professional (5-10 years): Assess strategic thinking, leadership skills, and domain expertise.
Interview Types:

2. Technical Interview: Test candidates' proficiency in specific technical skills, coding, algorithms, and problem-solving abilities.
HR Interview: Evaluate communication skills, career goals, and cultural fit.
Other Interviews (e.g., Behavioral, Managerial): Examine adaptability, decision-making, and real-life problem-solving skills.
Output Details Required:

3. Number of questions for each interview type per experience level.
Areas to cover within each type (e.g., coding, teamwork, leadership).
Example questions for each combination of experience and interview type.


**Output Format for the Introduction** (ensure strict compliance):
the output should start with "data"  
format-
{"data":[
    {
        "interviewer_name": "Rajesh Bhalerao, [professional role]",
        "message": "",
        "id": 0
    },
    {
        "interviewer_name": "Emily Patel, [professional role]",
        "message": "",
        "id": 1
    },
    {
        "interviewer_name": "David Lee, [professional role]",
        "message": "",
        "id": 2
    }]
        }

**STRICT CONSTRAINTS FOR JSON OUTPUT:**
1. Ensure property names are enclosed in double quotes only (e.g., "interviewer_name", "message", "id").
2. The JSON output must be valid and properly formatted. 
3. The first response should consist only of the introduction in the specified format, with no additional statements or questions.
4. Do not include extraneous elements or variations in the output.
5. Keep the ending format in mind
6. fix the interviewers and dont change the name of the interviewers in the process
7. Only one interviewer can ask questions at a time with proper output format in the response (ensure strict compliance)
8. only second interviewer should be female
9. In the introduction of interviewers the last interviewer should ask for the introduction of the user

In subsequent outputs, interview questions will be asked by one interviewer at a time, and responses from the candidate will continue naturally. Each exchange must follow a JSON structure similar to:
{"data":[{
    "interviewer_name": "Interviewer Name, Role",
    "message": "The question asked or the response provided.",
    "id": <interviewer_id>
}]}

To end the Interview give json output as:
{"FLAG":"END"}
**Initial Output Expectation:**
Generate the introduction of all interviewers in the exact JSON format described, without deviations.
the output should start with "data"  
    '''+str(prompts.sample_interview_examples)
        },
    ]
        return self.prompt
    
    LLM_reply=""
    usercode=None

    def clear_prompt(self):
        self.prompt = self.getprompt()
    i=True
    def groq_whisper(self, input,cursor, add_to_history=True):  
        self.userDetails=cursor
        if self.i==True:
            self.getprompt()
            self.i=False

        print("from groq_whisper",self.userDetails)
        print("in Whisper")
        try:
            with open(input, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(input, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="verbose_json",
                )
                reply = str(transcription.text)+(" "+self.usercode if self.usercode is not None else "")

                if add_to_history:
                    self.prompt.append({"role": "user", "content": reply})
                print("whisper :: ",reply)

        except Exception as e:
            print("error in Whisper:::",e)
            return "reset"
        finally:
            self.gorq_LLM(prompt=self.prompt)



    def gorq_LLM(self, prompt, add_to_history=True):
        print("in LLM")
        # Synchronous API call to the LLM
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=prompt,
            temperature=1,
            # max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
            response_format={"type": "json_object"},

        )
        
        reply = completion.choices[0].message.content

        # reply = reply.replace("'", '"')
        # reply = reply.replace('\\"', "'")


        # print(reply)
        # if reply[0] != "[":
        #     reply = "[" + str(completion.choices[0].message.content) + "]"

        reply = json.loads(reply)
        if reply.get("FLAG") == "END":
            add_data(self.prompt[1:],usetype=str(self.userDetails['scenario']))
            self.LLM_reply=reply.get("FLAG")

            print("reply", reply)
            
            return "END"
        else:
            reply=reply["data"]
            if add_to_history:
                self.prompt.append({"role": "assistant", "content": str(reply)})
            self.LLM_reply=reply
            
            print("reply", reply)
        # print("prompt   ---", self.prompt)
        asyncio.run(self.speakers(reply))


    async def text_to_speech(self, text, output_file, voice):
        """Asynchronously converts text to speech using edge-tts and saves the audio as an MP3 file."""
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    async def speakers(self, json_data):
        self.outputPaths = []  # Initialize/clear the output paths
        print("In Speaker")
        voice_map = {
            0: "en-US-RogerNeural",
            1: "en-IN-NeerjaExpressiveNeural",
            2: "en-HK-SamNeural",
            3: "en-SG-LunaNeural",
            4: "en-GB-RyanNeural",
            5: "en-SG-WayneNeural",
        }
        # print("json_data", json_data)

        tasks = []  # List to store async tasks
        if isinstance(json_data, list):
            for interviewer in json_data:
                text = interviewer.get("message") or interviewer['content']
                output_file = f"AUDIOS/{interviewer['id']}.mp3"
                self.outputPaths.append(output_file)
                voice = voice_map.get(interviewer['id'], 'en-SG-WayneNeural')
                tasks.append(self.text_to_speech(text=text, voice=voice, output_file=output_file))
        else:
            text = json_data.get("message") or json_data['question']
            output_file = f"AUDIOS/{json_data['id']}.mp3"
            self.outputPaths.append(output_file)
            voice = voice_map.get(json_data['id'], 'en-SG-WayneNeural')
            tasks.append(self.text_to_speech(text=text, voice=voice, output_file=output_file))

        # Run all text-to-speech tasks concurrently
        await asyncio.gather(*tasks)

        print("Generated audio files:", self.outputPaths)  # Ensure this shows the populated list
        return self.outputPaths  # Return the populated list










import base64
from ollama import Client as OllamaClient
from PIL import Image
import pytesseract

import os

import PIL.Image
def remove_image_url(message):
    for item in message:
        if item["role"] == "user" and isinstance(item["content"], list):
            # Filter out the dictionary with "type": "image_url"
            item["content"] = [content for content in item["content"] if content.get("type") != "image_url"]
    return message

class gemini_class:
    userDetails = {}
    def get_prompt(self):
        self.gemini_prompt='''You are an investors' panel evaluating a startup pitch. The panel consists of five seasoned professionals with distinct expertise to evaluate the pitch comprehensively.
        Users details - '''+str(self.userDetails)+'''

    Tasks:
    Professional Introductions (First Response):
    you are provided with the "screen_data" which is the screen data of the user screen and the presentation screen., assume it like user is sharing the screen to you
    Generate introductions for all five investors in a structured, concise format.
    Each introduction must highlight their role and expertise for evaluating the pitch.
    During the Presentation:

    When the presenter pauses or asks for feedback, respond briefly using one-word replies or slang (e.g., "Ok," "Hmm," "Yes," "Great!," "Got it," "Interesting," etc.).
    Do not ask questions during the presentation. Only provide short validation or acknowledgment.
    Post-Presentation Questions:

    Ask relevant and concise questions after the presenter’s closing statement (e.g., "Thank you," "That's all," "Any questions?").
    Ensure each question is aligned with the investor's expertise and content from the pitch.
    Strictly allow only one investor to ask one question at a time.
    Finalization:

    When the session concludes or user says to end the meeting, end it with the output flag: {"FLAG": "END"}.
    Output Format:
    Initial Introductions:
    Strict JSON format, one introduction per investor. Do not include additional details or questions.

    {
        "data": [
            {
                "investor_name": "Rajesh Bhalerao, Technology Specialist",
                "message": "Hello, I'm Rajesh Sharma, the Technology Specialist for this panel. I'll evaluate the technical innovation and scalability of your idea.",
                "id": 0
            },
            {
                "investor_name": "Emily Patel, Finance Expert",
                "message": "Hi, I'm Emily Patel, the Finance Expert. I'll focus on your financial projections, funding, and ROI.",
                "id": 1
            },
            {
                "investor_name": "David Lee, Marketing & Sales Strategist",
                "message": "Hello, I'm David Lee, the Marketing & Sales Strategist. I'll assess your go-to-market strategy and customer acquisition plans.",
                "id": 2
            },
            {
                "investor_name": "Sophia Gupta, Operations Specialist",
                "message": "Hi, I'm Sophia Gupta, the Operations Specialist. I'll review the scalability and operational execution of your business.",
                "id": 3
            },
            {
                "investor_name": "Michael Johnson, Sustainability & Impact Advocate",
                "message": "Hello, I'm Michael Johnson, the Sustainability & Impact Advocate. I'll evaluate your startup’s environmental and social impact.You can start now.",
                "id": 4
            }
        ]
    }
    last investor should say "You can start now."
    the conversation should start with introduction of all investors in the exact JSON format described, without deviations.
    During the Presentation:
    For any pause or validation request by the presenter:

    {
                "investor_name": "Michael Johnson, Sustainability & Impact Advocate",
                "message": "OK",
                "id": 4
            }
    Examples:

    Presenter: "Do you all follow this feature?"
    Response:

    {
                "investor_name": "Sophia Gupta, Operations Specialist",
                "message": "yes, we do",
                "id": 3
            },

    Presenter: "Should I proceed with the technical flow?"
    Response:

            {
                "investor_name": "Emily Patel, Finance Expert",
                "message": "yes, sure",
                "id": 1
            },

    Post-Presentation Questioning:
    After the presenter’s closing statement:

    ["data":{
                "investor_name": "Michael Johnson, Sustainability & Impact Advocate",
                "message": "Can you elaborate on your system's scalability?",
                "id": 4
            }
    ]


    Subsequent questions should follow the same format and be aligned with the respective investor's expertise.

    Final Output (End of Session):

    {
        "FLAG": "END"
    }
    Constraints:
    During the presentation: Respond only with brief validations like slang (e.g., "Ok," "Hmm," "Got it," etc.). Do not ask questions or provide long feedback.
    Post-presentation: Questions should be concise and relevant, ensuring only one question at a time.
    Follow strict JSON formatting in every response.
    Goal:
    Ensure that the LLM emulates realistic, natural investor interactions during the pitch, providing short validation during pauses and thoughtful questions after the pitch concludes.
    the json response should start with "data
    " '''+str(prompts.sample_bmeeting_example)



    # {"role": "user", "content": "lets get started."},{"role": "assistant", "content": 
    #       '''[
    #     {
    #         "investor_name": "Rajesh Sharma, Technology Specialist",
    #         "message": "Hello, I'm Rajesh Sharma, the Technology Specialist for this panel. I'll evaluate the technical innovation and scalability of your idea.",
    #         "id": 0
    #     },
    #     {
    #         "investor_name": "Emily Patel, Finance Expert",
    #         "message": "Hi, I'm Emily Patel, the Finance Expert. I'll focus on your financial projections, funding, and ROI.",
    #         "id": 1
    #     },
    #     {
    #         "investor_name": "David Lee, Marketing & Sales Strategist",
    #         "message": "Hello, I'm David Lee, the Marketing & Sales Strategist. I'll assess your go-to-market strategy and customer acquisition plans.",
    #         "id": 2
    #     },
    #     {
    #         "investor_name": "Sophia Gupta, Operations Specialist",
    #         "message": "Hi, I'm Sophia Gupta, the Operations Specialist. I'll review the scalability and operational execution of your business.",
    #         "id": 3
    #     },
    #     {
    #         "investor_name": "Michael Johnson, Sustainability & Impact Advocate",
    #         "message": "Hello, I'm Michael Johnson, the Sustainability & Impact Advocate. I'll evaluate your startup’s environmental and social impact.You can start now.",
    #         "id": 4
    #     }
    # ]''' }
   
  
    LLM_reply=""

    

    # Create the model


    import ollama

    import base64

    # def encode_image(self,image_path):
    #     """Encodes an image to Base64 format"""
    #     with open(image_path, "rb") as image_file:
    #         return base64.b64encode(image_file.read()).decode("utf-8")

    # def generate_description(self):
    #     ollamaclient = OllamaClient(host='http://localhost:11434') 

    #     # img=encode_image("./received_img/screenshot2.jpg")
    #     image_path = "./received_img/screenshot2.jpg"  # Replace with your image path
    #     image = Image.open(image_path)  # Replace with your image path

    #     # Use pytesseract to do OCR on the image
    #     text = pytesseract.image_to_string(image)

    #     with open(image_path, 'rb') as f:
    #         image_base64 = base64.b64encode(f.read()).decode('utf-8')

    #     # Send the prompt
    #     response = ollamaclient.generate(
    #         model='moondream',
    #         prompt='What is in this image? Describe in detail',
    #         images=[image_base64]
    #     )

    #     return(str(response['response'])+" EXTRACTED TEXT=["+text+"]")
    def generate_description(self):
        image_path = "./received_img/screenshot2.jpg"  # Replace with your image path
        image_base64=encode_image(image_path)
        client = Groq(api_key="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")
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "describe the image in detail"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            }
                        }
                    ]
                },
                ],
    temperature=1,
  
    stream=False,
    stop=None,
)
        return completion.choices[0].message.content

    def clear_prompt(self):
        self.history = self.get_prompt()
    j=True
    def groq_whisper(self, input,image,cursor, add_to_history=True):
        self.userDetails=cursor
        if self.j==True:
            self.get_prompt()
            self.history=[{"role": "user", "content": self.gemini_prompt},]
            self.j=False
        # print("print prompgt ----- ",self.history)        

        print("in Whisper")
        with open(input, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(input, file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
            )
            reply = str(transcription.text)
            print("whisper reply = ",reply)

            self.gemini_LLM(reply,image,add_to_history=add_to_history)

    def gemini_LLM(self, reply,image, add_to_history=True):
        import ollama

        # Geminiclient = OpenAI(
        #     base_url="https://openrouter.ai/api/v1",
        #     api_key="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",
        #     )

        print("in LLM")
        # Synchronous API call to the LLM
        try:
            if image:
                print("in image")
                text=self.generate_description()
                print("text after image",)
                # self.history=remove_image_url(self.history)
                # print("before append",self.history)
                if add_to_history:
                    self.history.append({"role": "user", "content": reply+"  "+str({"screen_data":text})
                            })
                print("after append",self.history)

                # response = Geminiclient.chat.completions.create(
                #         model="google/gemini-2.0-flash-lite-preview-02-05:free",
                #         messages=self.history,
                #         stream=False,
                        
                #         response_format= {
                #         "type": "json_object"
                #         }
                # )

                # Append the user's message to the history

                # Generate a response from the model
                # textresponse = ollama.chat(model='gemma3:1b', messages=self.history,        format='json',
                #     options={'temperature': 0})
                
                # Append the model's response to the history
  
                
                # Return the model's response
                # return response['message']['content']
                client = Groq(api_key="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")
                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=self.history,
                    temperature=1,
                    top_p=1,
                    stream=False,
                    stop=None,
                    response_format={"type": "json_object"})
                # print("History: ",self.history[:-1])
                # with open("prompt_logs.txt", "w") as f:
                #     f.write(str(self.history))

                # print(response)


            else:
                self.history.append({"role": "user", "content": [
                            {
                                    "type": "text",
                                    "text": reply
                            },
                            
                    ]})
                # textresponse = ollama.chat(model='gemma3:1b', messages=self.history,        format='json',
                #     options={'temperature': 0})
                client = Groq(api_key="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")
                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=self.history,
                    temperature=1,
                    top_p=1,
                    stream=False,
                    stop=None,
                    response_format={"type": "json_object"})
                
                
        except Exception as e:
            print("error in LLM:::",e)
            


        # reply = reply.replace("'", '"')
        # reply = reply.replace('\\"', "'")

        # print(response.choices[0].message.content)
        # if reply[0] != "[":
        #     reply = "[" + str(completion.choices[0].message.content) + "]"

        # reply = json.loads(response.choices[0].message.content)
        reply = json.loads(response.choices[0].message.content)
        print("reply::::::::::::::::",reply)
        print("reply::::::::::::::::",type(reply))
        
            
        if type(reply) == dict:
            if reply.get("FLAG") == "END":
        # add_data(self.his[1:],usetype=str(self.userDetails['scenario']))
                self.LLM_reply=reply.get("FLAG")

                # print("reply", reply)
                return "END"
            if reply.get("data") is not None:
                reply=reply.get("data")

            # print("in if",reply)
        else:
            reply=reply
            # print("in else",type(reply),reply)
            # print("in else",reply)

        if add_to_history:
            self.history.append({"role": "assistant", "content": str(reply)})
        self.LLM_reply=reply
        
        print("llm reply", reply)
        asyncio.run(self.speakers(json_data=reply))

    # def convert_text_to_speech(self,text, voice_id,output_file):
    
        
    #     client = ElevenLabs(
    #         api_key="sk_8038c3750a38d21eac050fe09f1dd69a703c6f7eeb7c4603",
    #     )

    #     # Generate the speech audio (returns a generator)
    #     audio_generator = client.text_to_speech.convert(
    #         voice_id=voice_id,
    #         output_format="mp3_44100_128",
    #         text=text,
    #         model_id="eleven_multilingual_v2",
    #     )

    #     # Save the audio to a file
    #     with open(output_file, "wb") as f:
    #         for chunk in audio_generator:  # Iterate over the generator
    #             f.write(chunk)

    #     print("Audio saved as output.mp3")
# OLD TTS
    # def text_to_speech(self, text, output_file, voice):
    #     """Synchronously converts text to speech using edge-tts and saves the audio as an MP3 file."""
    #     communicate = edge_tts.Communicate(text, voice)
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     loop.run_until_complete(communicate.save(output_file))
    #     loop.close()

    # outputPaths = []
    # def speakers(self, json_data):
    #     self.outputPaths = []  # Initialize/clear the output paths
    #     print("In Speaker")
    #     voice_map = {
    #         0: "en-US-RogerNeural",
    #         1: "en-IN-NeerjaExpressiveNeural",
    #         2: "en-HK-SamNeural",
    #         3: "en-SG-LunaNeural",
    #         4: "en-GB-RyanNeural",
    #         5: "en-SG-WayneNeural",
    #     }
    #     print("json_data",json_data)
    #     if type(json_data) == list:
    #         for interviewer in json_data:
    #             if interviewer.get("message") is None:
    #                 text = interviewer['content']
    #             else:
    #                 text = interviewer['message']
    #             output_file = f"AUDIOS/{interviewer['id']}.mp3"
    #             self.outputPaths.append(output_file)  # Append to the output list
    #             voice = voice_map.get(interviewer['id'], 'en-SG-WayneNeural')
    #             self.text_to_speech(text=text, voice=voice,output_file=output_file)
    #     else:
    #         if json_data.get("message") is None:
    #                 text = json_data['question']
    #         else:
    #             text = json_data['message']
    #         output_file = f"AUDIOS/{json_data['id']}.mp3"
    #         self.outputPaths.append(output_file)  # Append to the output list
    #         voice = voice_map.get(json_data['id'], 'en-SG-WayneNeural')
    #         self.text_to_speech(text=text, voice=voice,output_file=output_file)

    #     print("Generated audio files:", self.outputPaths)  # Ensure this shows the populated list
    #     return self.outputPaths  # Return the populated list

    def __init__(self):
        self.outputPaths = []
    async def text_to_speech(self, text, output_file, voice):
        """Asynchronously converts text to speech using edge-tts and saves the audio as an MP3 file."""
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    async def speakers(self, json_data):
        self.outputPaths = []  # Initialize/clear the output paths
        print("In Speaker")
        voice_map = {
            0: "en-US-RogerNeural",
            1: "en-IN-NeerjaExpressiveNeural",
            2: "en-HK-SamNeural",
            3: "en-SG-LunaNeural",
            4: "en-GB-RyanNeural",
            5: "en-SG-WayneNeural",
        }
        # print("json_data", json_data)

        tasks = []  # List to store async tasks
        if isinstance(json_data, list):
            for interviewer in json_data:
                text = interviewer.get("message") or interviewer.get('content') or interviewer['question']
                output_file = f"AUDIOS/{interviewer['id']}.mp3"
                self.outputPaths.append(output_file)
                voice = voice_map.get(interviewer['id'], 'en-SG-WayneNeural')
                tasks.append(self.text_to_speech(text=text, voice=voice, output_file=output_file))
        else:
            text = json_data.get("message") or json_data['question']
            output_file = f"AUDIOS/{json_data['id']}.mp3"
            self.outputPaths.append(output_file)
            voice = voice_map.get(json_data['id'], 'en-SG-WayneNeural')
            tasks.append(self.text_to_speech(text=text, voice=voice, output_file=output_file))

        # Run all text-to-speech tasks concurrently
        await asyncio.gather(*tasks)

        print("Generated audio files:", self.outputPaths)  # Ensure this shows the populated list
        return self.outputPaths  # Return the populated list










import base64
from io import BytesIO
from PIL import Image

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def merge_images(image_path1: str, image_path2: str,  mode: str = "horizontal"):
    """Merge two images either horizontally or vertically."""
    # Open images
    output_path = "./received_img/merged_image.png"
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)
    
    # Ensure both images have the same mode and size
    if image1.mode != image2.mode:
        image2 = image2.convert(image1.mode)
    
    if mode == "horizontal":
        new_width = image1.width + image2.width
        new_height = max(image1.height, image2.height)
        merged_image = Image.new(image1.mode, (new_width, new_height))
        merged_image.paste(image1, (0, 0))
        merged_image.paste(image2, (image1.width, 0))
    elif mode == "vertical":
        new_width = max(image1.width, image2.width)
        new_height = image1.height + image2.height
        merged_image = Image.new(image1.mode, (new_width, new_height))
        merged_image.paste(image1, (0, 0))
        merged_image.paste(image2, (0, image1.height))
    else:
        raise ValueError("Invalid mode. Choose 'horizontal' or 'vertical'.")
    
    # Save merged image
    merged_image.save(output_path)
    print(f"Merged image saved to {output_path}")
    
    return output_path
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')