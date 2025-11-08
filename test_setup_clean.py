"""
Minimal setup test - only tests what we need for Plan B
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_imports():
    """Test core libraries"""
    print("🔍 Testing imports...")

    try:
        import streamlit
        print(f"✅ Streamlit: {streamlit.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit: {e}")
        return False

    try:
        from huggingface_hub import InferenceClient
        print("✅ Hugging Face Hub: Ready")
    except ImportError as e:
        print(f"❌ HF Hub: {e}")
        return False

    try:
        import requests
        print(f"✅ Requests: {requests.__version__}")
    except ImportError as e:
        print(f"❌ Requests: {e}")
        return False

    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv: Ready")
    except ImportError as e:
        print(f"❌ Python-dotenv: {e}")
        return False

    return True

def test_env():
    """Test environment variables"""
    print("\n🔍 Testing environment...")

    token = os.getenv("HUGGINGFACE_TOKEN")
    if token and token != "your_token_here":
        print(f"✅ HF Token: Set (starts with {token[:10]}...)")
        return True
    else:
        print("❌ HF Token: NOT SET")
        print("   → Add to .env: HUGGINGFACE_TOKEN=hf_...")
        return False

def test_api():
    """Test HF API connection"""
    print("\n🔍 Testing API...")

    try:
        from huggingface_hub import InferenceClient
        token = os.getenv("HUGGINGFACE_TOKEN")

        if not token or token == "your_token_here":
            print("⚠️  Skipping - no token")
            return False

        client = InferenceClient(token=token)
        response = client.text_generation(
            "Hello", 
            model="gpt2",
            max_new_tokens=5
        )

        print(f"✅ API works: {response[:30]}...")
        return True

    except Exception as e:
        print(f"❌ API failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 PLAN B: MINIMAL ENVIRONMENT TEST")
    print("=" * 60)

    imports_ok = test_imports()
    env_ok = test_env() if imports_ok else False
    api_ok = test_api() if env_ok else False

    print("\n" + "=" * 60)
    if imports_ok and env_ok and api_ok:
        print("✅✅✅ READY TO BUILD (PLAN B - NO LANGGRAPH)")
        print("💡 We'll use pure Python for agent orchestration")
        print("=" * 60)
        print("\n🎯 NEXT: Build LLM Client + Agent Classes")
    elif imports_ok and not env_ok:
        print("⚠️  LIBRARIES OK - ADD HF TOKEN")
        print("=" * 60)
    else:
        print("❌ FIX ERRORS ABOVE")
        print("=" * 60)
