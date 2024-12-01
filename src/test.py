from datasets import load_dataset
from unsloth import FastLanguageModel
from models.generator import model_generator

# load data
ds = load_dataset("openai/gsm8k", "main")
samples = ds["train"]
test_data = ds["test"]

# test accuracy for different models
baseline = [
    "unsloth/Meta-Llama-3.1-8B",
    "unsloth/Llama-3.2-3B-Instruct",
    "unsloth/Llama-3.2-1B-Instruct",
]
acc_data = []

for model_name in baseline:
    model, tokenizer = model_generator(model_name)
    model = FastLanguageModel.for_inference(model)
    
    outputs = model.generate(input_ids = inputs, max_new_tokens = 64, use_cache = True,
                            temperature = 1.5, min_p = 0.1)
    tokenizer.batch_decode(outputs)
    acc_data.append(model_name, accuracy)
