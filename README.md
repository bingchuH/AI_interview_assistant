# AI面试助手使用文档

---

## 项目概述

AI面试助手，用于在面试中实时生成AI驱动的面试问题和回答。该项目使用Azure的语音识别服务与GPT模型。
在windows下运行，别的操作系统没有测试过！

## 文件结构

```
project_root/
│
├── main.py                       # 项目的主入口，负责启动应用程序
├── requirements.txt              # 项目依赖
├── README.md                     # 使用文档（即此文档）
├── src/                          # 源代码目录
│   ├── gpt_interaction.py        # 负责与Azure OpenAI服务交互，生成GPT响应
│   ├── stt.py                    # 语音识别模块，使用Azure的语音服务
│   └── transparent_log_window.py # 透明日志窗口模块，显示识别的文本
```

## 使用说明
1. **配置Azure**

   微软Azure还是很良心的，注册送200美元额度，期限一个月。认证学生身份送100美元，够用很久了。  
   这里主要用到的就是Azure提供的OpenAI服务和语音转文本（stt）服务。  

   [参考教程](https://blog.csdn.net/m0_71858447/article/details/135656444)  
   [Azure工作台](https://portal.azure.com/#home)  
   [Azure stt 文档](https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/speech-to-text)  

2. **配置环境变量**  

   记得是在同一个订阅组内创建OpenAI和stt服务，这样两个服务的ENDPOINT是一样的，如果分开创建运行代码会报错。
   
   AZURE_OPENAI_API_KEY  
   AZURE_OPENAI_ENDPOINT （一串url）  
   SPEECH_KEY  
   SPEECH_REGION （仅地区，如eastus、eastasia）  
   
4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

5. **启动应用**

   在终端中运行以下命令启动AI面试助手：

   ```bash
   python main.py
   ```

   该命令将启动语音识别服务，并弹出一个透明窗口来显示识别的语音文本。

6. **与AI助手交互**

   - **重置文本**: 按下`空格键`可重置当前识别的文本。
   - **提交并生成响应**: 按下`回车键`将当前识别的文本发送给GPT模型，并获取AI的响应。
   - **退出程序**: 按下`Esc键`可退出识别。

## 代码详解

### main.py

这是项目的主入口，主要负责启动语音识别和UI窗口。

### gpt_interaction.py

该模块负责与Azure OpenAI服务交互，通过GPT模型生成基于用户语音输入的响应。主要功能包括管理对话历史记录并生成上下文相关的AI回复。
一些prompt也放在里面了。

### stt.py

此模块使用Azure的语音识别服务，将用户的语音转换为文本，并在检测到句子结束时进行处理。

### transparent_log_window.py

这个模块实现了一个透明的日志窗口，用于实时显示识别的文本内容。通过Tkinter库实现简单的UI。
