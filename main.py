from langchain.memory import ConversationBufferMemory
import streamlit as st
from utils import get_chat_response

st.title("💭克隆ChatGPT")

with st.sidebar:
    api_key = st.text_input("请输入DeeepSeek API密钥", type="password")
    st.markdown("[获取DeepSeek API密钥](https://platform.deepseek.com/api_keys)")

    # 清除聊天记录按钮
    # 第一步：点击按钮，进入确认状态
    if st.button("🗑 清除聊天记录"):
        st.session_state["confirm_clear"] = True

    # 第二步：确认提示
    if st.session_state.get("confirm_clear", False):
        st.warning("⚠️ 确定要清除所有聊天记录吗？此操作不可恢复。")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 确认清除"):
                st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
                st.session_state["messages"] = [{"role":"ai", "content":"你好，我是AI助手，有什么可以帮助你的吗？"}]
                st.session_state["confirm_clear"] = False
                st.rerun()
        with col2:
            if st.button("❌ 取消"):
                st.session_state["confirm_clear"] = False
                st.rerun()


# memory需要存入会话状态中，不然每次刷新页面memory都会被重置。
# 会话状态中存入信息，用于后续刷新页面时，仍然可以显示之前的对话消息。
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role":"ai", "content":"你好，我是AI助手，有什么可以帮助你的吗？"}]

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])
    
    #或者使用下面的方法，效果是一样的
    # st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    if not api_key:
        st.info("请输入DeepSeek API密钥")
        st.stop()

    # 将用户的输入储存到会话状态中，并展示在界面上
    st.session_state["messages"].append({"role":"human", "content":prompt})
    # 展示用户的输入
    st.chat_message("human").write(prompt)

    # 添加加载组件
    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(prompt, st.session_state["memory"], api_key)

    # 将AI的回复储存到会话状态中，并展示在界面上
    st.session_state["messages"].append({"role":"ai", "content":response})
    # 展示AI的回复
    st.chat_message("ai").write(response)


        
