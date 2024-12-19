import torch
import re


def question_prompt(s):
    return f"Question: {s}"


def answer_prompt(s):
    return f"Answer: {s}"


def formatting_prompts_func(example, tokenizer):
    convo = [
        {"role": "user", "content": question_prompt(example["question"])},
        {"role": "assistant", "content": answer_prompt(example["answer"])},
    ]
    texts = tokenizer.apply_chat_template(
        convo, tokenize=False, add_generation_prompt=False
    )

    texts = texts + tokenizer.eos_token

    return {
        "text": texts,
    }

def nshot_chats_batch(batch, nshot_data, n):
    messages = []
    for question in batch['question']:
        message = nshot_chats(nshot_data, n, question)
        messages.append(message)
    
    return {
        'messages': messages
    }

def nshot_chats(nshot_data, n: int, question: str):
    chats = []

    shuffled_dataset = nshot_data.shuffle()

    chats.append(
        {
            "role": "system",
            "content": "In this task, you will be asked to solve and answer a question. "
            + "You should think step by step to solve the problem carefully, without skipping any steps or making mistakes. "
            + "You MUST write the final answer as an integer after '####' without any other symbols or text. "
            + "If you do not, the answer will not be valid and HORRIBLE things will happen.",
        }
    )

    for i in range(n):
        qna = shuffled_dataset[i]
        chats.append({"role": "user", "content": question_prompt(qna["question"])})
        chats.append({"role": "assistant", "content": answer_prompt(qna["answer"])})

    chats.append({"role": "user", "content": question_prompt(question)})

    return chats


def extract_ans_from_response(answer: str, eos=None, model=None, tokenizer=None):
    answer_parsed = re.search(r"####[\s]?(\d+)", answer)

    if answer_parsed:
        return int(answer_parsed.group(1))

    # failed to get answer
    return None


def extract_ans_from_response_fallback(answer: str, model, tokenizer):
    # extract answer from response with llm

    print("FALLBACK")

    chats = []

    chats.append(
        {
            "role": "system",
            "content": "Extract the final numeric answer from the response given below. "
            + "You MUST write your output as an integer prefaced by '####', without any other information. "
            + "Do NOT include ANY other symbols or text or explanation or formatting other than the specified prefix and the integer value. "
            + "E.g. '####42' is a valid answer",
        }
    )

    chats.append({"role": "user", "content": answer})

    response = get_response(model, tokenizer, chats)

    print("=================== FALLBACK =================")
    print(f"FALLBACK RESPONSE: {response}")
    print("=================== /FALLBACK =================")

    return extract_ans_from_response(response)


def get_response(model, tokenizer, message, full=False, generation=False):
    inputs = tokenizer.apply_chat_template(
        message,
        tokenize=True,
        padding=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to("cuda")


    outputs = model.generate(
        input_ids=inputs,
        max_new_tokens=1024,
        use_cache=True,
        temperature=0.01,
        min_p=0.1,
        pad_token_id=tokenizer.eos_token_id,
    )

    generated_tokens = outputs[:, len(inputs[0]) :]

    if full:
        return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
