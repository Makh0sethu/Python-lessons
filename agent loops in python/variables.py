import json
import functions as fn
import os 
#importing litellm and setting up keys, Openai,anthropic, google. i use google
#!pip install litellm
#!pip install google-genai

import google.genai as genai  #switch from google.generativeai which is now out of support
# NOTE :need to set up keys on vs code. this only works on google colab
from google.colab import userdata
api_key = userdata.get('GOOGLE_API_KEY')
genai.interactions.DynamicAgentConfig(api_key=api_key)
os.environ['GOOGLE_API_KEY'] = api_key
#print("Google Generative AI SDK configured.")

from litellm import completion #, _request_debug from typing




#available tools for the agent to use, you can add more tools here and make sure to implement them in functions.py


# @ list of all functions available to the agent
function_registry= {
    "list_files": fn.list_files,
    "read_file": fn.read_file,
    "terminate": fn.terminate
}

# @ name(in function registry), description(what it does), Parameters(Json Schema spcifying expected input)
tools =[

{
    "type": "function",
    "function":{
        "name": "list_files",
        "description": "List all files in the current directory.",
        "parameters": {
            "type": "object",
            "properties": {}, "required": []}
    }
},
{
    "type": "function",
    "function":{
        "name": "read_file",
        "description": "Read the content of a file in the specified directory.",
        "parameters": {
            "type": "object",
            "properties": {"file_name": {"type": "string",
                    "required": ["file_name"]
                }
            },
        
        }
    }
}, 
{
    "type": "function",
    "function":{
        "name": "terminate",
        "description": "Terminates the conversation. No further actions or iterations.",
        "parameters": {
            "type": "object",
            "properties": {"message": {"type": "string",
                    "required": ["message"]
                }
            },
        
        }
    }
}

]


# agent rules and memory, you can modify the rules to change the agent's behavior. The memory will be updated with the conversation history and results of actions.

agent_rules = [{
    "role": "system",
    "content": """
You are an AI agent that can perform tasks by using available tools. 

If a user asks about files, documents, or content, first list the files before reading them.

WHen you are done, terminate the conversation using the "terminate" tool and i will provide the results to the user.
"""
}]

#conversation

user_input = input("what would you like me to do (file operations only)?")

memory =["role: user, content: " + user_input]

messages = agent_rules + memory

#api call
response = completion(

        model="gemini/gemini-2.5-flash",
        messages=messages,
        #tools tell the model what functions it can call and how to call them, the model will then respond with a tool call that we can execute in python
        tools=tools,
        max_tokens=1024
    )

#process the structured response from the model, extract the tool call and arguments, execute the tool and get the result. This is where the agent's reasoning happens as it decides which tool to use based on the user's input and the conversation history.
tool=  response.choices[0].message.tool_calls[0]
tool_name = tool.function.name
#this unpacks the JSON object into key woord argumenst
tool_args = json.loads(tool.function.arguments)

action= {"tool_name": tool_name, "args": tool_args}

#execute the function
result = function_registry[tool_name](**tool_args)

print (f"Tool: {tool_name}, Args: {tool_args}")
print (f"Result: {result}")