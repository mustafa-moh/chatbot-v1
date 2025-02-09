from app.services.abstract.ai_service import AIService
from app.services.abstract.search_service import SearchService
from flask import current_app
import json


class AssistantService:
    def __init__(self, ai_service: AIService, search_service: SearchService):
        self.ai_service = ai_service
        self.search_service = search_service

    def get_response(self, context) -> str:
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_internet",
                    "description": "Use this function when you don't know the answer. It searches the internet for relevant information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query",
                            }
                        },
                        "required": ["query"],
                    },
                }
            }
        ]

        response_message = self.ai_service.get_response(
            context=context,
            tools=tools,
            tool_choice="auto",
        )

        context.append({
            "role": "assistant",
            "content": response_message.content or "",
            "tool_calls": json.loads(response_message.model_dump_json(indent=2))['tool_calls']
        })

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "search_internet":
                    function_response = self.search_internet(query=function_args.get("query"))
                else:
                    function_response = json.dumps({"error": "Unknown function"})

                context.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

                final_response = self.ai_service.get_response(context=context)
                return final_response.content
        else:
            return response_message.content

    def search_internet(self, query):
        return self.search_service.search(query)
