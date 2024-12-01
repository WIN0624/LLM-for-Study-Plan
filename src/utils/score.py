import os
import random
from tqdm import tqdm


def nshot_chats(nshot_data: list, n: int, question: str) -> dict:
    def question_prompt(s):
        return f"Question: {s}"

    def answer_prompt(s):
        return f"Answer: {s}"

    chats = []

    random.seed(42)
    for qna in random.sample(nshot_data, n):
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


def get_response(chats, generator):
    gen_text = generator(chats)[0]  # First return sequence
    return gen_text["generated_text"][-1]["content"]


def calc_accuracy(train_data, test_data, generator, n_shot):
    if not os.path.exists("log"):
        os.makedirs("log")

    log_file_path = "log/errors.txt"
    with open(log_file_path, "w") as log_file:
        log_file.write("")

    total = correct = 0
    for qna in tqdm(test_data):
        messages = nshot_chats(
            nshot_data=train_data, n=n_shot, question=qna["question"]
        )
        response = get_response(messages)

        pred_ans = extract_ans_from_response(response)
        true_ans = extract_ans_from_response(qna["answer"])

        total += 1
        if pred_ans != true_ans:
            with open(log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"{messages}\n\n")
                log_file.write(f"Response: {response}\n\n")
                log_file.write(f"Ground Truth: {qna['answer']}\n\n")
                log_file.write(f"Current Accuracy: {correct/total:.3f}\n\n")
                log_file.write("\n\n")
        else:
            correct += 1

    print(f"Total Accuracy: {correct/total:.3f}")


def pair_question_answer(example):
    return {"qa_pair": (example["question"], example["answer"])}


if __name__ == "__main__":
    
