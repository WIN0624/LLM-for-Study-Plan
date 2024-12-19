import time
from tqdm import tqdm
from datasets import load_dataset
from unsloth import FastLanguageModel

from models.generator import model_generator
from utils.formatter import *

baselines = [
    "./lora_model_steps2000_lr2e-04",
    "./lora_model_steps7000_lr2e-04",
    "unsloth/Meta-Llama-3.1-8B",
    "unsloth/Llama-3.2-3B-Instruct",
    "unsloth/Llama-3.2-1B-Instruct",
]

# load data
ds = load_dataset("openai/gsm8k", "main")
samples = ds["train"]
test_data = ds["test"]
test_data = test_data.take(200)

# test accuracy for different models
acc_data = []

for model_name in baselines:
    print(f"Testing {model_name}")
    start_time = time.perf_counter()
    if "lora_model" in model_name:
        model, tokenizer = model_generator(model_name, 2048, True)
    else:
        model, tokenizer = model_generator(model_name)

    FastLanguageModel.for_inference(model)  # Enable native 2x faster inference

    total = correct = 0
    for item in tqdm(test_data):
        messages = nshot_chats(nshot_data=samples, n=2, question=item["question"])
        response = get_response(model, tokenizer, messages)
        # print("============== QUESTION ==============")
        # print(item["question"])
        # print("============== ANSWER ==============")
        # print(item["answer"])
        # print("============== RESPONSE ==============")
        # print(response)

        pred_ans = extract_ans_from_response(response)
        true_ans = extract_ans_from_response(item["answer"])

        # print("============== EXTRACT_ANS ==============")
        # print(f"pred_ans: {pred_ans}")
        # print(f"true_ans: {true_ans}")

        total += 1
        if pred_ans == true_ans:
            correct += 1

    accuracy = f"{correct/total:.3f}"
    acc_data.append([model_name, accuracy])
    print(f"============== Testing {model_name} ============== ")
    print(f"Total Accuracy: {accuracy}")
    print(f"Duration: {time.perf_counter() - start_time}")
