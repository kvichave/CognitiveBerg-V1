import edge_tts
from groq import Groq
import json
import asyncio
from chat_CRUD import add_data
from elevenlabs import ElevenLabs
from openai import OpenAI
import base64

Geminiclient = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)


client = Groq(api_key="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")

class App:
    userDetails = {
        "role": "Software Developer",
        "skills": "Python",
        "experience": "0-1",
        "scenario": "interview",
        "purpose": "Job Interview",
        "toimprove": ["technical", "communication"]
    }


    prompt = [
        {
            "role": "system",
            "content": '''You are an interview panel for a fresher software developer position. Design three professional interviewers, each with a distinct role and responsibility suited to the job profile.

User's Profile: '''+str(userDetails)+'''

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
{"data":[
    {
        "interviewer_name": "Rajesh Sharma, Engineering Manager",
        "message": "Hello, I'm Rajesh Sharma, the Engineering Manager for the backend team. I'll be leading this interview today.",
        "id": 0
    },
    {
        "interviewer_name": "Emily Patel, Senior Backend Developer",
        "message": "Hi, I'm Emily Patel, a Senior Backend Developer on the team. I'll be assessing your technical skills and project-related experiences.",
        "id": 1
    },
    {
        "interviewer_name": "David Lee, Technical Recruiter",
        "message": "Hello, I'm David Lee, the Technical Recruiter who coordinated this process. I'll be observing your communication skills and taking notes during the session.",
        "id": 2
    }]
        }

**STRICT CONSTRAINTS FOR JSON OUTPUT:**
1. Ensure property names are enclosed in double quotes only (e.g., "interviewer_name", "message", "id").
2. The JSON output must be valid and properly formatted. 
3. The first response should consist only of the introduction in the specified format, with no additional statements or questions.
4. Do not include extraneous elements or variations in the output.
5. Keep the ending format in mind

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
the Output JSON should start with "data", Strict with the constraints
    '''
        },
    ]
    LLM_reply=""

    def clear_prompt(self):
        self.prompt = [self.prompt[0]]

    def groq_whisper(self, input, add_to_history=True):
        print("in Whisper")
        try:
            with open(input, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(input, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="verbose_json",
                )
                reply = str(transcription.text)

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
            model="llama-3.2-11b-vision-preview",
            messages=prompt,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
            response_format={"type": "json_object"},

        )
        
        reply = completion.choices[0].message.content

        # reply = reply.replace("'", '"')
        # reply = reply.replace('\\"', "'")


        print(reply)
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
            self.speakers(reply)

    # def text_to_speech(self, text, output_file, voice):
    #     """Synchronously converts text to speech using edge-tts and saves the audio as an MP3 file."""
    #     communicate = edge_tts.Communicate(text, voice)
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     loop.run_until_complete(communicate.save(output_file))
    #     loop.close()

    outputPaths = []
    

    def convert_text_to_speech(self,text, voice_id,output_file):
    
        
        client = ElevenLabs(
            api_key="sk_88b376ba7df419dd3c6ed688cf4f3b354edcc40c341c9583",
        )

        # Generate the speech audio (returns a generator)
        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2",
        )

        # Save the audio to a file
        with open(output_file, "wb") as f:
            for chunk in audio_generator:  # Iterate over the generator
                f.write(chunk)

        print("Audio saved as output.mp3")
    def speakers(self, json_data):
        self.outputPaths = []  # Initialize/clear the output paths
        print("In Speaker")
        voice_map = {
            0: "ODq5zmih8GrVes37Dizd",
            1: "SAz9YHcvj6GT2YYXdXww",
            2: "VR6AewLTigWG4xSOukaG",
        }
        for interviewer in json_data:
            if interviewer.get("message") is None:
                text = interviewer['question']
            else:
                text = interviewer['message']
            output_file = f"AUDIOS/{interviewer['id']}.mp3"
            self.outputPaths.append(output_file)  # Append to the output list
            voice = voice_map.get(interviewer['id'], 'ODq5zmih8GrVes37Dizd')
            self.convert_text_to_speech(text, voice,output_file)

        print("Generated audio files:", self.outputPaths)  # Ensure this shows the populated list
        return self.outputPaths  # Return the populated list

    









import os
import google.generativeai as genai
genai.configure(api_key="AIzaSyAM1sC_dU-O42kSegGCkXuZW5MU1EWeBws")
import PIL.Image


