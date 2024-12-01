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

    return {
        "text": texts,
    }


def nshot_chats(nshot_data, n: int, question: str):
    chats = []

    shuffled_dataset = nshot_data.shuffle(seed=42)

    for i in range(n):
        qna = shuffled_dataset[i]
        chats.append({"role": "user", "content": question_prompt(qna["question"])})
        chats.append({"role": "assistant", "content": answer_prompt(qna["answer"])})

    chats.append(
        {
            "role": "user",
            "content": question_prompt(question)
            + " Let's think step by step. At the end, you MUST write the answer as an integer after '####'.",
        }
    )

    return chats


def extract_ans_from_response(answer: str, eos=None):
    if eos:
        answer = answer.split(eos)[0].strip()

    answer = answer.split("####")[-1].strip()

    for remove_char in [",", "$", "%", "g"]:
        answer = answer.replace(remove_char, "")

    try:
        return int(answer)
    except ValueError:
        return answer


def get_response(model, tokenizer, message):
    inputs = tokenizer.apply_chat_template(
        message,
        tokenize=True,
        add_generation_prompt=False,  # Must add for generation
        return_tensors="pt",
    ).to("cuda")

    outputs = model.generate(
        input_ids=inputs, max_new_tokens=100, use_cache=True, temperature=1.5, min_p=0.1
    )

    return tokenizer.batch_decode(outputs)[0]