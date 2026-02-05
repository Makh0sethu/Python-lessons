from typing import List,Dict
import json
import os

#files contain all the business logic for each tool and handle operations the agent can perfom
  
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
    
def terminate(message: str) -> None:
    """Terminate the agent loop with a message."""
    print(message)