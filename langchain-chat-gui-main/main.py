# python 3.8 (3.8.16) or it doesn't work
# pip install streamlit streamlit-chat langchain python-dotenv
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()
    
    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)

    # setup streamlit page
    st.set_page_config(
        page_title="YLC Chatbot",
        page_icon="🤖"
    )


def main():
    init()

    chat = ChatOpenAI(temperature=0.1)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="The date is August 1st 2021 and you are a helpful research assistant. You don't need to mention the date in the conversations.")
        ]
    st.button("Chatbot",type="primary")
    st.header("YLC Chatbot 🤖")

    # sidebar with user input
    with st.sidebar:
        user_input = st.text_input("Your message: ", key="user_input")
        user_input2 = st.text_area("Instructions", key="user_input2")

        # handle user input
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(
                AIMessage(content=response.content))
        if user_input2:
            st.session_state.messages.append(HumanMessage(content=user_input2))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(
                AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()
