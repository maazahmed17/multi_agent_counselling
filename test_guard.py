# The fully corrected, modern version of test_guard.py

import torch
# We now need to import BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

print("Attempting to load the Llama Guard model...")

model_id = "meta-llama/Meta-Llama-Guard-2-8B"
device = "cuda"
dtype = torch.bfloat16

# 1. Create a quantization configuration object
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=dtype,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

try:
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # 2. Pass the config object to the 'quantization_config' argument
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=quantization_config,
        device_map=device,
    )

    print("\n✅ Success! Llama Guard model and tokenizer are loaded onto your GPU.")
    print(f"   - Model is on device: {model.device}")
    print(f"   - Model memory footprint: {model.get_memory_footprint() / 1e9:.2f} GB")

except Exception as e:
    print(f"\n❌ An error occurred: {e}")


    
#output: 
# #(ai_env) maaz@LAPTOP-I4IUGLCS:~/companionAI$ python test_guard.py
# Attempting to load the Llama Guard model...
# Loading checkpoint shards: 100%|| 4/4 [00:23<00:00,  5.80s/it]

# ✅ Success! Llama Guard model and tokenizer are loaded onto your GPU.
#    - Model is on device: cuda:0
#    - Model memory footprint: 5.59 GB