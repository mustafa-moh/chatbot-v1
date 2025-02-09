from abc import ABC, abstractmethod


class AIService(ABC):
    @abstractmethod
    def get_response(self, context, tools=None, tool_choice=None):
        pass
