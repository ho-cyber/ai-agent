import streamlit as st
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain.schema import AIMessage, HumanMessage
from streamlit_chat import message
import requests
# Constants
template = """
    I want you to act as a language tutor to help me learn {target_language}.
    I want you to have a dialog with me. 
    I will speak to you in either {native_language} or {target_language}. 
    And you will continue the conversation with me, your response is only in {target_language}, don't include any other language.
    Your first message is to say hello to me and start the conversation. 
"""
max_dialog_items = 20

prompt = PromptTemplate(
    input_variables=["target_language", "native_language"],
    template=template,
)

st.set_page_config(
    page_title="AI Language Tutor",
    page_icon=":robot:"
)
st.header("Your Personal AI Language Tutor")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""Practice the desired language you would like to 
    learn with your AI powered language tutor, with who you don't
    need to worry about the hourly cost, or the busy schedules. 
    Just chat bout whatever you would like to, whereever you are 
    and whenever you are free.
    """)

with col2:
    st.image(image="dialog.png", width=300)


def init_session_states():
    if "conversation_started" not in st.session_state:
        st.session_state["conversation_started"] = False


init_session_states()


# Section 1: organize the layouts to set up the preferences.

st.markdown("### Your Language Preference")


def api_key_input():
    input_text = st.text_input(
        label="OpenAI API Key ",
        placeholder="Ex: sk-2twmA8tfCb8un4...",
        key="openai_api_key_input",
        type="password",
        disabled=st.session_state.conversation_started)
    return input_text


def target_language_input():
    input_text = st.text_input(
        label="Which language do you want to practice?",
        placeholder="Spanish",
        max_chars=50,
        key="target_language_input",
        disabled=st.session_state.conversation_started)
    return input_text


def native_language_input():
    input_text = st.text_input(
        label="Which language are you familiar with?",
        placeholder="English",
        max_chars=50,
        key="native_language_input",
        disabled=st.session_state.conversation_started)
    return input_text


openai_api_key = api_key_input()

col1, col2 = st.columns(2)
with col1:
    target_language = target_language_input()
with col2:
    native_language = native_language_input()


# Section 2: Buttons to trigger or stop the conversation.

def start_conversation():
    if st.session_state.conversation_started:
        return
    if not target_language or not native_language:
        st.warning("Please share your language preferences.")
        return
    if not openai_api_key:
        st.warning(
            'Please provide your own OpenAI API Key.', icon="⚠️")
        return
    chat = ChatOpenAI(
        temperature=0.5,
        openai_api_key=openai_api_key,
        model="gpt-3.5-turbo")
    history = ChatMessageHistory()
    history.add_user_message(prompt.format(
        target_language=target_language, native_language=native_language))
    ai_greeting = chat(history.messages)
    history.add_ai_message(ai_greeting.content)
    st.session_state.history = history
    st.session_state.chat = chat
    st.session_state.conversation_started = True


def stop_conversation():
    if not st.session_state.conversation_started:
        return
    st.session_state.conversation_started = False
    st.session_state.chat = None
    st.session_state.history = None


st.button(
    "*Start practicing!*",
    type='secondary',
    help="Click to start the conversation with your AI language tutor.",
    disabled=st.session_state.conversation_started,
    on_click=start_conversation)

st.button(
    "*Stop practicing*",
    type='secondary',
    help="Click to stop the conversation with your AI language tutor.",
    disabled=not st.session_state.conversation_started,
    on_click=stop_conversation)


# Section 3: Handle the conversation logics.

st.markdown("### Conversation with Your Language Tutor")




if st.session_state.conversation_started:
    def user_dialog_input():
        input_text = st.text_input(label="You: ", key="user_dialog_input")
        return input_text

    user_input = user_dialog_input()
    history = st.session_state.history

    if user_input and not user_input.isspace():
        history.add_user_message(user_input)
        ai_response = st.session_state.chat(history.messages)
        history.add_ai_message(ai_response.content)

    messages = history.messages
    for i in range(len(messages) - 1, max(0, len(messages)-max_dialog_items-1), -1):
        if isinstance(messages[i], AIMessage):
            message(messages[i].content, key=str(i))
        elif isinstance(messages[i], HumanMessage):
            message(messages[i].content, key=str(i), is_user=True)

 
