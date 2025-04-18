import logging
from ollama import chat, ChatResponse


class DeepSeekModel:
    """
    Wrapper for locally hosted DeepSeek-R1:8b via Ollama.

    Prerequisites:
      • Ollama installed & running (`ollama serve`)
      • Model pulled: `ollama pull deepseek-r1:8b`
      • ollama Python SDK installed: `pip install ollama`
    """

    def __init__(self, model_name: str = "deepseek-r1:8b"):
        self.model_name = model_name
        logging.info(
            f"DeepSeekModel initialized with model '{model_name}'.")  # Logging setup :contentReference[oaicite:4]{index=4}

    def generate_response(self, prompt: str, max_tokens: int = 512) -> str:
        """
        Send a chat completion request to Ollama and return the reply.

        :param prompt: Instruction or question for DeepSeek
        :param max_tokens: Maximum number of tokens to generate
        :return: Model-generated response text, or empty string on error
        """
        try:
            response: ChatResponse = chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            content = response.message.content
            logging.debug(f"DeepSeek response: {content}")  # Debug log of full response
            return content
        except Exception as e:
            logging.error(f"Error in DeepSeekModel.generate_response: {e}")
            return ""
