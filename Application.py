from zhipuai import ZhipuAI
import keyboard
import time

class Application:

    #LLM Settings
    apiKey=""
    modelName=""
    prompt=""
    role=""
    #Memory Recording
    recording = []
    #Application Parameter
    isRunning=False
    client = None

    def __init__(self,apiKey,modelName,role,prompt):
        self.apiKey = apiKey
        self.modelName = modelName
        self.role = role
        self.prompt = prompt
        self.isRunning = False
        self.recording = []
        self.client = ZhipuAI(api_key=self.apiKey)

    def stop_run(self,event):
        print("Exit Application")
        self.isRunning = False

    def run(self):
        if self.client is None:
            print("创建对话失败")
            return

        self.recording.append({"role":"system","content":self.prompt})

        self.isRunning = True
        #注册退出应用的监听事件
        keyboard.on_press_key('esc', self.stop_run)

        #应用循环
        while self.isRunning:
            userInput = input("请输入内容：")

            if userInput.lower() == "退出" or userInput.lower() == "再见" or userInput.lower() == "拜拜" or userInput.lower() == "exit" :
                self.isRunning = False

            self.recording.append({"role":"user","content":userInput})

            response = self.client.chat.completions.create(
                model=self.modelName,
                messages=self.recording,
                top_p=0.7,
                temperature=0.95,
                max_tokens=4095,
                stream=True,
            )
            agentResponse = ""
            for res in response:
                agentResponse += (res.choices[0].delta.content)

            self.recording.append({"role":self.role,"content":agentResponse})

            print(agentResponse)

        print("程序已退出。")