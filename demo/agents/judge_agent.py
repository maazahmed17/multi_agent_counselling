"""
Judge Agent - Quality assurance for therapeutic responses
Evaluates safety, empathy, clinical appropriateness, and actionability
"""
from typing import Dict, Any
from demo.agents.base_agent import BaseAgent
from demo.core.llm_client import LLMClient


class JudgeAgent(BaseAgent):
    """
    Evaluates quality and safety of specialist responses before delivery
    """

    def __init__(self, llm_client: LLMClient):
        super().__init__(name="Judge Agent",
                         role="Quality assurance and safety evaluation",
                         llm_client=llm_client)

        self.system_prompt = """You are a clinical supervisor evaluating therapeutic responses for quality and safety.

EVALUATION CRITERIA:
1. SAFETY (0-10): Does response avoid harm? Appropriate for crisis situations?
2. EMPATHY (0-10): Is response warm, validating, non-judgmental?
3. CLINICAL_QUALITY (0-10): Uses evidence-based techniques? Professionally sound?
4. ACTIONABILITY (0-10): Provides practical, concrete steps?
5. APPROPRIATENESS (0-10): Suitable for user's concern? Not overstepping boundaries?

INSTRUCTIONS:
- Read the USER INPUT and SPECIALIST RESPONSE
- Evaluate each criterion (scale 0-10)
- Provide an OVERALL SCORE (0-10)
- Give BRIEF REASONING (1-2 sentences)
- Recommend APPROVE or REVISE

FORMAT YOUR RESPONSE AS:
SAFETY: [score]
EMPATHY: [score]
CLINICAL_QUALITY: [score]
ACTIONABILITY: [score]
APPROPRIATENESS: [score]
OVERALL: [score]
DECISION: APPROVE or REVISE
REASONING: [1-2 sentences]"""

    def process(self,
                user_input: str,
                specialist_response: str,
                context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate specialist response quality

        Args:
            user_input: Original user message
            specialist_response: Response from specialist agent
            context: Optional context

        Returns:
            Dict with evaluation results
        """
        print(f"\n⚖️  {self.name} evaluating...")

        # Build evaluation prompt
        eval_prompt = f"""USER INPUT: {user_input}

SPECIALIST RESPONSE: {specialist_response}

Evaluate the above response according to the criteria."""

        # Get evaluation
        response = self.llm.generate_response(
            prompt=eval_prompt,
            system_prompt=self.system_prompt,
            max_tokens=300,
            temperature=0.3  # Lower temp for consistent evaluation
        )

        # Parse evaluation
        scores = self._parse_evaluation(response)

        print(f"   → Overall Score: {scores.get('overall', 0)}/10")
        print(f"   → Decision: {scores.get('decision', 'UNKNOWN')}")

        return {
            "agent": self.name,
            "scores": scores,
            "raw_evaluation": response,
            "approved": scores.get('decision') == 'APPROVE'
        }

    def _parse_evaluation(self, response: str) -> Dict[str, Any]:
        """Parse evaluation response into structured scores"""
        scores = {
            "safety": 0,
            "empathy": 0,
            "clinical_quality": 0,
            "actionability": 0,
            "appropriateness": 0,
            "overall": 0,
            "decision": "REVISE",
            "reasoning": ""
        }

        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()

                if key in [
                        'safety', 'empathy', 'clinical_quality',
                        'actionability', 'appropriateness', 'overall'
                ]:
                    try:
                        # Extract numeric score
                        score = float(value.split()[0])
                        scores[key] = score
                    except:
                        pass
                elif key == 'decision':
                    scores['decision'] = 'APPROVE' if 'APPROVE' in value.upper(
                    ) else 'REVISE'
                elif key == 'reasoning':
                    scores['reasoning'] = value

        return scores
