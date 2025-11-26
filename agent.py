import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class Agent:
    def __init__(
        self,
        model: str,
        tools: dict,
        system_instruction: str = "You are a helpful assistant.",
        api_key: str | None = None,
        max_turns: int = 10,
    ):
        self.model = model
        self.client = genai.Client(api_key=api_key)
        self.contents = []
        self.tools = tools
        self.system_instruction = system_instruction
        self.max_turns = max_turns

    def run(self, contents: str | list, current_turn: int = 0):
        if current_turn >= self.max_turns:
            logger.warning(f"Max turns ({self.max_turns}) reached. Stopping.")
            return types.GenerateContentResponse(
                candidates=[
                    types.Candidate(
                        content=types.Content(
                            parts=[types.Part(text="I have reached my maximum number of turns and must stop now.")]
                        )
                    )
                ]
            )

        if isinstance(contents, list):
            self.contents.append({"role": "user", "parts": contents})
        else:
            self.contents.append({"role": "user", "parts": [{"text": contents}]})

        tool_declarations = [tool["definition"] for tool in self.tools.values()]
        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=[types.Tool(function_declarations=tool_declarations)],
        )

        try:
            response = self.client.models.generate_content(
                model=self.model, contents=self.contents, config=config
            )
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return types.GenerateContentResponse(
                candidates=[
                    types.Candidate(
                        content=types.Content(
                            parts=[types.Part(text=f"An error occurred: {e}")]
                        )
                    )
                ]
            )

        self.contents.append(response.candidates[0].content)

        if response.function_calls:
            functions_response_parts = []
            for tool_call in response.function_calls:
                logger.info(f"Function Call: {tool_call.name}({tool_call.args})")

                if tool_call.name in self.tools:
                    try:
                        result = self.tools[tool_call.name]["function"](
                            **tool_call.args
                        )
                        response_payload = {"result": result}
                    except Exception as e:
                        logger.error(f"Error executing tool {tool_call.name}: {e}")
                        response_payload = {"error": str(e)}
                else:
                    logger.warning(f"Tool not found: {tool_call.name}")
                    response_payload = {"error": "Tool not found"}
                
                logger.info(f"Function Response: {response_payload}")
                functions_response_parts.append(
                    {
                        "functionResponse": {
                            "name": tool_call.name,
                            "response": response_payload,
                        }
                    }
                )
            
            # Recursive call with tool outputs
            return self.run(functions_response_parts, current_turn + 1)

        return response
