from torch import wait
from unsloth import FastLanguageModel
from models.generator import model_generator

from utils.formatter import *
from generate.prompts import *

# load model
MODEL_NAME = "unsloth/Llama-3.2-3B-Instruct"
model, tokenizer = model_generator(MODEL_NAME)
FastLanguageModel.for_inference(model)
    
    
def initial_generate(task_eval_prompt, user_prompt):    
    prompts = {
        "RAW_SYSTEM_PROMPT": (
            task_eval_prompt["task_prompt"]
            + system_prompt
            + task_eval_prompt["evaluation_prompt"]
        ),
        "PARTIAL_PROMPT": (task_eval_prompt["task_prompt"] + system_prompt),
    }
    
    for prompt_name, prompt in prompts.items():
        input_chat = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_prompt},
        ]
        print(f"============== RESPONSE FOR {prompt_name} ==============")
        print(get_response(model, tokenizer, input_chat, generation=True))
        print("============== /RESPONSE ==============\n\n")


if __name__ == '__main__':
    # initial generation
    task_eval_prompt = initial_student_prompts
    user_prompt = "Can you generate a study plan for me? I am taking Calculus 1 this semester and struggling with integration, particularly u-substitution."
    initial_generate(task_eval_prompt, user_prompt)