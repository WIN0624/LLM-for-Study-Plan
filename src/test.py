from datasets import load_dataset
from unsloth import FastLanguageModel
from models.generator import model_generator

from tqdm import tqdm
from unsloth.chat_templates import get_chat_template

from utils.formatter import *


baselines = [
    "./lora_model",
    "unsloth/Meta-Llama-3.1-8B",
    "unsloth/Llama-3.2-3B-Instruct",
    "unsloth/Llama-3.2-1B-Instruct",
]

# load data
ds = load_dataset("openai/gsm8k", "main")
samples = ds["train"]
test_data = ds["test"]

test_data = test_data.take(10)

# test accuracy for different models
acc_data = []

for model_name in baselines:
    if model_name == "lora_model":
        model, tokenizer = model_generator(model_name, 2048, True)
    else:
        model, tokenizer = model_generator(model_name)

    tokenizer = get_chat_template(
        tokenizer,
        # chat_template="llama-3.1",
    )

    FastLanguageModel.for_inference(model)  # Enable native 2x faster inference

    total = correct = 0
    for item in tqdm(test_data):
        print(item)

        messages = nshot_chats(nshot_data=samples, n=2, question=item["question"])
        response = get_response(model, tokenizer, messages, generation=True)

        print("============== RESPONSE ==============")
        print(response)
        print("============== /RESPONSE ==============")

        pred_ans = extract_ans_from_response(response, model=model, tokenizer=tokenizer)
        true_ans = extract_ans_from_response(item["answer"])

        total += 1
        if pred_ans == true_ans:
            correct += 1

    accuracy = f"{correct/total:.3f}"
    acc_data.append((model_name, accuracy))
    print(f"Accuracy ({model_name}): {accuracy}")
