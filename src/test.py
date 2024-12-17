import time
from tqdm import tqdm
from datasets import load_dataset
from unsloth import FastLanguageModel
from torch.utils.data import DataLoader

from utils.formatter import *
from models.generator import model_generator

baselines = [
    "unsloth/Meta-Llama-3.1-8B",
    "unsloth/Llama-3.2-3B-Instruct",
    "unsloth/Llama-3.2-1B-Instruct",
]

# load data
ds = load_dataset("openai/gsm8k", "main")
samples = ds["train"]
test_dataset = ds["test"]

test_data = test_dataset.take(16)
"""
test_data = test_dataset.take(8)
test_data.set_format(type="torch")
test_dataloader = DataLoader(test_data, batch_size=2)
for batch in test_dataloader:
    messages = nshot_chats_batch(batch, samples, 2)
    response = get_response(model, tokenizer, messages)
    pred_answers = [extract_ans_from_response(answer) for answer in response]
    true_answers = [extract_ans_from_response(answer) for answer in batch['answer']]
    for i in range(len(pred_answers)):
        total += 1
        if pred_answers[i] == true_answers[i]:
            correct += 1
"""

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
        messages = nshot_chats(nshot_data=samples, n=8, question=item["question"])
        response = get_response(model, tokenizer, messages)
        print("============== QUESTION ==============")
        print(item["question"])
        print("============== ANSWER ==============")
        print(item["answer"])
        print("============== RESPONSE ==============")
        print(response)

        pred_ans = extract_ans_from_response(response)
        true_ans = extract_ans_from_response(item["answer"])

        print("============== EXTRACT_ANS ==============")
        print(f"pred_ans: {pred_ans}")
        print(f"true_ans: {true_ans}")

        total += 1
        if pred_ans == true_ans:
            correct += 1

    accuracy = f"{correct/total:.3f}"
    acc_data.append([model_name, accuracy])
    print(f"Total Accuracy: {accuracy}")
    print(f"Duration: {time.perf_counter() - start_time}")
