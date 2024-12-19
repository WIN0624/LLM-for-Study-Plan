import os
import openai
## set OPENAI_API_KEY env variable before executing

from utils.formatter import *
from generate.prompts import *

# setup openai client
openai_client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def compare_generate(raw_output, output_with_evaluations):
    
    response_pair = f"Response 1:\n{raw_output}\n\n\nResponse 2:\n{output_with_evaluations}"

    resp = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": compare_prompt},
            {"role": "user", "content": response_pair},
        ],
    )
    print("============== EXTRA_EVALUATION  ==============")
    print(resp)
    print("============== /EXTRA_EVALUATION ==============\n\n")

def advice_generate(task_eval_prompt):
    resp = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": advice_prompt},
            {"role": "user", "content": task_eval_prompt["evaluation_prompt"]},
        ],
    )
    print("============== ADVICE_ON_INITIAL_PROMPT  ==============")
    print(resp)
    print("============== /ADVICE_ON_INITIAL_PROMPT ==============")


if __name__ == "__main__":
    # compare initial outputs. Due to length, omit outputs here
    raw_output = "...." 
    output_with_evaluations = "..."
    compare_generate(raw_output, output_with_evaluations)
    
    # get advice for each initial evaluation dimensions
    task_eval_prompt = initial_student_prompts
    advice_generate(task_eval_prompt)
