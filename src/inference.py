from torch import wait
from unsloth import FastLanguageModel
from models.generator import model_generator

from utils.formatter import *
from unsloth.chat_templates import get_chat_template
from prompts import *

baselines = [
    "unsloth/Llama-3.2-3B-Instruct",
]

selected_prompts = student_prompts

raw_system_prompt = (
    selected_prompts["task_prompt"]
    + system_prompt
    + selected_prompts["evaluation_prompt"]
)
partial_system_prompt = selected_prompts["task_prompt"] + system_prompt


selected_system_prompt = raw_system_prompt

user_prompt = (
    "Can you generate a study plan for me? I am taking Calculus 1 this semester and struggling with integration, particularly u-substitution."
    # "Can you generate a study plan for me? I am taking Algebra 1 this semester and struggling with determining the equation of a line given a graph."
    # "Can you generate a plan for a lecture I will be teaching? I will be teaching a Geometry course next semester. What should I cover in the lecture introducing lines and angles and the relationships between them?"
)

input_chat = [
    {"role": "system", "content": selected_system_prompt},
    {"role": "user", "content": user_prompt},
]


for model_name in baselines:
    if model_name == "lora_model":
        model, tokenizer = model_generator(model_name, 2048, True)
    else:
        model, tokenizer = model_generator(model_name)

    tokenizer = get_chat_template(
        tokenizer,
        # chat_template="llama-3.1",
    )

    FastLanguageModel.for_inference(model)

    response = get_response(model, tokenizer, input_chat, generation=True)

    print(f"============== RESPONSE  ({model_name}) ==============")
    print(response)
    print(f"============== /RESPONSE ({model_name}) ==============")
