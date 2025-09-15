from langchain.chains import ConversationChain
from langchain_deepseek import ChatDeepSeek
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")


# 定义对话函数。记忆由外部传入，如果内部初始化，模型还是没有记忆。
def get_chat_response(prompt, memory, api_key): 
    model = ChatDeepSeek(model="deepseek-chat", api_key=api_key)
    chain = ConversationChain(llm=model, memory=memory)
    
    response = chain.invoke({"input":prompt})
    return response["response"]

# memory = ConversationBufferMemory(return_messages=True)

# print(get_chat_response("你好", memory=memory, api_key=api_key))

# print(get_chat_response("我上一个问题问的是啥？", memory=memory, api_key=api_key))