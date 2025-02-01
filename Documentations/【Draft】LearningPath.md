## Structure

* 整体控制在3-4页，结合图表和流程图

* <思考> 推荐系统专注于用户时长，学习系统的指标是什么，如何跟学生共同成长 => 学生是不断变化的

* **<u>Project Overview</u>**

  * 2-3 paras

  * What problems: new or existing (LLM在新领域落地) ? 

    * GenAI produce learning path with explanations. Not only list the contents and tags, but how each LO is related.
    * Aim to tailor learning experiences to the individual needs, preferences, and prior knowledge of learners. 
    * Enhance learning efficiency by providing customized study plan that adapt to unique learning pace.
    * Not only deeper understanding but also increase learner engagement
    * 研究要点：怎么提高诊断准确率？怎么减少冗余的诊断问题？

    ```shell
    # 重要性定义
    Michael Feldstein and Phil Hill.Personalized learning: What it really is and why it really matters.Educause review, 51(2):24–35, 2016.
    
    # draft
    Personalized Learning has emerged as a critical field of educational study, aiming to tailor learning experiences to meet learners' goals, preferences and prior knowlege. In contrast to the one-size-fits-all model of traditional education, personalized learning enhances learning efficiency by adapting different learning pace through customized study plan.
    
    Traditional approaches to generating personalized learning paths rely on rule-based cognitive diagnosis and require delicate annotations(Kuo et al., 2023). With the few-shot learning capability of Large Language models, personalized study plans can be generated more easily with minimul annotations. Futhermore, the logical reasoning abilities of Large Language models enable them to provide adaptive explanations for each recommendation step in the study plan, making it more understandable for teenage students.
    ```

  * Why LLM?

    * 早期只能识别文本关键字，无法对学生描述进行逻辑推理，判断当前难点

    * Former text generation is based on given templates, which maybe hard to understand.

    * Focus on similarities, lack of the ability on reasoning. Logic reasoning is required.

    * Few-shot learning ability. Traditional models requires delicate annotations or large scaled preference record.

      > Learn an effective predictor with limited annotations

    * Powerful Prior Knowledge

    * generate adaptive learning context and personalized feedback by incorporating learning-specific information into the prompts

    ```shell
    # 待定
    学生历史学习数据有限，且处于隐私保护不好利用，LLM可以通过角色模拟生成大量训练数据
    ```

* **<u>Project Objectives and Contributions</u>**

  * 1-2 paras

  * Main objectives and novel ideas/contributions

    * Domain-specific + smaller

  * How differ from existing solutions?

    * Smaller Lanaguage Models, benefits to limited resources students 

      > The method can be reuse on other subjects.
      >
      > Don't need to load everthing at once.
      >
      > Keep subject knowledge

    * Error set.

  ```shell
  Recent research has proved that Large Language Models (LLMs) have the ability to produce more explaianable and understandable learning paths in an interactive way, which improves learners performance and engagement. However, few studies have highlighted the difficuty students with Internet of Things (IoT) edge devices face in accessing Large Language Models. To promote educational equity, our project explores to introduce a domain-specific, smaller language models (SLMs) that can be deployed on smartphones while retaining most of the capacity to identify students' primary learning challenges and generate personalized study plans.
  ```

* **<u>Literature Review</u>**

  * 3-4 paras
  * How do existing literature address similar problems
    * Utilize knowledge graph as source of context information and with domain experts in the loop to reduce hullucination. LLM give explanations under a designed textual template.
    * Harness the power of LLMs by introducing cognitive model, item model and interative procedures, which increase the accuracy on locating individual's learning weakness by providing less but precise questions. This approach provides scaffolding approach during remidiation, enhancing the adpative mechanism of TALP platform.
    * Designs prompt into initial assessment, clarification prompt and explanatory prompt to incoporate learner-specific information to generate personlized and coherent learning path.
    * ToDo
      * Math Performance Finetuning (LLama 8B, outperform GPT-4)
      * Quantization: Small Large Language Models
  * Why are existing approaches insufficient to fully address
  * Cite 5-7 papers, explaining approaches and limitations

