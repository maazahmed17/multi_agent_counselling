import torch
# We now need to import BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

print("Attempting to load the Llama Guard model...")

model_id = "meta-llama/Meta-Llama-3.1-8b-Instruct"
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