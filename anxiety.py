#!/usr/bin/env python3
"""
CompanionAI Anxiety Specialist - Memory Optimized for RTX 4060 8GB
Ultra-conservative settings to prevent CUDA OOM
"""

import os
import torch
import json
from datetime import datetime
from pathlib import Path

# Set environment variables BEFORE importing other libraries
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Training libraries
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset
import pandas as pd

# Memory-Optimized Configuration for RTX 4060 8GB
class MemoryOptimizedConfig:
    def __init__(self):
        # Model settings
        self.base_model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
        self.output_dir = "./models/anxiety_specialist_v1"
        
        # Dataset paths
        self.train_data = "./data_lake/mentalchat16k/processed/anxiety_sft_train.jsonl"
        self.val_data = "./data_lake/mentalchat16k/processed/anxiety_sft_val.jsonl"
        
        # ULTRA-CONSERVATIVE Memory Settings
        self.max_seq_length = 512    # Reduced from 1024 - saves 50% memory
        self.batch_size = 1          # Must remain 1
        self.gradient_accumulation_steps = 32  # Increased to maintain effective batch size
        self.learning_rate = 1e-4    # Slightly lower for stability
        self.epochs = 2              # Reduced to save time/memory
        self.warmup_steps = 50       # Reduced
        
        # Conservative LoRA settings
        self.lora_r = 8              # Reduced from 16 - saves memory
        self.lora_alpha = 16         # Scaled proportionally
        self.lora_dropout = 0.1
        
        # Memory-focused logging
        self.logging_steps = 50      # Increased to reduce overhead
        self.save_steps = 500        # Increased to reduce I/O
        self.eval_steps = 500        # Increased to reduce overhead

def setup_model_and_tokenizer(config):
    """Load model with maximum memory optimization"""
    print("🚀 Loading Llama 3.1 8B with ULTRA-AGGRESSIVE memory optimization...")
    
    # Clear any existing GPU memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    
    # Most aggressive 4-bit quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,  # Changed from bfloat16 to save memory
        bnb_4bit_use_double_quant=False,       # Disabled to save memory
        llm_int8_enable_fp32_cpu_offload=True  # Enable CPU offloading if needed
    )
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(config.base_model)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    # Load model with maximum memory conservation
# Load model with maximum memory conservation
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        quantization_config=bnb_config,
        device_map="auto",
        dtype=torch.float16,        # torch_dtype is deprecated; use dtype
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )

    # Disable KV-cache during training (checkpointing requires this)
# Disable KV-cache during training for checkpointing compatibility
    model.config.use_cache = False  # avoids “use_cache=True is incompatible with gradient checkpointing” [web:70]

    # Enable gradient checkpointing at the model level
    if hasattr(model, "gradient_checkpointing_enable"):
        model.gradient_checkpointing_enable()  # saves memory, keeps graph intact [web:70][web:76]

    # Ensure inputs require grad so loss has a grad_fn under PEFT/QLoRA
    if hasattr(model, "enable_input_require_grads"):
        model.enable_input_require_grads()     # crucial to avoid “element 0 ... does not require grad” [web:65][web:70]

    # Apply LoRA after enabling training features
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=["q_proj", "v_proj"]
    )
    model = get_peft_model(model, lora_config)


    model.print_trainable_parameters()
    
    # Clear cache after loading
    torch.cuda.empty_cache()
    
    return model, tokenizer

