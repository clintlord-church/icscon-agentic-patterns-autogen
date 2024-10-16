from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import lang_chain_models

class ClintsCoolAgent:
    def __init__(self, model, system_message, format: str=''):
        self.chain = None
        self.model = model
        self.system_message = system_message
        self.input_tokens = 0
        self.output_tokens = 0
        self.format = format

    def get_token_count(self):
        return {"input_tokens": self.input_tokens, "output_tokens": self.output_tokens, "total_tokens": self.input_tokens + self.output_tokens}
    
    def _get_chain(self):
        if self.chain is None:
            self.chain = lang_chain_models.get_chain(self.model, False, format=self.format)
        return self.chain

    def respond(self, human_message):
        chain = self._get_chain()
        response: AIMessage = chain.invoke([
            SystemMessage(content=self.system_message),
            HumanMessage(content=human_message)
        ])

        # extract the token count from the response
        self.input_tokens += response.usage_metadata.get("input_tokens", 0)
        self.output_tokens += response.usage_metadata.get("output_tokens", 0)

        return response.content