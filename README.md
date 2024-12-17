# LLM-for-Study-Plan

* **<u>Framwork</u>**：Torch

* **<u>Library</u>**

  * Unsloth
  * Huggingface-Transformers
  * SFTTrainer

* **<u>ComputationResources</u>**

  * HPC；Autodl

* **<u>Components</u>**

  * DatasetPreprocessing => DataSetDownload
    * 3 Task
  * Model => Freezing Most, Reset some 
    * ModelChoice：Which model? Which layer's weights to be trained?
    * FinetuningTricks：Only hyperpara or add Layers?
    * Loss：What loss？
    * TrainingWay：Multi-object/Multi-task
  * Metrics => Precison, Recall

* **<u>Technical</u>** 

  * Joint Learning?

* **<u>Difficulty</u>**

  * computation resources
  * training speed

* **<u>Application</u>**

  * For presentation： different scenario => based on chatbot

    * P0
      * solve math problems
      * generate a study plan (grade, weakeness domain)
    * P1
      * input error set (answer question + analyze weakness + generate plan)

  * For report

    * compare with baseline

      * Math QA => public dataset

      * Concept Extracting => self-customed dataset + model-labeld dataset (train/test)

        > How many data are required

* **<u>STEPS|MileStones</u>**

  * **Model Construction**

    * Find public github repo + adapt to our tasks(data processing)

      > REF: [Github](https://github.com/togethercomputer/finetuning)
      >
      > [GPT-4 Finetuned](https://github.com/liutiedong/goat)
      >
      > Math-Finetuning Github with metrics
      >
      > Finetuning Lllama3 8B Github

    * Llam3 3B/8B + Lora

      > 8B: 14GB, 16bit  
      >
      > 3B: 4bit
      > [Tutorial](https://github.com/amitlevy/finetune_llama_3_own_data/blob/master/llama3_8b_finetune_own_data.ipynb)

    * Finetune on Math dataset

    * Hyperpara: lr

    * Resources

      > VastAi, 1 4090 =>  1 24GB, 0.35

    * **Checkpoint**

      * **Accuaray Metrics for this two, accuracy/solveRate**

        > Rule-base extraction
        >
        > ChatGpt extraction

      * **Training Framwork**

  * **PromptEngineering**

    * target: find best prompt to solve question

      > Metrics |  How do people measures prompt improvements
      >
      > refer COT, still accuracy
      >
      > refer ROSCOE => evaluate reasoning
      >
      > refer Confidence of Hallucination => study plan (confidence higher than baseline)

    * only prompt

    * prompt + sft

    * **Checkpoint**

      * Inference Framwork
      * Reasoning Metrics

  * **PresentationWay**

    * Quantize + Deploy on phone
    * Comparison: Quantized Version

  * **Serving**

    * Ollama 