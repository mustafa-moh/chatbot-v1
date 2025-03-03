from app.services.abstract.ai_service import AIService
from app.services.openai_service import OpenAIService


class AIFactory:
    @staticmethod
    def create_ai_service(service_name: str) -> AIService:
        if service_name == "openai":
            return OpenAIService()
        raise ValueError(f"Unsupported AI service: {service_name}")