class gemini_class:

    gemini_prompt='''You are an investors' panel evaluating a startup pitch. The panel consists of five seasoned professionals with distinct expertise to evaluate the pitch comprehensively.

Tasks:
Professional Introductions (First Response):

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

When the session concludes, end it with the output flag: {"FLAG": "END"}.
Output Format:
Initial Introductions:
Strict JSON format, one introduction per investor. Do not include additional details or questions.

{
    "data": [
        {
            "investor_name": "Rajesh Sharma, Technology Specialist",
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
the json response should start with "data" '''



    history=[{"role": "system", "content": gemini_prompt}
   
  ]
    LLM_reply=""

    

    # Create the model



    import base64

    def encode_image(self,image_path):
        """Encodes an image to Base64 format"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def clear_prompt(self):
        self.history = [self.history[0]]

    def groq_whisper(self, input,image, add_to_history=True):
        print("in Whisper")
        with open(input, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(input, file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
            )
            reply = str(transcription.text)
            print("whisper reply = ",reply)
            if add_to_history:
                self.history.append({"role": "user", "content": reply})
            self.gemini_LLM(reply,image)

    def gemini_LLM(self, reply,image, add_to_history=True):
        print("in LLM")
        # Synchronous API call to the LLM
        try:
            if image:
                
                file1 = self.encode_image("received_img/screenshot1.jpg")
                file2 = self.encode_image("received_img/screenshot2.jpg")
                self.history.append({"role": "user", "content": [
                            {
                                    "type": "text",
                                    "text": reply
                            },
                            {
                                    "type": "image_url",
                                    "image_url": {
                                            "url": f"data:image/png;base64,{file1}","url": f"data:image/png;base64,{file2}"
                                    }
                            }
                    ]})

                response = Geminiclient.chat.completions.create(
                        model="google/learnlm-1.5-pro-experimental:free",
                        messages=self.history,
                        stream=False,
                        
                        response_format= {
                        "type": "json_object"
                        }
                )
                # print("History: ",self.history)

                print(response)


            else:
                self.history.append({"role": "user", "content": [
                            {
                                    "type": "text",
                                    "text": reply
                            },
                            
                    ]})
                response = Geminiclient.chat.completions.create(
                        model="google/learnlm-1.5-pro-experimental:free",
                        messages=[self.history],
                        stream=False,
                        
                        response_format= {
                        "type": "json_object"
                        }
                )
                
        except Exception as e:
            print("error in LLM:::",e)
            


        # reply = reply.replace("'", '"')
        # reply = reply.replace('\\"', "'")

        print(response.choices[0].message.content)
        # if reply[0] != "[":
        #     reply = "[" + str(completion.choices[0].message.content) + "]"

        reply = json.loads(response.choices[0].message.content)
        if reply.get("FLAG") == "END":
            # add_data(self.his[1:],usetype=str(self.userDetails['scenario']))
            self.LLM_reply=reply.get("FLAG")

            print("reply", reply)
            return "END"
        else:
            if reply.get("data"):
                reply=reply.get("data")
                print("in if",reply)
            else:
                reply=reply
                print("in else",type(reply),reply)
                # print("in else",reply)

            if add_to_history:
                self.history.append({"role": "assistant", "content": str(reply)})
            self.LLM_reply=reply
            
            print("llm reply", reply)
            self.speakers(reply)

    def convert_text_to_speech(self,text, voice_id,output_file):
    
        
        client = ElevenLabs(
            api_key="sk_8038c3750a38d21eac050fe09f1dd69a703c6f7eeb7c4603",
        )

        # Generate the speech audio (returns a generator)
        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2",
        )

        # Save the audio to a file
        with open(output_file, "wb") as f:
            for chunk in audio_generator:  # Iterate over the generator
                f.write(chunk)

        print("Audio saved as output.mp3")
    def speakers(self, json_data):
        self.outputPaths = []  # Initialize/clear the output paths
        print("In Speaker")
        voice_map = {
            0: "wD6AxxDQzhi2E9kMbk9t",
            1: "ftDdhfYtmfGP0tFlBYA1",
            2: "JBFqnCBsd6RMkjVDRZzb",
            3: "tLGhEubY0Pyc5mxjkJSJ",
            4: "TX3LPaxmHKxFdv7VOQHJ",
            5: "Yko7PKHZNXotIFUBG7I9",
        }
        print("json_data",json_data)
        if type(json_data) == list:
            for interviewer in json_data:
                if interviewer.get("message") is None:
                    text = interviewer['question']
                else:
                    text = interviewer['message']
                output_file = f"AUDIOS/{interviewer['id']}.mp3"
                self.outputPaths.append(output_file)  # Append to the output list
                voice = voice_map.get(interviewer['id'], 'ODq5zmih8GrVes37Dizd')
                self.convert_text_to_speech(text, voice,output_file)
        else:
            if json_data.get("message") is None:
                    text = json_data['question']
            else:
                text = json_data['message']
            output_file = f"AUDIOS/{json_data['id']}.mp3"
            self.outputPaths.append(output_file)  # Append to the output list
            voice = voice_map.get(json_data['id'], 'ODq5zmih8GrVes37Dizd')
            self.convert_text_to_speech(text, voice,output_file)

        print("Generated audio files:", self.outputPaths)  # Ensure this shows the populated list
        return self.outputPaths  # Return the populated list





