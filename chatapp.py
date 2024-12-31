import os
import streamlit as st

from langchain_openai import AzureChatOpenAI
# from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.callbacks import get_openai_callback

def init_page():
    st.set_page_config(
        page_title="My ChatGPT",
        page_icon="🤗"
    )
    st.header("My ChatGPT")
    st.sidebar.title("Options")

def init_messages():
    clear_button = st.sidebar.button("Clear conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="あなたは優秀なアシスタントです")
        ]
        st.session_state.costs = []

def select_model():
    model = st.sidebar.radio("モデルを選択してください：", ("GPT-4o-mini", "GPT-4o"))
    if model == "GPT-4o-mini":
        model_name = os.environ["AZURE_OPENAI_MODEL_4O_MINI"]
    else:
        model_name = os.environ["AZURE_OPENAI_MODEL_4O"]

    temperature = st.sidebar.slider("Temperature: ", min_value=0.0, max_value=1.5, value=0.0, step=0.01)

    llm = AzureChatOpenAI(
        azure_deployment = os.environ["AZURE_OPENAI_MODEL_4O_MINI"],
        api_version = "2024-11-01-preview",
        temperature = temperature,
        max_tokens = 500,
        timeout = None,
        max_retries = 2,
    )

    return llm

def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)

    return answer.content, cb.total_cost


def main():
    init_page()

    llm = select_model()
    init_messages()

    # ユーザの入力を監視
    if user_input := st.chat_input("ご質問をどうぞ"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is thinking ..."):
            answer, cost = get_answer(llm, st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=answer))
        st.session_state.costs.append(cost)

    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:
            st.write(f"Sytem messages：{message.content}")

    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")

if __name__ == '__main__':
    main()