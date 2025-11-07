# CompanionAI Anxiety Specialist

## Overview
This is a machine learning project for fine-tuning Meta's Llama 3.1 8B model to create a specialized anxiety support chatbot using Cognitive Behavioral Therapy (CBT) principles. The project uses QLoRA (Quantized Low-Rank Adaptation) for memory-efficient fine-tuning optimized for RTX 4060 8GB GPU.

## Project Structure
- `anxiety.py` - Main training script with memory-optimized settings for RTX 4060 8GB
- `validate_setup.py` - Pre-training validation suite to check system resources and dependencies
- `validate_model.py` - Post-training validation and model quality assessment
- `test_llama-3.py` - Quick test script for Llama model loading with quantization
- `test_guard.py` - Safety classification testing
- `dataset_loader.py` - Dataset loading and preprocessing utilities
- `models/anxiety_specialist_v1/` - Trained LoRA adapter weights and configuration
- `eval_outputs/` - Evaluation metrics and results
- `validation_results/` - Model validation outputs

## Recent Changes
- Initial project import to Replit environment
- Set up Python 3.11 environment
- Installed core ML dependencies (PyTorch CPU, Transformers, PEFT, etc.)

## Architecture

### Technology Stack
- **Base Model**: Meta Llama 3.1 8B Instruct
- **Fine-tuning Method**: QLoRA (4-bit quantization + LoRA)
- **Framework**: PyTorch, HuggingFace Transformers, PEFT
- **Training**: TRL (Transformer Reinforcement Learning)
- **Optimization**: BitsAndBytes 4-bit quantization

### Memory Optimization
The training is configured for 8GB VRAM with:
- 4-bit NF4 quantization
- LoRA rank 8, alpha 16
- Max sequence length: 512 tokens
- Batch size: 1 with gradient accumulation (32 steps)
- FP16 mixed precision training
- Gradient checkpointing enabled

## Important Notes

### GPU Requirements
This project is designed for **GPU training** with CUDA support. The current Replit environment runs on CPU only, which means:
- ✅ Code can be viewed and edited
- ✅ Dependencies are installed
- ✅ Project structure can be explored
- ❌ Training cannot run (requires NVIDIA GPU with CUDA)
- ❌ Model inference will be extremely slow on CPU

### Running Locally
To run this project on a machine with NVIDIA GPU:
1. Set up a conda environment: `conda env create -f ai_env.yml`
2. Or install from requirements.txt: `pip install -r requirements.txt`
3. Ensure CUDA and cuDNN are properly installed
4. Run validation: `python validate_setup.py`
5. Start training: `python anxiety.py`

### Dataset Requirements
The training scripts expect datasets in `./data_lake/mentalchat16k/processed/` directory:
- `anxiety_sft_train.jsonl` - Training data
- `anxiety_sft_val.jsonl` - Validation data  
- `anxiety_sft_test.jsonl` - Test data

These are not included in the repository and need to be prepared separately.

## User Preferences
- Optimized for RTX 4060 8GB VRAM
- Conservative memory settings to prevent OOM errors
- Offline-first approach (uses local model cache)
- Focus on anxiety support using CBT methodology

## Development Environment
- Python 3.11.13
- PyTorch (CPU-only in Replit)
- No conda in Replit (using pip)
- Git version control enabled
