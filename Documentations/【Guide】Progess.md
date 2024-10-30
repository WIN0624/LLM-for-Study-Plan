## Period1: Offline Training

* **<u>Framwork</u>**：Torch

* **<u>ComputationResources</u>**：HPC；Autodl

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

  * What library? 
    * Langchain?
  * Joint Learning?

* **<u>Difficulty</u>**

  * computation resources
  * training speed

* **<u>ToDo</u>**

  * Learn trendy library + Write model skeleton + NewDataset => 11.11 [2pm]

    > optional: PreprocessingWay

  * Finish whole framework + Start training => 11.15

  * Rest Presentation Process

  * Set Experiments：Research SLMs/JointLearning/Finetuning