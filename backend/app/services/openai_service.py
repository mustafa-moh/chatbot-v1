from app.services.abstract.ai_service import AIService
from openai import AzureOpenAI
from config import Config


class OpenAIService(AIService):
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version="2024-08-01-preview",
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
        )

    def get_response(self, context, tools=None, tool_choice=None):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=context,
            tools=tools,
            tool_choice=tool_choice
        )
        return response.choices[0].message
