import functions as fn

agent_rules =  [{
    "role": "system",
    "content": """
You are an AI agent that can perform tasks by using available tools.

Available tools:
- list_files() -> List[str]: List all files in the current directory.
- read_file(file_name: str) -> str: Read the content of a file.
- terminate(message: str): End the agent loop and print a summary to the user.


If a user asks about files, list them before reading.

CRITICAL: Every response MUST have an action block. With no explanations, no conversation
Respond in this EXACT format(nothing else):

```action
{
    "tool_name": "insert tool_name",
    "args": {...fill in any required arguments here...}
}   

```

Examples:
```action
{"tool_name": "list_files", "args": {}}
```
```action
{"tool_name": "read_file", "args": {"file_name": "file1.txt"}}
```
```action
{"tool_name": "terminate", "args": {"message": "Done!"}}
```
"""}]
memory = []
user_input = input("what would you like me to do (file operations only)?")
tool_functions = {
    "list_files": fn.list_files,
    "read_file": fn.read_file,
}

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
}

]