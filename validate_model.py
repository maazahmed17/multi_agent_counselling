#!/usr/bin/env python3
"""
CompanionAI Anxiety Specialist Model Validation
RTX 4060 8GB optimized - strictly offline, sequential model loading
"""

import os
import json
import math
import gc
import time
from pathlib import Path
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

# Force strict offline mode - no network calls
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1" 
os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Configuration
BASE_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
ADAPTER_PATH = "./models/anxiety_specialist_v1"
TEST_DATA = "./data_lake/mentalchat16k/processed/anxiety_sft_test.jsonl"
OUTPUT_DIR = "./validation_results"

# Create output directory
Path(OUTPUT_DIR).mkdir(exist_ok=True)

class ValidationSuite:
    def __init__(self):
        self.results = {}
        self.print_header("🧪 Anxiety Specialist Model Validation")
        
    def print_header(self, text):
        print(f"\n{'='*70}")
        print(f"{text:^70}")
        print(f"{'='*70}\n")
        
    def print_section(self, text):
        print(f"\n🔍 {text}")
        print("-" * 60)

    def get_bnb_config(self):
        """4-bit quantization config"""
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=False
        )

    def load_tokenizer(self):
        """Load tokenizer from local cache only"""
        tokenizer = AutoTokenizer.from_pretrained(
            BASE_MODEL, 
            local_files_only=True
        )
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        return tokenizer

    def format_conversation(self, instruction, user_input, assistant_output):
        """Format conversation using Llama 3.1 chat template"""
        return (
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
            f"{instruction}<|eot_id|>\n"
            "<|start_header_id|>user<|end_header_id|>\n"
            f"{user_input}<|eot_id|>\n" 
            "<|start_header_id|>assistant<|end_header_id|>\n"
            f"{assistant_output}<|eot_id|>"
        )

    def compute_perplexity(self, model, tokenizer, test_dataset, max_samples=200):
        """Compute perplexity on test data"""
        print(f"Computing perplexity on {min(len(test_dataset), max_samples)} samples...")
        
        # Format test conversations
        formatted_texts = []
        for i in range(min(len(test_dataset), max_samples)):
            example = test_dataset[i]  # Access dataset by index
            text = self.format_conversation(
                example.get("instruction", "You are an anxiety specialist using CBT. Be empathic, structured, and safety-aware."),
                example["input"],
                example["output"]
            )
            formatted_texts.append(text)
        
        # Compute loss in batches
        total_loss = 0.0
        batch_size = 2  # Conservative for 8GB
        num_batches = 0
        
        for i in range(0, len(formatted_texts), batch_size):
            batch_texts = formatted_texts[i:i + batch_size]
            
            # Tokenize batch
            encoded = tokenizer(
                batch_texts,
                truncation=True,
                max_length=512,
                padding=True,
                return_tensors="pt"
            )
            
            # Move to GPU
            input_ids = encoded["input_ids"].to(model.device)
            attention_mask = encoded["attention_mask"].to(model.device)
            
            # Compute loss
            with torch.no_grad():
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=input_ids
                )
                total_loss += outputs.loss.item()
                num_batches += 1
            
            # Clear GPU memory
            del input_ids, attention_mask, encoded
            torch.cuda.empty_cache()
        
        avg_loss = total_loss / max(num_batches, 1)
        perplexity = math.exp(avg_loss)
        
        return avg_loss, perplexity


    def generate_responses(self, model, tokenizer, prompts):
        """Generate responses for evaluation prompts"""
        print(f"Generating responses for {len(prompts)} prompts...")
        
        responses = []
        for i, prompt in enumerate(prompts):
            print(f"  Prompt {i+1}/{len(prompts)}")
            
            # Format as conversation
            formatted_prompt = (
                "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
                "You are an anxiety specialist using CBT. Be empathic, structured, and safety-aware.<|eot_id|>\n"
                "<|start_header_id|>user<|end_header_id|>\n"
                f"{prompt}<|eot_id|>\n"
                "<|start_header_id|>assistant<|end_header_id|>\n"
            )
            
            # Tokenize
            inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)
            
            # Generate
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=200,
                    do_sample=False,  # Deterministic generation
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Decode response
            full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the assistant's response
            assistant_start = full_response.find("<|start_header_id|>assistant<|end_header_id|>\n")
            if assistant_start != -1:
                response = full_response[assistant_start + len("<|start_header_id|>assistant<|end_header_id|>\n"):].strip()
            else:
                response = full_response[len(formatted_prompt):].strip()
            
            responses.append(response)
            
            # Clear memory
            del inputs, outputs
            torch.cuda.empty_cache()
        
        return responses

    def evaluate_base_model(self, test_data, eval_prompts):
        """Evaluate base model"""
        self.print_section("Base Model Evaluation")
        
        # Load base model
        print("Loading base model...")
        tokenizer = self.load_tokenizer()
        
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            quantization_config=self.get_bnb_config(),
            device_map="auto",
            torch_dtype=torch.float16,
            local_files_only=True
        )
        base_model.config.use_cache = False
        base_model.eval()
        
        print(f"Base model loaded. Memory: {torch.cuda.memory_allocated(0) / (1024**3):.2f}GB")
        
        # Compute perplexity
        base_loss, base_ppl = self.compute_perplexity(base_model, tokenizer, test_data)
        
        # Generate responses
        base_responses = self.generate_responses(base_model, tokenizer, eval_prompts)
        
        # Cleanup
        del base_model, tokenizer
        gc.collect()
        torch.cuda.empty_cache()
        
        return {
            "loss": base_loss,
            "perplexity": base_ppl,
            "responses": base_responses
        }

    def evaluate_finetuned_model(self, test_data, eval_prompts):
        """Evaluate fine-tuned model"""
        self.print_section("Fine-tuned Model Evaluation")
        
        # Load tokenizer
        tokenizer = self.load_tokenizer()
        
        # Load base model
        print("Loading base model for fine-tuned evaluation...")
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            quantization_config=self.get_bnb_config(),
            device_map="auto", 
            torch_dtype=torch.float16,
            local_files_only=True
        )
        base_model.config.use_cache = False
        
        # Load LoRA adapter
        print("Loading LoRA adapter...")
        finetuned_model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
        finetuned_model.eval()
        
        print(f"Fine-tuned model loaded. Memory: {torch.cuda.memory_allocated(0) / (1024**3):.2f}GB")
        
        # Compute perplexity
        ft_loss, ft_ppl = self.compute_perplexity(finetuned_model, tokenizer, test_data)
        
        # Generate responses
        ft_responses = self.generate_responses(finetuned_model, tokenizer, eval_prompts)
        
        # Cleanup
        del finetuned_model, base_model, tokenizer
        gc.collect()
        torch.cuda.empty_cache()
        
        return {
            "loss": ft_loss,
            "perplexity": ft_ppl,
            "responses": ft_responses
        }

    def run_validation(self):
        """Run complete validation suite"""
        start_time = time.time()
        
        # Load test data
        self.print_section("Loading Test Data")
        print(f"Loading test data from: {TEST_DATA}")
        
        test_dataset = load_dataset("json", data_files=TEST_DATA, split="train")
        print(f"Loaded {len(test_dataset)} test samples")
        
        # Evaluation prompts for anxiety specialist
        eval_prompts = [
            "I'm having panic attacks before exams. What are 3 CBT techniques I can use right now?",
            "I avoid social events because I fear judgment. Can you give me a step-by-step exposure plan?",
            "My anxiety keeps me awake at night with racing thoughts. What can I do?",
            "I feel overwhelmed at work and can't focus. How can I manage this anxiety?",
            "I'm having relationship anxiety after a fight with my partner. How should I approach this?",
            "I'm terrified of public speaking. Can you help me prepare using CBT methods?",
            "I worry constantly about things I can't control. How do I break this pattern?",
            "I feel anxious in crowded places like trains. What grounding techniques can help?"
        ]
        
        print(f"Using {len(eval_prompts)} evaluation prompts")
        
        # Evaluate base model
        base_results = self.evaluate_base_model(test_dataset, eval_prompts)
        
        # Evaluate fine-tuned model  
        ft_results = self.evaluate_finetuned_model(test_dataset, eval_prompts)
        
        # Save results
        self.save_results(base_results, ft_results, eval_prompts, start_time)

    def save_results(self, base_results, ft_results, eval_prompts, start_time):
        """Save validation results"""
        self.print_section("Saving Results")
        
        # Metrics comparison
        metrics = {
            "base_model": {
                "loss": base_results["loss"],
                "perplexity": base_results["perplexity"]
            },
            "finetuned_model": {
                "loss": ft_results["loss"], 
                "perplexity": ft_results["perplexity"]
            },
            "improvement": {
                "loss_delta": base_results["loss"] - ft_results["loss"],
                "perplexity_ratio": base_results["perplexity"] / ft_results["perplexity"]
            },
            "validation_time_seconds": time.time() - start_time
        }
        
        # Side-by-side comparisons
        comparisons = []
        for i, prompt in enumerate(eval_prompts):
            comparisons.append({
                "prompt": prompt,
                "base_response": base_results["responses"][i],
                "finetuned_response": ft_results["responses"][i]
            })
        
        # Save files
        with open(f"{OUTPUT_DIR}/metrics.json", "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
        
        with open(f"{OUTPUT_DIR}/comparisons.jsonl", "w", encoding="utf-8") as f:
            for comp in comparisons:
                f.write(json.dumps(comp, ensure_ascii=False) + "\n")
        
        # Print summary
        print(f"📊 VALIDATION RESULTS SUMMARY")
        print(f"{'='*50}")
        print(f"Base Model Perplexity:        {base_results['perplexity']:.2f}")
        print(f"Fine-tuned Model Perplexity:  {ft_results['perplexity']:.2f}")
        print(f"Improvement Ratio:            {metrics['improvement']['perplexity_ratio']:.2f}x")
        print(f"Loss Improvement:             {metrics['improvement']['loss_delta']:.4f}")
        print(f"")
        print(f"Results saved to: {OUTPUT_DIR}/")
        print(f"  - metrics.json: Quantitative results")
        print(f"  - comparisons.jsonl: Side-by-side responses")
        print(f"")
        print(f"⏱️ Validation completed in {metrics['validation_time_seconds']:.1f} seconds")
        
        # Quick quality check
        if ft_results['perplexity'] < base_results['perplexity']:
            print("✅ Fine-tuning SUCCESS: Lower perplexity indicates better fit to anxiety counseling data")
        else:
            print("⚠️  Fine-tuning CONCERN: Higher perplexity may indicate overfitting or data issues")

if __name__ == "__main__":
    validator = ValidationSuite()
    validator.run_validation()
