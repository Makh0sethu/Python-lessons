
import json
import os
import google.genai as genai  #switch from google.generativeai which is now out of support
from google.colab import userdata
api_key = userdata.get('GOOGLE_API_KEY')
genai.interactions.DynamicAgentConfig(api_key=api_key)
os.environ['GOOGLE_API_KEY'] = api_key
#print("Google Generative AI SDK configured.")
from litellm import completion #, _turn_on_debug
from typing import List, Dict
#incase you face issues or want to see whats happening on lite, turn on the debug, but dont forget to disable it. Default: False
#_request_debug=True
#_turn_on_debug

def generate_response(messages: List[Dict]) -> str:

    response = completion(

        model="gemini/gemini-2.5-flash",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

#function to extract code block from response

def extract_code_block(response: str) -> str:
    """Extract code block from response"""
    if not '```' in response:
        return response

    code_block = response.split('```')[1].strip()
    if code_block.startswith("python"):
        code_block = code_block[6:]

    return code_block
def develop_custom_function():
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''prompt 1'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    initial_messages = input("Hi im Khodi, what python function can i help you with?").strip()

    messages = [
    {"role": "system", "content": "You are an expert software engineer that writes basic python functions."}
    ]
    messages.append({
    "role": "user",
    "content": f"Write a Python function that {initial_messages}. Output the function in a ```python code block```."
}
)
    print("generating function...\n")
    initial_response = generate_response(messages)

    initial_response = extract_code_block(initial_response)
    print("===initial response===\n")
    print (initial_response)


    #store response in llm memory/assistant
    messages.append({
    "role": "assistant", 
    "content": "\`\`\`python\n\n"+initial_response+"\n\n\`\`\`"
})

    ''''''''''''''''''''''''''''''''''''''''''''''''''''prompt 2'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    #old code before seeing solution in notes
    refine_messages = [
    {"role": "system", "content": "You are a python expert that writes basic python functions, and writes clean files, without unnecesssary values."},
    {"role": "user", "content": "add comprehensive documentation including Function description ,Parameter descriptions ,Return value description"},
    {"role": "assistant", "content": initial_response}
]
    print("refining function with documentation...\n")
    refined_response = generate_response(refine_messages)


    messages.append({
    "role": "user",
    "content": "add comprehensive documentation including Function description ,Parameter descriptions .Return value"
                 "return value, examples, and edge cases. Output the function in a ```python code block```."
})

    print("refining function with documentation...\n")
    refined_response = generate_response(messages)
    refined_response = extract_code_block(refined_response)
    print("===refined response===\n")
    print (refined_response)
    #store response in llm memory/assistant
    messages.append({
    "role": "assistant", 
    "content": "\`\`\`python\n\n"+refined_response+"\n\n\`\`\`"
})
    '''''''''''''''''''''''''''''''''''''''''''''''''''''prompt 3'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    '''
    final_messages = [
        {"role": "system", "content": "You are a python tester, adding minimal but huge cover unittests to the end of a given python file "},
        {"role": "user", "content": "optimize the code for performance and readability, include testcases using unnittest module at the end of the code, covering edge cases, error handling and typical usage scenarios."},
        {"role": "assistant", "content": refined_response}
    ]
    print("optimizing function and adding testcases...\n")
    final_response = generate_response(final_messages)
    '''
    messages.append({
      "role": "user",
      "content": "Add unittest test cases for this function, including tests for basic functionality, "
                 "edge cases, error cases, and various input scenarios. Output the code in a \`\`\`python code block\`\`\` with python: '(function_name)'."
   })

    final_response = generate_response(messages)
    final_response = extract_code_block(final_response)
    print("===final response===\n")
    print (final_response)

    file_path = "_".join(refined_response.split()[:3]) + ".py"
    with open(file_path, "w") as f:
        #there might be an issue on the output whether its just tests or code and tests
        f.write(refined_response +"\n\n"+ final_response)

    print(f"Function generation complete. Check {file_path} for the result.")

if __name__ == "__main__":


    function_code, tests, filename = develop_custom_function()
    print(f"\nFinal code has been saved to {filename}")