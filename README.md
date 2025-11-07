# CompanionAI Anxiety Specialist

A fine-tuned Llama 3.1 8B model specialized in providing anxiety support using Cognitive Behavioral Therapy (CBT) principles.

## 🎯 Project Overview

This project uses **QLoRA** (Quantized Low-Rank Adaptation) to efficiently fine-tune Meta's Llama 3.1 8B Instruct model for anxiety support conversations. The training is optimized for **RTX 4060 8GB** VRAM with aggressive memory optimizations.

### Key Features
- **4-bit NF4 quantization** for minimal memory footprint
- **LoRA fine-tuning** (rank 8, alpha 16) targeting attention layers
- **Memory-optimized training**: 512 token max length, batch size 1, gradient accumulation
- **CBT-focused responses**: Trained on mental health conversation datasets
- **Safety-aware**: Structured for empathetic and clinically appropriate responses

## 📁 Project Structure

```
.
├── anxiety.py              # Main training script
├── validate_setup.py       # Pre-training system validation
├── validate_model.py       # Post-training model evaluation
├── test_llama-3.py         # Quick model loading test
├── test_guard.py           # Safety classification testing
├── dataset_loader.py       # Data preprocessing utilities
├── requirements.txt        # Python dependencies
├── ai_env.yml             # Conda environment specification
├── models/                 # Model outputs
│   └── anxiety_specialist_v1/  # Trained LoRA adapters
├── eval_outputs/          # Evaluation metrics
└── validation_results/    # Validation reports
```

## ⚙️ Technical Specifications

### Model Configuration
- **Base Model**: `meta-llama/Meta-Llama-3.1-8B-Instruct`
- **Fine-tuning Method**: QLoRA (PEFT)
- **Quantization**: 4-bit NF4 with FP16 compute dtype
- **LoRA Parameters**:
  - Rank (r): 8
  - Alpha: 16
  - Dropout: 0.1
  - Target modules: `q_proj`, `v_proj`

### Training Parameters
- **Sequence Length**: 512 tokens
- **Batch Size**: 1 (per device)
- **Gradient Accumulation**: 32 steps
- **Effective Batch Size**: 32
- **Learning Rate**: 1e-4
- **Epochs**: 2
- **Precision**: FP16 mixed precision
- **Optimizer**: AdamW (PyTorch)

### Memory Optimization
- Gradient checkpointing enabled
- No KV-cache during training
- CPU offloading for quantization
- Minimal logging and checkpointing
- Conservative batch processing

## 🚀 Getting Started

### Prerequisites
- **NVIDIA GPU** with CUDA support (RTX 4060 or better)
- **8GB+ VRAM** (16GB recommended)
- **16GB+ System RAM**
- **50GB+ Free Disk Space**
- CUDA 12.1+ and cuDNN 8.9+

### Installation

#### Option 1: Conda Environment (Recommended)
```bash
conda env create -f ai_env.yml
conda activate ai_env
```

#### Option 2: pip
```bash
pip install -r requirements.txt
```

### Prepare Datasets
Place your training data in `./data_lake/mentalchat16k/processed/`:
- `anxiety_sft_train.jsonl`
- `anxiety_sft_val.jsonl`
- `anxiety_sft_test.jsonl`

Each JSONL file should contain entries with:
```json
{
  "instruction": "You are an anxiety specialist...",
  "input": "User's anxiety concern",
  "output": "Therapist's CBT-based response"
}
```

### Training

1. **Validate Setup**:
```bash
python validate_setup.py
```

2. **Start Training**:
```bash
python anxiety.py
```

Expected training time: **4-6 hours** on RTX 4060 8GB

3. **Validate Model**:
```bash
python validate_model.py
```

## 📊 Expected Results

### Model Performance
- Perplexity on test set: ~3-5 (lower is better)
- Specialized vocabulary for anxiety and CBT concepts
- Empathetic, structured, and safety-aware responses

### Example Interaction
```
User: I've been feeling really anxious about my job interview tomorrow.