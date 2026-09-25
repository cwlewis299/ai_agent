import os, sys
import argparse
import json
from prompts import system_prompt
from dotenv import load_dotenv
from openai import OpenAI
from call_function import *


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set. Please set it in your .env file.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    parser = argparse.ArgumentParser(description="Generate a response from the OpenRouter API based on a user prompt.")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        if not response.usage:
            raise RuntimeError("Response does not contain usage information. Please check your API key and model availability.")
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                #function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, verbose=args.verbose)
                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(message.content)
            break
    if not message.content:
        sys.exit("Unable to complete request within 20 iterations")


if __name__ == "__main__":
    main()
