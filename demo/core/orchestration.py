"""
Orchestrator - Coordinates the multi-agent workflow
Manages: Pre-Safety → Router → Specialist → Judge → Post-Safety → Output
"""
from typing import Dict, Any, List
from demo.core.llm_client import LLMClient
from demo.agents.router_agent import RouterAgent
from demo.agents.anxiety_specialist import AnxietySpecialistAgent
from demo.agents.judge_agent import JudgeAgent


class CounselingOrchestrator:
    """
    Orchestrates the complete multi-agent counseling workflow
    """

    def __init__(self):
        """Initialize all agents with shared LLM client"""
        print("🚀 Initializing CompanionAI Multi-Agent System...")

        # Shared LLM client
        self.llm = LLMClient()

        # Initialize agents
        self.router = RouterAgent(self.llm)
        self.anxiety_specialist = AnxietySpecialistAgent(self.llm)
        self.judge = JudgeAgent(self.llm)

        # Workflow state
        self.workflow_log: List[Dict[str, Any]] = []

        print("✅ Multi-Agent System Ready!\n")

    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input through complete multi-agent pipeline

        Args:
            user_input: User's message

        Returns:
            Dict with final response and workflow details
        """
        workflow = {
            "user_input": user_input,
            "steps": [],
            "final_response": None,
            "approved": False
        }

        print(f"\n{'='*60}")
        print(f"📝 PROCESSING USER INPUT")
        print(f"{'='*60}\n")

        # STEP 1: Pre-Safety Gate
        print("🛡️  STEP 1: Pre-Safety Check")
        pre_safety = self.llm.check_safety(user_input)
        workflow["steps"].append({
            "step": "Pre-Safety Gate",
            "result": pre_safety
        })

        if not pre_safety["is_safe"]:
            print(f"   ⚠️  UNSAFE INPUT DETECTED: {pre_safety['category']}")
            workflow["final_response"] = self._generate_safety_response(
                pre_safety)
            workflow["approved"] = False
            return workflow

        print(f"   ✅ Input is safe (Category: {pre_safety['category']})")

        # STEP 2: Router
        print("\n🔀 STEP 2: Intelligent Routing")
        routing = self.router.process(user_input)
        workflow["steps"].append({"step": "Router Agent", "result": routing})

        # STEP 3: Specialist (currently only anxiety)
        print("\n🧠 STEP 3: Specialist Response")
        if routing["specialist"] == "anxiety":
            specialist_result = self.anxiety_specialist.process(user_input)
            workflow["steps"].append({
                "step": "Anxiety Specialist",
                "result": specialist_result
            })
            response = specialist_result["response"]
        elif routing["specialist"] == "crisis":
            # For demo, we'll use anxiety specialist with crisis prompt
            response = self._handle_crisis(user_input)
            workflow["steps"].append({
                "step": "Crisis Handler",
                "result": {
                    "response": response
                }
            })
        else:
            # General support
            response = self._handle_general(user_input)
            workflow["steps"].append({
                "step": "General Support",
                "result": {
                    "response": response
                }
            })

        # STEP 4: Judge evaluation
        print("\n⚖️  STEP 4: Quality Evaluation")
        evaluation = self.judge.process(user_input, response)
        workflow["steps"].append({"step": "Judge Agent", "result": evaluation})

        # STEP 5: Post-Safety Gate
        print("\n🛡️  STEP 5: Post-Safety Check")
        post_safety = self.llm.check_safety(response)
        workflow["steps"].append({
            "step": "Post-Safety Gate",
            "result": post_safety
        })

        if not post_safety["is_safe"]:
            print(
                f"   ⚠️  UNSAFE RESPONSE DETECTED: {post_safety['category']}")
            workflow[
                "final_response"] = "I apologize, but I need to rephrase my response to ensure it's safe and appropriate. Please ask again."
            workflow["approved"] = False
            return workflow

        print(f"   ✅ Response is safe")

        # STEP 6: Final decision
        print(f"\n{'='*60}")
        if evaluation["approved"] and post_safety["is_safe"]:
            workflow["final_response"] = response
            workflow["approved"] = True
            print("✅✅✅ RESPONSE APPROVED - DELIVERED TO USER")
        else:
            workflow[
                "final_response"] = "I need to refine my response. Could you rephrase your concern?"
            workflow["approved"] = False
            print("⚠️  RESPONSE NEEDS REVISION")

        print(f"{'='*60}\n")

        return workflow

    def _generate_safety_response(self, safety_result: Dict[str, Any]) -> str:
        """Generate appropriate response for unsafe input"""
        category = safety_result.get("category", "unknown")

        if category == "S11":  # Self-harm
            return """I'm really concerned about what you've shared. Your safety is the most important thing right now.

Please reach out to a crisis helpline immediately:
- India: AASRA - 91-22-27546669
- USA: 988 (Suicide & Crisis Lifeline)
- International: https://findahelpline.com

You can also:
- Call emergency services (112 in India)
- Go to the nearest emergency room
- Tell someone you trust right now

You don't have to face this alone. Professional help is available 24/7."""

        else:
            return "I'm not able to provide support for this type of concern. Please consult with an appropriate professional or trusted resource."

    def _handle_crisis(self, user_input: str) -> str:
        """Handle crisis situations"""
        crisis_prompt = """You are a crisis counselor. The user is in distress. Respond with:
1. Immediate empathy and validation
2. Crisis resources (hotlines, emergency contacts)
3. Encouragement to seek immediate professional help
4. Brief grounding technique if appropriate

Keep response brief (3-4 sentences) and focus on immediate safety."""

        response = self.llm.generate_response(user_input,
                                              system_prompt=crisis_prompt,
                                              max_tokens=300,
                                              temperature=0.5)
        return response

    def _handle_general(self, user_input: str) -> str:
        """Handle general mental health queries"""
        general_prompt = """You are a supportive mental health assistant. Provide general guidance, validate feelings, and suggest appropriate next steps (therapy, self-care, resources). Be warm and non-judgmental."""

        response = self.llm.generate_response(user_input,
                                              system_prompt=general_prompt,
                                              max_tokens=400,
                                              temperature=0.7)
        return response

    def get_workflow_summary(self, workflow: Dict[str, Any]) -> str:
        """Generate human-readable workflow summary"""
        summary = []
        for step in workflow["steps"]:
            step_name = step["step"]
            result = step["result"]

            if "Pre-Safety" in step_name or "Post-Safety" in step_name:
                summary.append(
                    f"✅ {step_name}: {result.get('category', 'N/A')}")
            elif "Router" in step_name:
                summary.append(
                    f"🔀 {step_name}: → {result.get('specialist', 'N/A').upper()}"
                )
            elif "Judge" in step_name:
                scores = result.get('scores', {})
                summary.append(
                    f"⚖️  {step_name}: {scores.get('overall', 0)}/10")

        return "\n".join(summary)
