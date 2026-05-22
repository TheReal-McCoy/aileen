import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api key not found in .env")


def main():
    parser = argparse.ArgumentParser(description="aileen")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    client = genai.Client(api_key=api_key)
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages, 
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0),
        )
        if response.usage_metadata == None:
            raise RuntimeError("no response from gemini api")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        function_responses = []
        if response.function_calls != None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception("there should be a response")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("there should be a response here")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("no result..")
                function_responses.append(function_call_result.parts[0])
                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
            return
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))
    print("model has not produced final response after 20 iterations")

if __name__ == "__main__":
    main()
