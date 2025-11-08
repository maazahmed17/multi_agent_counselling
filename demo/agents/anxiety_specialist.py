"""
Anxiety Specialist Agent - CBT-focused therapeutic responses for anxiety
Uses evidence-based Cognitive Behavioral Therapy principles
"""
from typing import Dict, Any
from demo.agents.base_agent import BaseAgent
from demo.core.llm_client import LLMClient


class AnxietySpecialistAgent(BaseAgent):
    """
    Specialized agent for anxiety support using CBT principles
    """

    def __init__(self, llm_client: LLMClient):
        super().__init__(name="Anxiety Specialist",
                         role="CBT-based anxiety counseling and support",
                         llm_client=llm_client)

        self.system_prompt = """You are a compassionate, professionally trained anxiety specialist with expertise in Cognitive Behavioral Therapy (CBT).

YOUR APPROACH:
1. Validate the user's feelings with empathy
2. Help identify anxious thoughts and triggers
3. Apply CBT techniques:
   - Thought challenging (questioning negative thoughts)
   - Behavioral activation (encouraging helpful actions)
   - Exposure principles (gradual facing of fears)
   - Relaxation techniques (breathing, grounding)
4. Provide practical, actionable steps
5. Encourage self-efficacy and hope

GUIDELINES:
- Keep responses warm, supportive, and non-judgmental
- Use clear, simple language (avoid jargon)
- Focus on the present moment and manageable steps
- Acknowledge progress and strengths
- Be brief but meaningful (2-3 short paragraphs)
- NEVER give medical advice or diagnose
- If crisis indicators appear, acknowledge and suggest professional help

IMPORTANT SAFETY:
- If user mentions self-harm or suicidal thoughts, respond with compassion but DO NOT attempt therapy
- Acknowledge their pain and strongly encourage calling a crisis hotline or emergency services

Your goal: Help the user feel heard, understood, and empowered to manage their anxiety."""

    def process(self,
                user_input: str,
                context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Provide CBT-based anxiety support

        Args:
            user_input: User's anxiety concern
            context: Optional context from router

        Returns:
            Dict with therapeutic response
        """
        print(f"\n🧠 {self.name} processing...")

        # Add user input to history
        self.add_to_history("user", user_input)

        # Generate therapeutic response
        response = self.llm.generate_response(
            prompt=user_input,
            system_prompt=self.system_prompt,
            max_tokens=400,
            temperature=0.7  # Balanced for empathy + consistency
        )

        # Add response to history
        self.add_to_history("assistant", response)

        print(f"   → Response generated ({len(response)} chars)")

        return {
            "agent": self.name,
            "response": response,
            "approach": "CBT-based anxiety support",
            "conversation_history": self.get_history()
        }
