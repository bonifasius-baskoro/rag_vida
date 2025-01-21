from dotenv import load_dotenv
load_dotenv() 
import os
from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
def groq_completion(prompt,system_prompt):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),)
    chat_completion = client.chat.completions.create(
        messages=[
         {
            "role": "system",
            "content": system_prompt,
        },   
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.3-70b-versatile",
    temperature= 0.2,
        )
    return chat_completion.choices[0].message.content