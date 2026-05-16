"""
llm_config.py – OpenAI (ChatGPT) configuration.
API key is loaded from the .env file: OPENAI_API_KEY
Optionally set OPENAI_MODEL in .env to override the model (default: gpt-4o-mini)
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # loads variables from .env


def get_llm(temperature: float = 0):
    """Returns a LangChain ChatOpenAI instance using settings from .env."""
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key or api_key.startswith("sk-your-"):
        raise ValueError(
            "OpenAI API key not set!\n"
            "Open the .env file and replace the placeholder:\n"
            "  OPENAI_API_KEY=sk-..."
        )
    return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)
