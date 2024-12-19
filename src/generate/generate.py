import os
import openai
from torch import wait
from unsloth import FastLanguageModel
from models.generator import model_generator

from utils.formatter import *
from generate.prompts import *

# load model
MODEL_NAME = "unsloth/Llama-3.2-3B-Instruct"
model, tokenizer = model_generator(MODEL_NAME)
FastLanguageModel.for_inference(model)

# setup openai client
openai_client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def generate(task_eval_prompt, user_prompt):
    whole_task_prompt = (
        task_eval_prompt["task_prompt"]
        + system_prompt
        + task_eval_prompt["evaluation_prompt"]
    )
    
    input_chat = [
        {"role": "system", "content": whole_task_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    resp = get_response(model, tokenizer, input_chat, generation=True)
    
    print(f"============== FINAL RESPONSE ==============")
    print(resp)
    print("============== /RESPONSE ==============")
    
    return resp
    
def score_response(user_prompt, resp, use_gpt=False):
    inference_qa_pair = f"Question:\n{user_prompt}\n\nAnswer:\n{resp}"

    messages = [
        {"role": "system", "content": score_prompt},
        {"role": "user", "content": inference_qa_pair},
    ]
    
    if use_gpt:
        resp = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
    else:
        resp = get_response(model, tokenizer, messages, generation=True)

    print(f"============== FINAL RESPONSE ==============")
    print(resp)
    print("============== /RESPONSE ==============")

    return resp


if __name__ == "__main__":
    # final generation
    task_eval_promt = finalized_student_prompts
    user_prompt = "Can you generate a study plan for me? I am taking Calculus 1 this semester and struggling with integration, particularly u-substitution."
    response = generate(task_eval_promt, user_prompt)

    # score the response
    score_response(user_prompt, response)