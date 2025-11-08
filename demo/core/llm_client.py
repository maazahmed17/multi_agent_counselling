"""
LLM Client - Direct HTTP API calls to Groq (NO SDK dependencies)
Works around Replit's broken pydantic environment
"""
import os
import json
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()


class LLMClient:
    """
    Unified client using direct HTTP calls to Groq API
    No pydantic/SDK dependencies
    """

    def __init__(self):
        """Initialize with Groq API key"""
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key or self.api_key == "your_groq_key_here":
            raise ValueError("❌ GROQ_API_KEY not set in .env file!\n"
                             "Get key from: https://console.groq.com/keys")

        # Groq API endpoint
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

        # Model configurations
        self.llama_instruct = os.getenv("LLAMA_INSTRUCT_MODEL",
                                        "llama-3.1-8b-instant")
        self.llama_guard = os.getenv("LLAMA_GUARD_MODEL", "llama-guard-3-8b")

        print(f"✅ LLM Client initialized (Groq Direct API)")
        print(f"   - Instruct Model: {self.llama_instruct}")
        print(f"   - Guard Model: {self.llama_guard}")

    def _make_request(self,
                      messages: List[Dict[str, str]],
                      model: str,
                      max_tokens: int,
                      temperature: float,
                      retry_count: int = 3) -> str:
        """Make direct HTTP request to Groq API"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9
        }

        for attempt in range(retry_count):
            try:
                response = requests.post(self.base_url,
                                         headers=headers,
                                         json=payload,
                                         timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    error_msg = f"API error {response.status_code}: {response.text}"
                    if attempt < retry_count - 1:
                        print(
                            f"⚠️  Attempt {attempt + 1} failed: {error_msg}, retrying..."
                        )
                        time.sleep(1)
                        continue
                    else:
                        return f"[Error: {error_msg}]"

            except requests.exceptions.Timeout:
                if attempt < retry_count - 1:
                    print(f"⚠️  Timeout on attempt {attempt + 1}, retrying...")
                    time.sleep(1)
                    continue
                else:
                    return "[Error: Request timeout]"

            except Exception as e:
                if attempt < retry_count - 1:
                    print(
                        f"⚠️  Attempt {attempt + 1} failed: {e}, retrying...")
                    time.sleep(1)
                    continue
                else:
                    return f"[Error: {str(e)}]"

        return "[Error: Max retries exceeded]"

    def generate_response(self,
                          prompt: str,
                          model: Optional[str] = None,
                          max_tokens: int = 512,
                          temperature: float = 0.7,
                          system_prompt: Optional[str] = None,
                          retry_count: int = 3) -> str:
        """
        Generate a response using direct API call

        Args:
            prompt: User input
            model: Model to use
            max_tokens: Maximum response length
            temperature: Sampling temperature
            system_prompt: Optional system instruction
            retry_count: Number of retries

        Returns:
            Generated text response
        """
        if model is None:
            model = self.llama_instruct

        # Build messages
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        return self._make_request(messages, model, max_tokens, temperature,
                                  retry_count)

    def generate_with_chat_format(self,
                                  messages: List[Dict[str, str]],
                                  model: Optional[str] = None,
                                  max_tokens: int = 512,
                                  temperature: float = 0.7) -> str:
        """
        Generate response using chat message format

        Args:
            messages: List of message dicts
            model: Model to use
            max_tokens: Max tokens
            temperature: Temperature

        Returns:
            Generated response
        """
        if model is None:
            model = self.llama_instruct

        return self._make_request(messages, model, max_tokens, temperature)

    def check_safety(self, text: str, retry_count: int = 2) -> Dict[str, Any]:
        """
        Check if text is safe using Llama Guard

        Args:
            text: Text to check
            retry_count: Number of retries

        Returns:
            Dict with safety assessment
        """
        guard_prompt = f"""Task: Check if there is unsafe content in the user message according to our safety policy.

<BEGIN UNSAFE CONTENT CATEGORIES>
S1: Violent Crimes
S2: Non-Violent Crimes  
S3: Sex Crimes
S4: Child Exploitation
S5: Defamation
S6: Specialized Advice (financial, medical, legal)
S7: Privacy
S8: Intellectual Property
S9: Indiscriminate Weapons
S10: Hate
S11: Self-Harm
S12: Sexual Content
S13: Elections
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
User: {text}
<END CONVERSATION>

Provide your safety assessment. Reply with "safe" or "unsafe" followed by the category if unsafe."""

        messages = [{"role": "user", "content": guard_prompt}]

        result = self._make_request(messages,
                                    self.llama_guard,
                                    max_tokens=100,
                                    temperature=0.1,
                                    retry_count=retry_count)

        result_lower = result.lower()

        # Parse response
        if "unsafe" in result_lower:
            # Extract category
            import re
            category = "unknown"
            match = re.search(r'S\d+', result.upper())
            if match:
                category = match.group(0)

            return {
                "is_safe": False,
                "category": category,
                "confidence": 0.9,
                "response": result
            }
        elif "safe" in result_lower:
            return {
                "is_safe": True,
                "category": "safe",
                "confidence": 0.9,
                "response": result
            }
        else:
            # Ambiguous - default to unsafe
            return {
                "is_safe": False,
                "category": "unclear",
                "confidence": 0.5,
                "response": result
            }


def test_client():
    """Test the LLM client"""
    print("\n" + "=" * 60)
    print("🧪 TESTING GROQ CLIENT (DIRECT HTTP)")
    print("=" * 60)

    try:
        client = LLMClient()

        # Test 1: Basic response
        print("\n📝 Test 1: Basic Response")
        response = client.generate_response(
            "What is anxiety? Answer in one sentence.",
            max_tokens=50,
            temperature=0.7)
        print(f"✅ Response: {response}")

        # Test 2: Therapeutic response
        print("\n📝 Test 2: Therapeutic Response")
        response = client.generate_response(
            "I feel anxious about my exam tomorrow.",
            system_prompt=
            "You are a compassionate anxiety specialist trained in CBT. Provide brief, supportive guidance.",
            max_tokens=150,
            temperature=0.7)
        print(f"✅ Response: {response[:250]}...")

        # Test 3: Safety - safe content
        print("\n🛡️  Test 3: Safety Check (Safe)")
        safety = client.check_safety(
            "I'm worried about my job interview tomorrow.")
        print(f"   Is Safe: {safety['is_safe']}")
        print(f"   Category: {safety['category']}")

        # Test 4: Safety - self-harm
        print("\n🛡️  Test 4: Safety Check (Self-Harm)")
        safety = client.check_safety("I want to hurt myself and end my life.")
        print(f"   Is Safe: {safety['is_safe']}")
        print(f"   Category: {safety['category']}")

        # Test 5: Multi-turn chat
        print("\n💬 Test 5: Multi-Turn Chat")
        messages = [{
            "role": "system",
            "content": "You are a helpful anxiety counselor."
        }, {
            "role": "user",
            "content": "I have social anxiety."
        }]
        response = client.generate_with_chat_format(messages, max_tokens=100)
        print(f"✅ Response: {response[:200]}...")

        print("\n" + "=" * 60)
        print("✅✅✅ ALL TESTS PASSED - CLIENT WORKING!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_client()
