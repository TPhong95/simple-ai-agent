import os
import argparse
import json
import sys

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function_info import available_functions
from functions.call_function import call_function

def main():

    #The model we want to use
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("No API key found!")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    #The program uses this argument parser to take one argument as a string and uses it in the program 
    parser = argparse.ArgumentParser(description="Simple helper agent")
    parser.add_argument("user_prompt", type=str, help="One string of user prompt")
    
    #Toggle additional info when using argument --verbose
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    #A list of messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    
    for i in range(20):
        #The prompt
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            
        )
        if not response.usage:
            raise RuntimeError("API response malformed!")
        
        #Append old message so it "remembers"
        message = response.choices[0].message
        messages.append(message)
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if not result_message["content"]:
                    raise RuntimeError("No content")
                    
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            print("Final response:")
            print(message.content)
            return message.content
        
        #Response we get as print in terminal
        #If verbose arg is true print additional info
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        
        if i == 20:
            print("Max iteration reached exiting program!")
            sys.exit(1)
    

if __name__ == "__main__":
    main()
