## ReferenceRepo

### MathInstruct

* Github：[Fine-tuning Llama-3 on MathInstruct](https://github.com/togethercomputer/finetuning)
* 数据集：[Math Instruct dataset](https://huggingface.co/datasets/TIGER-Lab/MathInstruct) 
* 代码架构
  * Promt: 系统prompt + userQuestion + modelAnswer
  * finetune：Together库上传数据文件，启动finetune任务
  * eval
    * Together异步进行多模型的infer，得到多模型输出
    * Lllma3-70B作为评估模型，传入两个输入，输出为Accurate或Inaccurate

* TogetherAI
  * f4fd3c3dffa234e7e7b5674219f9b8994a2decb1ac3bd2633419c637ebbf6e03

### Llama-GSM8k

* [How to Use Llama 3 Instruct on Hugging Face](https://medium.com/@sewoong.lee/how-to-use-llama-3-instruct-on-hugging-face-5cc8409c4ab7)

* [How to Reproduce Llama-3's Performance on GSM-8k](https://medium.com/@sewoong.lee/how-to-reproduce-llama-3s-performance-on-gsm-8k-e0dce7fe9926)

* [Unsloth Tutorial: Llama 1B-3B](https://colab.research.google.com/drive/1T5-zKWM_5OD21QHwXHiV9ixTRR7k3iB9?usp=sharing#scrollTo=gGFzmplrEy9I)

  

## ToDo

* 训练框架 241130

  - [ ] 加载3B和8B预训练模型，计算数学数据集准确率 
  
    > [Kaggle: Test Llama3 with some math questions](https://www.kaggle.com/code/gpreda/test-llama3-with-some-math-questions)
  
    - [x] 学习相关教程｜16:15-16:50 + 18:40-20:00
  
    - [x] 配置autodl环境｜21:10-22:00
  
      > `pip install xformers`
  
  - [x] 跑通训练｜22:00-23:00
  
  - [ ] 排查测试慢的原因｜00:20-02:30
  
    > [HF-国内镜像](https://hf-mirror.com/)
    >
    > 用4090快很多，但还有两个问题
    >
    > 1. autodl不能联网
    > 2. infer的结果不能准确按照指令生成（不知道是3b的问题还是..)
  
* LLama3 + LoRA微调教程

  > [仅LoRA教程](https://www.mercity.ai/blog)