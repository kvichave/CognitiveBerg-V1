import edge_tts
from groq import Groq
import json
import asyncio
from chat_CRUD import add_data

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

                self.gorq_LLM(prompt=self.prompt)
        except Exception as e:
            print("error in Whisper:::",e)
            return "reset"


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

    def text_to_speech(self, text, output_file, voice):
        """Synchronously converts text to speech using edge-tts and saves the audio as an MP3 file."""
        communicate = edge_tts.Communicate(text, voice)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(communicate.save(output_file))
        loop.close()

    outputPaths = []

    def speakers(self, json_data):
        self.outputPaths = []  # Initialize/clear the output paths
        print("In Speaker")
        voice_map = {
            0: "en-US-BrianNeural",
            1: "en-IN-NeerjaExpressiveNeural",
            2: "en-US-ChristopherNeural",
        }
        for interviewer in json_data:
            if interviewer.get("message") is None:
                text = interviewer['question']
            else:
                text = interviewer['message']
            output_file = f"AUDIOS/{interviewer['id']}.mp3"
            self.outputPaths.append(output_file)  # Append to the output list
            voice = voice_map.get(interviewer['id'], 'en-US-BrianNeural')
            self.text_to_speech(text, output_file, voice)

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
            "message": "Hello, I'm Michael Johnson, the Sustainability & Impact Advocate. I'll evaluate your startup’s environmental and social impact.",
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
Ensure that the LLM emulates realistic, natural investor interactions during the pitch, providing short validation during pauses and thoughtful questions after the pitch concludes.'''



    history=[
    {
      "role": "model",
      "parts": [
        "{\n  \"data\": [\n    {\n      \"investor_name\": \"Rajesh Sharma, Technology Specialist\",\n      \"message\": \"Hello, I'm Rajesh Sharma, the Technology Specialist for this panel.  I'll be focusing on the technical feasibility, scalability, and innovation of your AI/ML solution.\",\n      \"id\": 0\n    },\n    {\n      \"investor_name\": \"Emily Patel, Finance Expert\",\n      \"message\": \"Hi, I'm Emily Patel, the Finance Expert. My focus will be on your revenue model, cost structure, and overall financial projections for this deepfake detection technology.\",\n      \"id\": 1\n    },\n    {\n      \"investor_name\": \"David Lee, Marketing & Sales Strategist\",\n      \"message\": \"Hello, I'm David Lee, the Marketing & Sales Strategist. I'll be evaluating your go-to-market strategy, target audience, and competitive analysis within the deepfake detection market.\",\n      \"id\": 2\n    },\n    {\n      \"investor_name\": \"Sophia Gupta, Operations Specialist\",\n      \"message\": \"Hi, I'm Sophia Gupta, the Operations Specialist.  I'll be assessing the operational scalability, team capabilities, and overall execution plan for your solution.\",\n      \"id\": 3\n    },\n    {\n      \"investor_name\": \"Michael Johnson, Sustainability & Impact Advocate\",\n      \"message\": \"Hello, I'm Michael Johnson, the Sustainability & Impact Advocate. My focus will be on the ethical considerations and societal impact of your deepfake detection technology.\",\n      \"id\": 4\n    }\n  ]\n}",
      ],
    },
   
  ]
    LLM_reply=""

    def upload_to_gemini(path, mime_type=None):
        """Uploads the given file to Gemini.

        See https://ai.google.dev/gemini-api/docs/prompting_with_media
        """
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=gemini_prompt,
    )

    # TODO Make these files available on the local file system
    # You may need to update the file paths
    # files = [
    #   upload_to_gemini("Screenshot from 2025-01-12 21-16-54.png", mime_type="image/png"),
    # ]

    chat_session = model.start_chat(
    history=history
    )




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

            if add_to_history:
                self.history.append({"role": "user", "content": reply})
            self.gemini_LLM(reply,image)

    def gemini_LLM(self, reply,image, add_to_history=True):
        print("in LLM")
        # Synchronous API call to the LLM
        if image:
            file1 = PIL.Image.open("received_img/screenshot1.jpg")
            file2 = PIL.Image.open("received_img/screenshot2.jpg")

            response = self.chat_session.send_message([file1,file2, reply])
        
        else:
            response = self.chat_session.send_message(reply)

        # reply = reply.replace("'", '"')
        # reply = reply.replace('\\"', "'")


        print(response.text)
        # if reply[0] != "[":
        #     reply = "[" + str(completion.choices[0].message.content) + "]"

        reply = json.loads(response.text)
        if reply.get("FLAG") == "END":
            # add_data(self.his[1:],usetype=str(self.userDetails['scenario']))
            self.LLM_reply=reply.get("FLAG")

            print("reply", reply)
            return "END"
        else:
            reply=reply["data"]
            if add_to_history:
                self.history.append({"role": "assistant", "content": str(reply)})
            self.LLM_reply=reply
            
            print("reply", reply)
            self.speakers(reply)

    def text_to_speech(self, text, output_file, voice):
        """Synchronously converts text to speech using edge-tts and saves the audio as an MP3 file."""
        communicate = edge_tts.Communicate(text, voice)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(communicate.save(output_file))
        loop.close()

    outputPaths = []

    def speakers(self, json_data):
        self.outputPaths = []  # Initialize/clear the output paths
        print("In Speaker")
        voice_map = {
            0: "en-US-BrianNeural",
            1: "en-IN-NeerjaExpressiveNeural",
            2: "en-US-ChristopherNeural",
            3: "en-US-EricNeural",
            4: "en-US-AriaNeural"
        }
        for investor in json_data:
            if investor.get("message") is None:
                text = investor['question']
            else:
                text = investor['message']
            output_file = f"AUDIOS/{investor['id']}.mp3"
            self.outputPaths.append(output_file)  # Append to the output list
            voice = voice_map.get(investor['id'], 'en-US-BrianNeural')
            self.text_to_speech(text, output_file, voice)

        print("Generated audio files:", self.outputPaths)  # Ensure this shows the populated list
        return self.outputPaths  # Return the populated list





