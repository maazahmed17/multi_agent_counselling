"""
Test script for all agents
"""
from demo.core.llm_client import LLMClient
from demo.agents.router_agent import RouterAgent
from demo.agents.anxiety_specialist import AnxietySpecialistAgent
from demo.agents.judge_agent import JudgeAgent


def test_agents():
    """Test the multi-agent system"""
    print("\n" + "="*60)
    print("🧪 TESTING MULTI-AGENT SYSTEM")
    print("="*60)

    # Initialize shared LLM client
    llm = LLMClient()

    # Initialize agents
    router = RouterAgent(llm)
    anxiety_specialist = AnxietySpecialistAgent(llm)
    judge = JudgeAgent(llm)

    # Test case
    user_input = "I'm feeling really anxious about my job interview tomorrow. I keep worrying I'll mess it up."

    print(f"\n📝 USER INPUT: {user_input}")

    # Step 1: Router
    routing = router.process(user_input)
    print(f"\n✅ Routing: {routing['specialist']}")

    # Step 2: Specialist (assuming anxiety)
    if routing['specialist'] == 'anxiety':
        specialist_response = anxiety_specialist.process(user_input)
        print(f"\n✅ Specialist Response:")
        print(f"{specialist_response['response'][:200]}...")

        # Step 3: Judge
        evaluation = judge.process(user_input, specialist_response['response'])
        print(f"\n✅ Judge Evaluation:")
        print(f"   Overall Score: {evaluation['scores']['overall']}/10")
        print(f"   Decision: {evaluation['scores']['decision']}")
        print(f"   Reasoning: {evaluation['scores']['reasoning']}")

        if evaluation['approved']:
            print(f"\n✅✅✅ RESPONSE APPROVED - READY TO DELIVER")
        else:
            print(f"\n⚠️  RESPONSE NEEDS REVISION")

    print("\n" + "="*60)
    print("🎉 AGENT TESTING COMPLETE")
    print("="*60)


if __name__ == "__main__":
    test_agents()
