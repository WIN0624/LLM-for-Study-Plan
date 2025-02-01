## 难点

* 如何评估学习计划好坏
  * LLM-as-a-Judge

## 初稿

* 细化LLM在问题解决方面的应用，只要找对细分领域，总有人没有涉足过

* **<u>Chain-of-thoughts</u>**

  - Write prompt LLM talk to themselves => logical problems
  - It is shown to the users, final outputs (behind the scene)

* **<u>Low-power device</u>**

  - Small size model on phone

* **<u>RAG</u>**

  - database of knowledge => attach 

* **<u>All in Once</u>**

  - Multiple models/stages => Agents

* **<u>Applications</u>**

  - **IMPACT**: how can we help children with limited resources? In interactive way, answering questions

    > Even no internet

  - **Idea**

    - 01-Most important function: Build a study plan into manageable parts (personalized?)

      > Multi-disciplined? Too much information❌ RAG (practical problems: latency + storage)
      >
      > Hardest discipline to form a study plan? ~~Foreign language~~ Math/STEM/Foreign Language(Lack of exposure and application, not effective => audio chatting, Chatgpt not that good at Foreign Language as English) 

    - 02-Quantization? Qlora? => Existing models to fit small devices

  - **Demo | Function**

    - Function: Visualized Study Plan

      - Prompt: Displine and grade? Do you have specific difficuties? Focus Requirements?

      - Input: Natural language describing discipline and grade

        > Do we need dataset? Find a Math LLM, then don't. (Step1)
        >
        > (step2. Combine RAG)
        >
        > What database do we use?  Open-source Dataset, otherwise need to crawl data/textbook
        >
        > Copy-right laws? [ToDo]

      - Output Formats

        - visulized general study plan
        - specific study plan 
        - (optional) breakdown steps on specific focus (guidance)

    - Methods

      - 1. Fine-tuning to get a better performance on Math discipline => Existing models
      - 2. Agents?

    - Metrics: How to evaluate improvement? [ToDo]

    - Interface Framework: Gradio

  - **Plan**
    - step1. Research More | 10.25
      - how prior studies design study plan (Methods, Dataset, Metrics)

    - step2. Technial Details| 11.1[TBD]

      - Training
        - Dataset Preprocess? Data Scale (Big data tools needed) ?
        - Which model? LLama, 7B? Loss/Optimizer? => What's the target for this model?
        - What platform/framework/library? Huggingface, Langchain? Olama? Llama.cpp => Torch based
        - Training speed? Distributed?
        - Resources? HPC? Vast.ai (cheaper, `H100 $2/hour, A100 $1.25/hour`); AWS (A100 $3/hour)
      - Depolyment
        - How to deploy LLM?

    - step3. Development 

      - Training/Testing/Evaluation | 11.15

        > How to collaborate [ToDo]
        >
        > Foundation: General functions
        >
        > Rules: work on different branch

      - Refinement/Tuning | 11.26 (2 weeks)

        > Share params on HPC

      - Serving framwork; Interface

  - **<u>Suggestions?</u>**

* **<u>Collaboration</u>**

  * How to write proposal: Write bullets/simple sentances for each sections | 10.23
  * How to write codes: 