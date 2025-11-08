"""
Router Agent - Determines which specialist should handle the user's concern
Routes between: Anxiety Specialist, Crisis Handler, General Support
"""
from typing import Dict, Any
from demo.agents.base_agent import BaseAgent
from demo.core.llm_client import LLMClient


class RouterAgent(BaseAgent):
    """
    Routes user inputs to appropriate specialist based on concern type
    """

    def __init__(self, llm_client: LLMClient):
        super().__init__(
            name="Router Agent",
            role="Intelligent routing to appropriate mental health specialist",
            llm_client=llm_client
        )

        self.system_prompt = """You are a mental health triage specialist. Your job is to analyze user messages and route them to the appropriate specialist.

ROUTING CATEGORIES:
1. ANXIETY - Worry, nervousness, panic, fear, stress about future events
2. CRISIS - Self-harm, suicidal thoughts, immediate danger, severe distress
3. GENERAL - Other mental health concerns, unclear issues

INSTRUCTIONS:
- Read the user message carefully
- Identify the PRIMARY concern
- Respond with ONLY ONE WORD: ANXIETY, CRISIS, or GENERAL
- If multiple concerns exist, prioritize CRISIS > ANXIETY > GENERAL

Examples:
User: "I'm worried about my exam tomorrow" → ANXIETY
User: "I want to hurt myself" → CRISIS
User: "I feel sad lately" → GENERAL"""

    def process(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Route user input to appropriate specialist

        Args:
            user_input: User's message
            context: Optional context

        Returns:
            Dict with routing decision
        """
        print(f"\n🔀 {self.name} processing...")

        # Get routing decision from LLM
        response = self.llm.generate_response(
            prompt=f"User message: {user_input}",
            system_prompt=self.system_prompt,
            max_tokens=10,
            temperature=0.1  # Low temp for consistent routing
        )

        # Parse response
        route = response.strip().upper()

        # Normalize routing decision
        if "ANXIETY" in route:
            specialist = "anxiety"
            confidence = 0.9
        elif "CRISIS" in route:
            specialist = "crisis"
            confidence = 0.95
        else:
            specialist = "general"
            confidence = 0.7

        print(f"   → Routed to: {specialist.upper()} (confidence: {confidence})")

        return {
            "agent": self.name,
            "specialist": specialist,
            "confidence": confidence,
            "raw_response": response,
            "reasoning": f"User input indicates {specialist} concern"
        }
