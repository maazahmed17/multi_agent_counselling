#!/usr/bin/env python3
"""
CompanionAI Anxiety Specialist - Project Information
Displays project overview and system status in Replit environment
"""

import sys

def print_header(text):
    print(f"\n{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}\n")

def print_section(text):
    print(f"\n{'='*70}")
    print(f"📋 {text}")
    print(f"{'='*70}")

def main():
    print_header("🧠 CompanionAI Anxiety Specialist")
    
    print_section("Project Overview")
    print("""
This is a machine learning project for fine-tuning Meta's Llama 3.1 8B model
to create a specialized anxiety support chatbot using Cognitive Behavioral
Therapy (CBT) principles.

The project uses QLoRA (Quantized Low-Rank Adaptation) for memory-efficient
fine-tuning, optimized for RTX 4060 8GB GPU.
""")
    
    print_section("Key Components")
    print("""
📁 Main Scripts:
  • anxiety.py          - Training script with memory-optimized settings
  • validate_setup.py   - Pre-training validation suite
  • validate_model.py   - Post-training model validation
  • test_llama-3.py     - Quick Llama model loading test
  
📂 Directories:
  • models/anxiety_specialist_v1/  - Trained LoRA adapter weights
  • eval_outputs/                  - Evaluation metrics
  • validation_results/            - Validation outputs
""")
    
    print_section("System Status")
    
    # Check Python version
    print(f"✓ Python Version: {sys.version.split()[0]}")
    
    # Check PyTorch
    try:
        import torch
        torch_version = getattr(torch, '__version__', 'installed (version unknown)')
        print(f"✓ PyTorch Version: {torch_version}")
        
        # Check CUDA availability
        if hasattr(torch, 'cuda') and torch.cuda.is_available():
            print(f"✓ CUDA Available: YES")
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
            print(f"  VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f}GB")
        else:
            print(f"⚠ CUDA Available: NO (CPU-only mode)")
            print(f"  Note: Training requires NVIDIA GPU with CUDA support")
    except Exception as e:
        print(f"⚠ PyTorch: Error loading - {str(e)}")
    
    # Check Transformers
    try:
        import transformers
        print(f"✓ Transformers Version: {transformers.__version__}")
    except ImportError:
        print("✗ Transformers: Not installed")
    
    # Check PEFT
    try:
        import peft
        print(f"✓ PEFT Version: {peft.__version__}")
    except ImportError:
        print("✗ PEFT: Not installed")
    
    # Check Datasets
    try:
        import datasets
        print(f"✓ Datasets Version: {datasets.__version__}")
    except ImportError:
        print("✗ Datasets: Not installed")
    
    print_section("Important Notes")
    print("""
⚠️  GPU REQUIREMENT:
    This project requires an NVIDIA GPU with CUDA support for training.
    Replit's environment runs on CPU only, which means:
    
    ✅ Code can be viewed and edited
    ✅ Dependencies are installed  
    ✅ Project structure can be explored
    ❌ Training cannot run (requires NVIDIA GPU with CUDA)
    ❌ Model inference will be extremely slow on CPU

📚 DATASET REQUIREMENT:
    Training expects datasets in ./data_lake/mentalchat16k/processed/:
    • anxiety_sft_train.jsonl
    • anxiety_sft_val.jsonl
    • anxiety_sft_test.jsonl
    
    These are not included and need to be prepared separately.

🚀 TO RUN LOCALLY:
    1. Set up environment: conda env create -f ai_env.yml
    2. Or use pip: pip install -r requirements.txt
    3. Ensure CUDA and cuDNN are installed
    4. Validate setup: python validate_setup.py
    5. Start training: python anxiety.py
""")
    
    print_section("Model Information")
    print("""
📊 Training Configuration:
  • Base Model: Meta Llama 3.1 8B Instruct
  • Method: QLoRA (4-bit quantization + LoRA)
  • LoRA Rank: 8, Alpha: 16
  • Max Seq Length: 512 tokens
  • Batch Size: 1 (gradient accumulation: 32)
  • Precision: FP16 mixed precision
  • Estimated Training Time: 4-6 hours (RTX 4060)

🎯 Use Case:
  Anxiety support chatbot trained on CBT-based mental health conversations.
  The model provides empathetic, structured, and safety-aware responses.
""")
    
    print_section("Next Steps")
    print("""
If you're viewing this in Replit:
  • Explore the code and project structure
  • Review the training configuration in anxiety.py
  • Check the model card in models/anxiety_specialist_v1/README.md
  • Clone this repo to run on a machine with NVIDIA GPU

For Questions or Issues:
  • Review replit.md for detailed documentation
  • Check validation reports in validation_results/
""")
    
    print_header("Project Status: Ready for Local GPU Training")
    print()

if __name__ == "__main__":
    main()
