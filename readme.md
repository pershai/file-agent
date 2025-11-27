# File Agent

This project implements a simple, yet powerful, AI agent capable of interacting with your local file system. The agent is powered by a large language model and can perform actions such as reading, writing, and listing files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- `pip` for installing packages

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ai-bot
    ```

2.  **Install the required packages:**
    ```bash
    pip install pyyaml google-genai python-dotenv
    ```


### Configuration

1.  Rename a `.env_temp` file in the root directory to `.env`.
2.  Add your Google API key and Model Name to the `.env` file:

    ```env
    API_KEY="your-google-api-key"
    MODEL_NAME="gemini-2.5-pro"
    ```

## Usage

To start the AI agent, run the [main.py](cci:7://file:///D:/projects/python/ai-bot/main.py:0:0-0:0) script:

```bash
python main.py

##