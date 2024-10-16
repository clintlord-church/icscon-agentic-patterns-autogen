from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_fireworks import ChatFireworks
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from enum import Enum

class Model(Enum):
    GPT4o = "gpt-4o"
    GPT4oMini = "gpt-4o-mini"
    Claude35Sonnet = "claude-3-5-sonnet"
    Llama31_8b = "llama-31-8b"
    Llama31_70b = "llama-31-70b"
    Llama31_405b = "llama-31-405b"
    GeminiFlash = "gemini-flash"
    LocalLMStudio = "local-lm-studio"
    LocalOllama = "local-ollama"

def get_chain(model: Model, include_parser: bool, format: str=''):
    if model == Model.GPT4o:
        chat_model = ChatOpenAI(model="gpt-4o-2024-08-06")
    elif model == Model.GPT4oMini:
        chat_model = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
    elif model == Model.Claude35Sonnet:
        chat_model = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    elif model == Model.Llama31_405b:
        chat_model = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-405b-instruct")
    elif model == Model.Llama31_70b:
        chat_model = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-70b-instruct")
    elif model == Model.Llama31_8b:
        chat_model = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-8b-instruct")
    elif model == Model.GeminiFlash:
        chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    elif model == Model.LocalOllama:
        chat_model = ChatOllama(model="llama3.2:3b", format=format)
    elif model == Model.LocalLMStudio:
        chat_model = ChatOpenAI(
            model="", 
            base_url="http://localhost:1234/v1",
            api_key=""
        )

    if include_parser:
        parser = StrOutputParser()
        chain = chat_model | parser
    else:
        chain = chat_model
        
    return chain
