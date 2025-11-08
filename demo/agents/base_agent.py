"""
Base Agent - Parent class for all specialized agents
Provides common functionality like logging, safety checks, etc.
"""
from typing import Dict, Any, Optional, List
from demo.core.llm_client import LLMClient


class BaseAgent:
    """
    Base class for all agents in the multi-agent counseling system
    """

    def __init__(self, name: str, role: str, llm_client: LLMClient):
        """
        Initialize base agent

        Args:
            name: Agent name (e.g., "Anxiety Specialist")
            role: Agent role/description
            llm_client: Shared LLM client instance
        """
        self.name = name
        self.role = role
        self.llm = llm_client
        self.conversation_history: List[Dict[str, str]] = []

        print(f"✅ {self.name} initialized")

    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def process(self,
                user_input: str,
                context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user input - to be implemented by child classes

        Args:
            user_input: User's message
            context: Optional context from previous agents

        Returns:
            Dict with agent's response and metadata
        """
        raise NotImplementedError("Child agents must implement process()")