* **<u>Methodology</u>**

  * 3-4 paras

  * Key components

    * **step1. Finetune Llama 8B**

      * on MathDataset (loss=NumberTokensAccuracy)

      * on ReasoningDataset (loss=Rouge-L)

      * on ConceptDataset (loss=Rouge-L)

      * Get metrics on different dataset and compared to baseline

        > Baseline: Gpt-4, Unfinetuned Llama

    * **step1.5 Solve SLMs problems**

    * **step2. Prompt Engineering + Deployment** => Prototype

      * List biggest difficulties
      * List relevant concepts
      * List study plan with explanations

    ```latex
    \subsection{Finetune SLMs with Math Dataset}\label{AA}
    To generate a personalized study plan, the model needs to demonstrate the ability in: a) problem-solving to assess whether students can perform correctly on certain topics; b) math reasoning to evaluate whether students accurately deduce and arrive at solutions. c) concept-relating to identify students' biggest difficulties based on their provided error sets. 
    
    To achieve these abilities, two datasets will be used to fine-tune smaller language models:
    \begin{itemize}
    \item For problem-solving and reasoning skill, the MATH Dataset, which contains 12,500 challenging competition mathematics problems, will be used. A joint task focusing on on producing the correct output and generating step-by-step solutions will be created.
    @article{hendrycksmath2021,
      title={Measuring Mathematical Problem Solving With the MATH Dataset},
      author={Dan Hendrycks and Collin Burns and Saurav Kadavath and Akul Arora and Steven Basart and Eric Tang and Dawn Song and Jacob Steinhardt},
      journal={NeurIPS},
      year={2021}
    }
    \item For concept-relating skill, the Chasat-Algebra-Sub02 Dataset, which contains the relation between questions and corresponding concepts, will be utilized.
    [1] Manas Bansal, "Chasat-Algebra-Sub02 Dataset," Hugging Face, 2022. [Online]. Available: https://huggingface.co/datasets/themanas021/chasat-algebra-sub02. [Accessed: 25-Oct-2024].
    
    \subsection{Prompt Engineering and Smartphone Deployment}
    After the best-performing SLM model is fine-tuned, we will create a prototype where students can obtain a personalized math study plan by inputting specific error sets. The existing prompt engineering \cite{b4} for personalized study plan generation will be reused to integrate the student input and the fine-tuned model. The output would identify the biggest difficulties the student are facing, recomending the relevant concepts to learn and next-steps sequencing study plan.
    
    \subsection{Idea Validation}
    The finetuned SLM model would be tested on above-mentioned datasets. For Math Dataset, accuracy would be the main detectors. For the Chasat-Algebra-Sub02 Dataset, ROUGE-N metric would be used. The baseline model would be GPT-4 and unfinetuned LLama model.
    ```

    

  * How to validate ideas

    * MathDataset - QuestionSolving Ablity
    * ConceptLinking  - Locate Concept Correctly
    * [Quality] - Generation Quality (Coherent, Relevant => human blind test)

  * Data Requirements

    * [Math Dataset](https://github.com/hendrycks/math)
    * Concept Related

* **<u>Technical Considerations</u>**

  * 2-3 paras
  * Which LLM plan to use? Llama 8B, Llama 3B
  * Only APIs or fine-tuning? Fine-tuning
  * Resource Considerations
    * computationally feasible? how many GPU, how long can be used.
    * commercial APIs, what's the cost? 

* **<u>Timeline and Milestones</u>**

  * 1-2 paras

  * 4-6 major milestones and completion dates

  * **step1. Finetune Llama 8B**

    * on MathDataset (loss=NumberTokensAccuracy)

    * on ReasoningDataset (loss=Rouge-L)

    * on ConceptDataset (loss=Rouge-L)

    * Get metrics on different dataset and compared to baseline

      > Baseline: Gpt-4, Unfinetuned Llama

  * **step1.5 Solve SLMs problems**

  * **step2. Prompt Engineering + Deployment**

* **<u>Expected Outcome and Evaluation</u>**

  * 1-2 paras
  * Tangible results? prototype, comparison
  * Metrics or evalutation methods

* **<u>Potential Challenges and Mitigation Strategies</u>**

  * 3-4 challenges
  * Plan to mitigate these challenges
  * Finetuning-Resources Insufficient => Smaller Dataset + Commercial APIs
  * Forgetten Knowledge => Narrow + [ToDo]
  * Inability to cover Math knowledge and Study plan generation => Large but still can be deployed

* **<u>Conclusion</u>**

  * Summarize = Reiterate problems, approach, the potential impact

    

