from unsloth import FastLanguageModel
from models.generator import model_generator

from utils.formatter import *
from unsloth.chat_templates import get_chat_template
from prompts.prompts import *
import openai
import os

## set OPENAI_API_KEY env variable before executing

model_name = "unsloth/Llama-3.2-3B-Instruct"

selected_prompts = student_prompts

raw_system_prompt = (
    selected_prompts["task_prompt"]
    + system_prompt
    + selected_prompts["evaluation_prompt"]
)
partial_system_prompt = selected_prompts["task_prompt"] + system_prompt


user_prompt = "Can you generate a study plan for me? I am taking Calculus 1 this semester and struggling with integration, particularly u-substitution."

raw_input_chat = [
    {"role": "system", "content": raw_system_prompt},
    {"role": "user", "content": user_prompt},
]

partial_input_chat = [
    {"role": "system", "content": raw_system_prompt},
    {"role": "user", "content": user_prompt},
]

# init model
model, tokenizer = model_generator(model_name)

tokenizer = get_chat_template(
    tokenizer,
    # chat_template="llama-3.1",
)

FastLanguageModel.for_inference(model)


# get inference response
raw_inference_response = get_response(model, tokenizer, raw_input_chat, generation=True)
partial_inference_response = get_response(
    model, tokenizer, partial_input_chat, generation=True
)

print("============== RAW RESPONSE  ==============")
print(raw_inference_response)
print("============== /RAW RESPONSE ==============")

print("============== PARTIAL RESPONSE  ==============")
print(partial_inference_response)
print("============== /PARTIAL RESPONSE ==============")

# setup openai client
openai_client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

response_pair = f"Response 1:\n{raw_inference_response}\n\n\nResponse 2:\n{partial_inference_response}"

# get scoring from chatgpt
resp = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": compare_prompt},
        {"role": "user", "content": response_pair},
    ],
)

resp = resp.choices[0].message.content

print("============== COMPARISON  ==============")
print(resp)
print("============== /COMPARISON ==============")
