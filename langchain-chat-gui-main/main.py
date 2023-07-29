# python 3.8 (3.8.16)
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

    def clear_text():
        st.session_state["user_input"] = ""
    
    chat = ChatOpenAI(temperature=0.1)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="The date is August 1st 2021 and you are a helpful research assistant. You don't need to mention the date in the conversations. If you are unsure and the answer is not clear, say 'Sorry, I don't know how to help with that.'")
        ]
    #st.button("Chatbot",type="primary")
    st.header("YLC Chatbot 🤖")

    # sidebar with user input
    with st.sidebar:
        user_input = st.text_area("Your Message/Instructions:", key="user_input")
        submit_button = st.button(":green[Submit]")
        clear_button = st.button(":white[Clear]", on_click=clear_text, key="clear_button")

    # handle user input
    if submit_button or user_input:
        if st.session_state["user_input"] != "":
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
  

    # handle user input
    # if user_input:
    #     st.session_state.messages.append(HumanMessage(content=user_input))
    #     with st.spinner("Thinking..."):
    #         response = chat(st.session_state.messages)
    #     st.session_state.messages.append(
    #         AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()
