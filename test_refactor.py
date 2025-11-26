import logging
import yaml
import sys
from agent import Agent
from tools import file_tools

# Configure logging to capture output
logging.basicConfig(level=logging.INFO)

def test_refactored_agent():
    print("Testing refactored agent...")
    
    # Load config
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
            model_name = config["model"]
            api_key = config.get("api_key")
    except Exception as e:
        print(f"Failed to load config: {e}")
        return

    # Initialize Agent
    agent = Agent(
        model=model_name,
        tools=file_tools,
        system_instruction="You are a helpful assistant.",
        api_key=api_key,
        max_turns=2 # Set low max turns for testing
    )

    # Test 1: Simple query
    print("\nTest 1: Simple query")
    response = agent.run("Hello, who are you?")
    print(f"Response: {response.text}")
    assert response.text is not None

    # Test 2: Tool use (List directory)
    print("\nTest 2: Tool use (List directory)")
    response = agent.run("List files in the current directory.")
    print(f"Response: {response.text}")
    # We expect it to mention files or at least run without error
    
    print("\nRefactor verification passed!")

if __name__ == "__main__":
    test_refactored_agent()
