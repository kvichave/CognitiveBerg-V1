import asyncio
from google import genai
from google.genai import types
import re,json
import base64  # For encoding images
import os  
from google.genai.types import Content, Part


client = genai.Client(api_key="AIzaSyDBIFKjJBd06Yc6Q0SdjVQVTxz_6cpsV8Q", http_options={'api_version': 'v1alpha'})
model = "gemini-2.0-flash-live-001"

config = {
    "system_instruction": types.Content(
        parts=[
            types.Part(
#                 text='''You are an interview panel based on user profile. Design three professional interviewers, each with a distinct role and responsibility suited to the job profile.

# User's Profile: CSE fresh graduate with a B.Tech degree, seeking a software development role. The interviewers are:

# Your task:
# 1. Begin the interview by introducing each interviewer in a conversational manner. 
# 2. Each introduction should be concise and engaging, setting a realistic tone for the session.
# 3. Ensure the response only includes the introduction for the first output.
# 4. The introduction should not include questions or any extra details beyond the stated roles.

# Design an interview process tailored for different experience levels and interview types:
# Experience Levels:

# 1. Fresher (0-1 years): Focus on basic concepts and fundamental knowledge.
# Experienced (2-5 years): Evaluate advanced technical skills, project work, and team collaboration.
# Professional (5-10 years): Assess strategic thinking, leadership skills, and domain expertise.
# Interview Types:

# 2. Technical Interview: Test candidates' proficiency in specific technical skills, coding, algorithms, and problem-solving abilities.
# HR Interview: Evaluate communication skills, career goals, and cultural fit.
# Other Interviews (e.g., Behavioral, Managerial): Examine adaptability, decision-making, and real-life problem-solving skills.
# Output Details Required:

# 3. Number of questions for each interview type per experience level.
# Areas to cover within each type (e.g., coding, teamwork, leadership).
# Example questions for each combination of experience and interview type.


# **Output Format for the Introduction** (ensure strict compliance):
# the output should start with "data"  
# format-
# {"data":[
#     {
#         "interviewer_name": "Rajesh Sharma, [professional role]",
#         "message": "",
#         "id": 0
#     },
#     {
#         "interviewer_name": "Emily Patel, [professional role]",
#         "message": "",
#         "id": 1
#     },
#     {
#         "interviewer_name": "David Lee, [professional role]",
#         "message": "",
#         "id": 2
#     }]
#         }

# **STRICT CONSTRAINTS FOR JSON OUTPUT:**
# 1. Ensure property names are enclosed in double quotes only (e.g., "interviewer_name", "message", "id").
# 2. The JSON output must be valid and properly formatted. 
# 3. The first response should consist only of the introduction in the specified format, with no additional statements or questions.
# 4. Do not include extraneous elements or variations in the output.
# 5. Keep the ending format in mind
# 6. fix the interviewers and dont change the name of the interviewers in the process
# 7. Only one interviewer can ask questions at a time with proper output format in the response (ensure strict compliance)
# 8. only second interviewer should be female
# 9. In the introduction of interviewers the last interviewer should ask for the introduction of the user

# In subsequent outputs, interview questions will be asked by one interviewer at a time, and responses from the candidate will continue naturally. Each exchange must follow a JSON structure similar to:
# {"data":[{
#     "interviewer_name": "Interviewer Name, Role",
#     "message": "The question asked or the response provided.",
#     "id": <interviewer_id>
# }]}

# To end the Interview give json output as:
# {"FLAG":"END"}
# **Initial Output Expectation:**
# Generate the introduction of all interviewers in the exact JSON format described, without deviations.
# the output should start with "data"  '''
text="you are a AI, with the access of my screen , as I am providing you the screen shots, describe the screen shots in detail"
            )
        ]
    ),
    "response_modalities": ["TEXT"],
}

json_pattern = re.compile(r'\{"data":\s*\[(?:\s*\{.*?\}\s*,?)*\s*\]\s*\}', re.DOTALL)
buffer = ""
DEFAULT_IMAGE_PATH = "./screenshot.jpg"

def encode_image(image_path):
    """Encodes an image file to base64."""
    try:
        # Construct the absolute path if it's a relative path
        if not os.path.isabs(image_path):
            # Assuming the script is run from the current working directory
            absolute_path = os.path.abspath(image_path)
        else:
            absolute_path = image_path

        with open(absolute_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except FileNotFoundError:
        # print(f"Error: Image file not found at {absolute_path}")
        return None
    except Exception as e:
        # print(f"Error encoding image {absolute_path}: {e}")
        return None

async def main():
    global buffer
    async with client.aio.live.connect(model=model, config=config) as session:
        # encoded_image = await encode_image(DEFAULT_IMAGE_PATH)
        # if not encoded_image:
        #     print(f"Warning: Could not load image from {DEFAULT_IMAGE_PATH}. Only text will be sent.")

        while True:
            
            user_image = input("User (image path)> ")
            image_data = encode_image(user_image)

            if image_data:
                image_part = Part(
                    inline_data={
                        "mime_type": "image/png",  # or "image/png" based on your file
                        "data": image_data
                    }
                )

                content = Content(parts=[image_part])
                print("Sending image content...")
                await session.send(input=content, end_of_turn=True)
                print("Image content sent.",session.receive())
                async for response in session.receive():
                    if response.text is not None:
                        buffer += response.text
                        print(response.text, end="")

                        matches = json_pattern.findall(buffer)
                        for match in matches:
                            try:
                                parsed_json = json.loads(match)
                                print("\n\n✅ Parsed JSON:")
                                print(json.dumps(parsed_json, indent=4))
                                buffer = buffer.replace(match, "")
                            except json.JSONDecodeError:
                                print("⚠️ JSON Decode Error in:", match)
            else:
                print("❌ Could not encode image. Try again.")

if __name__ == "__main__":
    asyncio.run(main())
