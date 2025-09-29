#!/usr/bin/env python3
"""
CompanionAI Pre-Training Validation Suite
Validates datasets, models, and training pipeline for RTX 4060 8GB
"""

import os
import json
import torch
import psutil
import subprocess
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from datasets import load_dataset
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ValidationSuite:
    def __init__(self):
        self.results = {}
        self.gpu_memory_gb = 8  # RTX 4060 8GB
        self.print_header("🚀 CompanionAI Pre-Training Validation Suite")
        
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f"{text:^60}")
        print(f"{'='*60}\n")
        
    def print_section(self, text):
        print(f"\n🔍 {text}")
        print("-" * 50)
        
    def log_result(self, test_name, status, details=""):
        self.results[test_name] = {"status": status, "details": details}
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   └─ {details}")

    def check_system_resources(self):
        """Verify system meets requirements"""
        self.print_section("System Resource Check")
        
        # GPU Check
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            self.log_result("GPU Detection", "PASS", f"{gpu_name} - {gpu_memory:.1f}GB")
            
            if gpu_memory >= 7.5:  # Account for system overhead
                self.log_result("GPU Memory", "PASS", f"{gpu_memory:.1f}GB available")
            else:
                self.log_result("GPU Memory", "WARNING", f"Only {gpu_memory:.1f}GB - may limit batch size")
        else:
            self.log_result("GPU Detection", "FAIL", "CUDA not available")
            
        # RAM Check
        ram_gb = psutil.virtual_memory().total / (1024**3)
        if ram_gb >= 14:  # Your 16GB - 2GB for OS
            self.log_result("System RAM", "PASS", f"{ram_gb:.1f}GB available")
        else:
            self.log_result("System RAM", "WARNING", f"Only {ram_gb:.1f}GB - recommend 16GB+")
            
        # Storage Check
        disk_free = psutil.disk_usage('.').free / (1024**3)
        if disk_free >= 50:
            self.log_result("Storage Space", "PASS", f"{disk_free:.1f}GB free")
        else:
            self.log_result("Storage Space", "WARNING", f"Only {disk_free:.1f}GB free")

    def validate_models(self):
        """Check if models are properly loaded and cached"""
        self.print_section("Model Validation")
        
        models_to_check = {
            "meta-llama/Meta-Llama-3.1-8B-Instruct": "Anxiety Specialist Base",
            "meta-llama/Llama-Guard-3-8B": "Safety Classification"
        }
        
        for model_name, purpose in models_to_check.items():
            try:
                # Check if model is cached
                cache_dir = Path.home() / ".cache/huggingface/hub"
                model_cache_exists = any(model_name.replace("/", "--") in str(p) for p in cache_dir.glob("*"))
                
                if model_cache_exists:
                    self.log_result(f"Model Cache - {purpose}", "PASS", f"{model_name}")
                else:
                    self.log_result(f"Model Cache - {purpose}", "FAIL", f"{model_name} not cached")
                    continue
                    
                # Try loading tokenizer
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.log_result(f"Tokenizer - {purpose}", "PASS", f"Vocab size: {tokenizer.vocab_size}")
                
            except Exception as e:
                self.log_result(f"Model Load - {purpose}", "FAIL", str(e))

    def test_quantization_memory(self):
        """Test 4-bit quantization memory usage"""
        self.print_section("QLoRA Memory Test")
        
        try:
            # Configure 4-bit quantization
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            
            # Test load Llama 3.1 8B with quantization
            print("Loading Llama 3.1 8B with 4-bit quantization...")
            torch.cuda.empty_cache()
            initial_memory = torch.cuda.memory_allocated() / (1024**3)
            
            model = AutoModelForCausalLM.from_pretrained(
                "meta-llama/Meta-Llama-3.1-8B-Instruct",
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.bfloat16,
            )
            
            peak_memory = torch.cuda.max_memory_allocated() / (1024**3)
            current_memory = torch.cuda.memory_allocated() / (1024**3)
            
            self.log_result("4-bit Quantization", "PASS", 
                          f"Peak: {peak_memory:.2f}GB, Current: {current_memory:.2f}GB")
            
            # Test inference
            tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
            test_input = "I feel anxious about my upcoming exam."
            inputs = tokenizer(test_input, return_tensors="pt").to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=50, do_sample=False)
                
            self.log_result("Inference Test", "PASS", "Model generates responses successfully")
            
            # Cleanup
            del model, tokenizer
            torch.cuda.empty_cache()
            
        except Exception as e:
            self.log_result("QLoRA Memory Test", "FAIL", str(e))

    def validate_datasets(self):
        """Check dataset format and quality"""
        self.print_section("Dataset Validation")
        
        # Define expected dataset locations based on your project
        dataset_paths = {
            "anxiety_cbt_data.json": "CBT-focused anxiety conversations",
            "crisis_intervention_data.json": "Crisis intervention protocols", 
            "safety_classification_data.json": "Llama Guard training data",
            "general_counseling_data.json": "General therapeutic conversations"
        }
        
        for filename, description in dataset_paths.items():
            if os.path.exists(filename):
                try:
                    # Load and validate JSON structure
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if isinstance(data, list) and len(data) > 0:
                        # Check first entry structure
                        sample = data[0]
                        required_keys = ['instruction', 'input', 'output']
                        
                        if all(key in sample for key in required_keys):
                            self.log_result(f"Dataset Format - {description}", "PASS", 
                                          f"{len(data)} samples, correct structure")
                            
                            # Quality checks
                            avg_input_len = np.mean([len(item.get('input', '')) for item in data[:100]])
                            avg_output_len = np.mean([len(item.get('output', '')) for item in data[:100]])
                            
                            self.log_result(f"Dataset Quality - {description}", "PASS",
                                          f"Avg input: {avg_input_len:.0f} chars, output: {avg_output_len:.0f} chars")
                        else:
                            self.log_result(f"Dataset Format - {description}", "FAIL", 
                                          f"Missing required keys: {set(required_keys) - set(sample.keys())}")
                    else:
                        self.log_result(f"Dataset Format - {description}", "FAIL", "Empty or invalid format")
                        
                except Exception as e:
                    self.log_result(f"Dataset Load - {description}", "FAIL", str(e))
            else:
                self.log_result(f"Dataset File - {description}", "WARNING", f"{filename} not found")

    def test_training_pipeline(self):
        """Test QLoRA training setup without actual training"""
        self.print_section("Training Pipeline Test")
        
        try:
            from peft import LoraConfig, get_peft_model, TaskType
            from transformers import TrainingArguments
            
            # Test LoRA configuration
            lora_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                inference_mode=False,
                r=16,  # Conservative for RTX 4060
                lora_alpha=32,
                lora_dropout=0.1,
                target_modules=["q_proj", "v_proj", "gate_proj", "up_proj"]
            )
            self.log_result("LoRA Configuration", "PASS", "r=16, alpha=32, dropout=0.1")
            
            # Test training arguments
            training_args = TrainingArguments(
                output_dir="./test_output",
                per_device_train_batch_size=1,  # Conservative for 8GB
                gradient_accumulation_steps=8,   # Effective batch size = 8
                learning_rate=2e-4,
                num_train_epochs=3,
                logging_steps=10,
                save_steps=500,
                evaluation_strategy="steps",
                eval_steps=500,
                warmup_steps=100,
                fp16=True,  # Memory optimization
                dataloader_pin_memory=False,
                remove_unused_columns=False,
            )
            self.log_result("Training Arguments", "PASS", 
                          "batch_size=1, grad_accum=8, fp16=True")
            
        except Exception as e:
            self.log_result("Training Pipeline", "FAIL", str(e))

    def estimate_training_time(self):
        """Estimate training time and resource requirements"""
        self.print_section("Training Time Estimation")
        
        # Estimates based on RTX 4060 8GB performance
        estimates = {
            "Anxiety Specialist (15K samples)": "8-12 hours",
            "Crisis Specialist (10K samples)": "6-10 hours", 
            "Safety Classifier (5K samples)": "3-6 hours",
            "Total Training Time": "17-28 hours"
        }
        
        for task, time_est in estimates.items():
            self.log_result(f"Estimated Time - {task}", "INFO", time_est)
        
        # Memory recommendations
        self.log_result("Memory Optimization", "INFO", 
                       "Use batch_size=1, grad_accumulation=8-16")
        self.log_result("Power Management", "INFO", 
                       "Ensure laptop is plugged in and cooling is adequate")

    def check_dependencies(self):
        """Verify all required libraries are installed"""
        self.print_section("Dependency Check")
        
        required_packages = [
            ("torch", "PyTorch"),
            ("transformers", "HuggingFace Transformers"),
            ("peft", "Parameter Efficient Fine-Tuning"),
            ("bitsandbytes", "Quantization"),
            ("accelerate", "Training Acceleration"),
            ("datasets", "Dataset Loading"),
            ("trl", "Transformer Reinforcement Learning"),
        ]
        
        for package, description in required_packages:
            try:
                __import__(package)
                self.log_result(f"Package - {description}", "PASS", package)
            except ImportError:
                self.log_result(f"Package - {description}", "FAIL", f"{package} not installed")

    def generate_report(self):
        """Generate final validation report"""
        self.print_section("Validation Summary")
        
        passed = sum(1 for r in self.results.values() if r["status"] == "PASS")
        failed = sum(1 for r in self.results.values() if r["status"] == "FAIL")
        warnings = sum(1 for r in self.results.values() if r["status"] == "WARNING")
        
        print(f"📊 Results: {passed} PASSED, {failed} FAILED, {warnings} WARNINGS")
        
        if failed == 0:
            print("🎉 System is ready for fine-tuning!")
            print("\nNext Steps:")
            print("1. Start with Anxiety Specialist fine-tuning")
            print("2. Use conservative settings: batch_size=1, grad_accumulation=8")
            print("3. Monitor GPU temperature and memory usage")
            print("4. Expected training time: 8-12 hours")
        else:
            print("⚠️ Address failed checks before proceeding with training")
            
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"validation_report_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Detailed report saved to: {report_file}")

    def run_all_tests(self):
        """Execute complete validation suite"""
        start_time = datetime.now()
        
        self.check_system_resources()
        self.check_dependencies() 
        self.validate_models()
        self.validate_datasets()
        self.test_quantization_memory()
        self.test_training_pipeline()
        self.estimate_training_time()
        
        end_time = datetime.now()
        duration = (end_time - start_time).seconds
        
        print(f"\n⏱️ Validation completed in {duration} seconds")
        self.generate_report()

if __name__ == "__main__":
    validator = ValidationSuite()
    validator.run_all_tests()
