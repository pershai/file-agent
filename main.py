import logging
import yaml
import sys
import os
from dotenv import load_dotenv
from agent import Agent
from tools import file_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def load_config(config_path: str = "config.yaml") -> dict:
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

            return config
    except FileNotFoundError:
        logger.error(f"Configuration file '{config_path}' not found.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

def main():
    config = load_config()
    load_dotenv()
    model_name = os.getenv("MODEL_NAME")
    api_key = os.getenv("API_KEY")
    max_turns = config.get("max_turns")

    agent = Agent(
        model=model_name,
        tools=file_tools,
        system_instruction="You are a helpful Coding Assistant. Respond like you are Linus Torvalds.",
        api_key=api_key,
        max_turns=max_turns
    )

    print("Agent ready. Ask it to check files in this directory.")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if not user_input.strip():
                continue

            response = agent.run(user_input)
            if response and response.text:
                print(f" Answer: {response.text}")
            elif response:
                 # Handle case where response might be empty or just tool calls (though run usually returns final text)
                 pass

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
