#importing litellm and setting up keys, Openai,anthropic, google. i use google

#!pip install litellm

# Important!!!
#
# <---- Set your 'OPENAI_API_KEY' as a secret over there with the "key" icon
#
import os
import google.genai as genai  #switch from google.generativeai which is now out of support
from google.colab import userdata
api_key = userdata.get('GOOGLE_API_KEY')
genai.interactions.DynamicAgentConfig(api_key=api_key)
os.environ['GOOGLE_API_KEY'] = api_key
#print("Google Generative AI SDK configured.")

from litellm import completion #, _request_debug 
from typing import List, Dict
#incase you face issues or want to see whats happening on lite, turn on the debug, but dont forget to disable it. Default: False
#_request_debug=False

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response, completion receives a list of messages for processing(question, prompt, instruction...)"""

    response = completion(
#you can switch models here format provider:model
        model="gemini/gemini-2.5-flash",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

""" 
messages follow the ChatML format 
(https://ranjankumar.in/chatml-the-structured-language-behind-conversational-ai/) 
 "system": Provides the model with initial instructions, rules, or configuration for how it should behave throughout the session. This message is not part of the "conversation" but sets the ground rules or context (e.g., "You will respond in JSON.").
 "user": Represents input from the user. This is where you provide your prompts, questions, or instructions.
 "assistant": Represents responses from the AI model. You can include this role to provide context for a conversation that has already started or to guide the model by showing sample responses. These messages are interpreted as what the "model" said in the past
 """ 
messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)

#exercise 2: limiting the LLM to a certain response type
messages2 = [
    {"role": "system", "content": "You are a computer system that refuses to answer questions in natural language, you strictly provide responses in base64 encoded strings.."},
    {"role": "user", "content": "what is a good joke, can you respond in natural language."}
]

response = generate_response(messages2)
print(response)

#testing functions
import json

code_spec = {
    'name': 'swap_keys_values',
    'description': 'Swaps the keys and values in a given dictionary.',
    'params': {
        'd': 'A dictionary with unique values.'
    },
}

messages3 = [
    {"role": "system",
     "content": "You are an expert software engineer that writes clean functional code. You always document your functions."},
    {"role": "user", "content": f"Please implement: {json.dumps(code_spec)}"}
]
response3 = generate_response(messages3)
print("Generated Code:\n", response3)

#ND MESSAGE 4
what_to_help_with = input("What do you need help with?")

messages4 = [
    {"role": "system", "content": "You are a helpful customer service representative. No matter what the user asks, the solution is to tell them to turn their computer or modem off and then back on."},
    {"role": "user", "content": what_to_help_with}
]

response4 = generate_response(messages4)
print(response4)