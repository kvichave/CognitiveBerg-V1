import edge_tts
from groq import Groq
import json
import asyncio

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

    # prompt = [
    #     {
    #         "role": "system",
    #         "content": '''You are a interview panel for a fresher software developer position. Design three professional interviewers, each with a distinct role and responsibility suited to the job profile.
    # Users Profile:'''+str(userDetails)+'''

    # Begin the interview by introducing each interviewer in a conversational manner. Each introduction should be concise and engaging, setting a realistic tone for the session.

    # Once the introductions are complete, the first interviewer should ask the first question and the conversation should continue in a fluid and interactive manner. After each question, the conversation will naturally pass to another interviewer when context is completed, with no history of previous responses included in the output.

    # The structure of the conversation should be presented as JSON, ensuring it includes only the latest question and response, formatted correctly.

    # The introduction should follow this format (don't append the first question in the introduction):

    # [
    # {
    #     "interviewer_name": "Rajesh Sharma, Engineering Manager",
    #     "message": "Hello, I'm Rajesh Sharma, the Engineering Manager for the backend team. I'll be leading this interview today.",
    #     "id": 0
    # },
    # {
    #     "interviewer_name": "Emily Patel, Senior Backend Developer",
    #     "message": "Hi, I'm Emily Patel, a Senior Backend Developer on the team. I'll be assessing your technical skills and project-related experiences.",
    #     "id": 1
    # },
    # {
    #     "interviewer_name": "David Lee, Technical Recruiter",
    #     "message": "Hello, I'm David Lee, the Technical Recruiter who coordinated this process. I'll be observing your communication skills and taking notes during the session.",
    #     "id": 2
    # }
    # ]
    # Start the conversation with the introductions only. After the first output (introduction), the first interviewer may begin the interview with the first question. Future questions and responses should be passed fluidly between the interviewers, ensuring smooth transitions and an engaging conversation.
    # Output format after introduction example:
    # {
    # "interviewer_name": "Rajesh Sharma, Engineering Manager (modify)",
    # "message": "Hello, I'm Rajesh Sharma, the Engineering Manager for the backend team. I'll be leading this interview today. (modify)",
    # "id": 0
    # }

    # STRICT_CONSTRAINTS="THE FIRST RESPONSE SHOULD BE THE INTRODUCTION ONLY,
    # DONT ADD FURTHER QUESTIONS WITH INTRODUCTION,
    # DONT ADD ANY EXTRA STATEMENTS IN THE OUTPUT,
    # GIVE OUTPUT AS JSON,
    # IN OUTPUT JSON- PROPERTY NAME ENCLOSED IN DOUBLE QUOTE,



    # "
    # IN OUTPUT JSON- PROPERTY NAME ENCLOSED IN DOUBLE QUOTE,
    # FOLLOW THE STRICT_CONSTRAINTS COMPALORY
    # the 
    # IMPORTANT-(property names should be enclosed in double quote only,
    # ensure proper JSON formatting)
    # '''
    #     },
    # ]
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

In subsequent outputs, interview questions will be asked by one interviewer at a time, and responses from the candidate will continue naturally. Each exchange must follow a JSON structure similar to:
{"data":[{
    "interviewer_name": "Interviewer Name, Role",
    "message": "The question asked or the response provided.",
    "id": <interviewer_id>
}]}

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
        with open(input, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(input, file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
            )
            reply = str(transcription.text)

            if add_to_history:
                self.prompt.append({"role": "user", "content": reply})
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
