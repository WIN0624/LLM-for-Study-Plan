from trl import SFTTrainer
from transformers import TrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset

from unsloth import is_bfloat16_supported
from unsloth.chat_templates import get_chat_template
from unsloth.chat_templates import train_on_responses_only

from models.generator import model_generator
from utils.formatter import formatting_prompts_func

max_steps = 2000
learning_rate = 2e-4
lora_model_name = f"lora_model_steps{max_steps}_lr{learning_rate:.0e}"

model_name = "unsloth/Llama-3.2-3B-Instruct"
max_seq_length = 2048

# get model
model, tokenizer = model_generator(model_name, max_seq_length)

tokenizer = get_chat_template(
    tokenizer,
    chat_template="llama-3.1",
)

# get dataset
dataset = load_dataset("openai/gsm8k", "main", split="train")
dataset = dataset.map(lambda example: formatting_prompts_func(example, tokenizer))

# get trainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer),
    dataset_num_proc=2,
    packing=False,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=max_steps,
        learning_rate=learning_rate,
        fp16=not is_bfloat16_supported(),
        bf16=is_bfloat16_supported(),
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="outputs",
        report_to="none",
    ),
)

trainer = train_on_responses_only(
    trainer,
    instruction_part="<|start_header_id|>user<|end_header_id|>\n\n",
    response_part="<|start_header_id|>assistant<|end_header_id|>\n\n",
)

trainer_stats = trainer.train()

# save
model.save_pretrained(lora_model_name)
tokenizer.save_pretrained(lora_model_name)
