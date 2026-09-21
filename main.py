import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY environment variable is not set. Please set it in your .env file.")

def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