def load_and_prepare_data(config, tokenizer):
    """Load and prepare data with memory optimization"""
    print("📊 Loading anxiety training datasets...")
    
    # Load smaller subset to test first
    train_dataset = load_dataset('json', data_files=config.train_data, split='train[:2000]')  # Limited subset
    val_dataset = load_dataset('json', data_files=config.val_data, split='train[:400]')      # Limited subset
    
    print(f"Training samples: {len(train_dataset)} (limited for memory)")
    print(f"Validation samples: {len(val_dataset)} (limited for memory)")
    
    def format_conversation(example):
        """Shorter format to reduce memory usage"""
        conversation = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        conversation += f"{example['instruction']}<|eot_id|>\n"
        conversation += f"<|start_header_id|>user<|end_header_id|>\n{example['input']}<|eot_id|>\n"
        conversation += f"<|start_header_id|>assistant<|end_header_id|>\n{example['output']}<|eot_id|>"
        
        return {"text": conversation}
    
    # Apply formatting
    train_dataset = train_dataset.map(format_conversation, remove_columns=train_dataset.column_names)
    val_dataset = val_dataset.map(format_conversation, remove_columns=val_dataset.column_names)
    
    def tokenize_function(examples):
        """Memory-optimized tokenization"""
        tokenized = tokenizer(
            examples["text"],
            truncation=True,
            max_length=config.max_seq_length,  # Reduced to 512
            padding="max_length",
        )
        
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized
    
    # Process with smaller batches
    train_dataset = train_dataset.map(
        tokenize_function,
        batched=True,
        batch_size=100,  # Smaller batch size for processing
        remove_columns=["text"],
        desc="Tokenizing training data"
    )
    val_dataset = val_dataset.map(
        tokenize_function,
        batched=True,
        batch_size=100,
        remove_columns=["text"],
        desc="Tokenizing validation data"
    )
    
    return train_dataset, val_dataset

def setup_training_arguments(config):
    """Memory-optimized training arguments"""
    return TrainingArguments(
        output_dir=config.output_dir,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        num_train_epochs=config.epochs,
        lr_scheduler_type="linear",  # Changed from cosine - uses less memory
        warmup_steps=config.warmup_steps,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        eval_strategy="steps",
        eval_steps=config.eval_steps,
        save_total_limit=2,  # Reduced from 3
        load_best_model_at_end=False,  # Disabled to save memory
        
        # AGGRESSIVE Memory optimization
        fp16=True,
        dataloader_pin_memory=False,
        remove_unused_columns=True,  # Changed to True
        dataloader_num_workers=0,    # Reduced to 0 to save memory
        # gradient_checkpointing=True, # Enable gradient checkpointing
        optim="adamw_torch",         # Use torch optimizer (uses less memory)
        
        # Disable extra features
        report_to="none",
        logging_dir=None,            # Disable logging directory
        prediction_loss_only=True,  # Only compute loss, not additional metrics
        
        # Memory cleanup
        dataloader_drop_last=True,
        eval_accumulation_steps=1,
        
        # Additional memory optimizations
        max_grad_norm=1.0,
        weight_decay=0.01,
        adam_epsilon=1e-8,
    )

def main():
    """Main training function with memory monitoring"""
    print("🎯 Starting MEMORY-OPTIMIZED Anxiety Specialist Fine-Tuning")
    print("=" * 70)
    
    # Initialize config
    config = MemoryOptimizedConfig()
    
    # Check GPU memory before starting
    if torch.cuda.is_available():
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f}GB")
        torch.cuda.empty_cache()
        print(f"Free Memory: {torch.cuda.memory_reserved(0) / (1024**3):.2f}GB")
    
    # Setup model and tokenizer
    model, tokenizer = setup_model_and_tokenizer(config)
    
    # Check memory after model loading
    if torch.cuda.is_available():
        print(f"Memory after model loading: {torch.cuda.memory_allocated(0) / (1024**3):.2f}GB")
    
    # Load data
    train_dataset, val_dataset = load_and_prepare_data(config, tokenizer)
    
    # Training arguments
    training_args = setup_training_arguments(config)
    
    # Lightweight data collator
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        padding=True,
        return_tensors="pt",
        pad_to_multiple_of=8  # Optimize for tensor cores
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
    )
    
    # Memory check before training
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print(f"Memory before training: {torch.cuda.memory_allocated(0) / (1024**3):.2f}GB")
    
    print(f"🚀 Beginning CONSERVATIVE training at {datetime.now()}")
    print(f"📊 Training samples: {len(train_dataset)}")
    print(f"⏱️ Estimated time: 4-6 hours (reduced dataset)")
    print("💡 Monitor GPU temperature and memory usage closely")
    
    try:
        # Train the model
        trainer.train()
        
        # Save final model
        trainer.save_model(config.output_dir)
        tokenizer.save_pretrained(config.output_dir)
        
        print(f"✅ Training completed! Model saved to: {config.output_dir}")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        if torch.cuda.is_available():
            print(f"Memory at failure: {torch.cuda.memory_allocated(0) / (1024**3):.2f}GB")
        raise

if __name__ == "__main__":
    main()
