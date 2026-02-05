
#importing litellm and setting up keys, Openai,anthropic, google. i use google

#!pip install litellm
import google.genai as genai  #switch from google.generativeai which is now out of support
from google.colab import userdata
api_key = userdata.get('GOOGLE_API_KEY')
genai.interactions.DynamicAgentConfig(api_key=api_key)
os.environ['GOOGLE_API_KEY'] = api_key
#print("Google Generative AI SDK configured.")

from litellm import completion #, _request_debug from typing
from typing import List,Dict
import json
import os


def generate_response(messages: List[Dict]) -> str:

    response = completion(

        model="gemini/gemini-2.5-flash",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

def extract_markdown_block(response: str, block_type: str) -> str:
    """Extract a specific markdown block from response"""
    block_start=f'```{block_type}'
    block_end='```'
    if block_start not in response:
        response = f"```{block_type}` not found in response."
        return response
    
    try :
        parts = response.split(block_start)
        if len(parts) < 2:
            return None
        
        end_parts = parts[1].split(block_end)
        if len(end_parts) < 2:

            code_block = parts[1].strip()
            print ("Warning: Closing ``` not found. Extracting until end of response.")
            return code_block
        return end_parts[0].strip()
    except Exception as e:
        print(f"Error extracting markdown block: {str(e)}")
        return None

def parse_action(response: str) -> Dict:
    """Parse the LLM response into a structured action dictionary and retry if the new blok is invalid.. By breaking down the LLM’s output into tool_name and args, the agent can precisely determine the next action and its inputs."""
    try:
        extracted = extract_markdown_block(response, "action")
        if extracted is None:
            return {"tool_name": "error", "args": {"message": "`action` block not found in response."}} 
        
        response_json = json.loads(extracted)
        
        if "tool_name" not in response_json:
            return {"tool_name": "error", "args": {"message": "Missing 'tool_name' in action JSON."}}
        
        if "args" not in response_json:
            return {"tool_name": "error", "args": {"message": "Missing 'args' in action JSON."}}
        
    
        return response_json
    
    except json.decoder.JSONDecodeError as e:
            return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}}
    except Exception as e:
            return {"tool_name": "error", "args": {"message": str(e)}}

#create random files for testing
create_file_prompt =[
    {"role": "user", "content": "generate a 5 line political commentery on the state of Zimbabwe"},
    {"role": "system", "content": "You are a commedian who takes inspiration from Dave Chapel, you double what someone asks you, add the file name as a random news headline with 3 "}
]

create_file= generate_response(create_file_prompt)
with open("test.txt", "w") as file:
    file.write(create_file)

def list_files() -> List[str]:
    try :
        return [f for f in os.listdir() if os.path.isfile(f)]
    except Exception as e:
        return [f"Error listing files: {str(e)}"]


def read_file(file_name: str) -> str:
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except Exception as e:
        return f"Error reading {file_name}: {str(e)}"