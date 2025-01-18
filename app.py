import streamlit as st
from utils import apply_styles
from multi_agent import multi_ai_agent, as_stream

st.title("Phidata multi agent ai")
st.markdown("This is a multi-agent system using GROQ model that can perform various tasks such as search web for info, aggregate finance/shares data, generate python code, search information from wikipedia, fetch metadata/caption from youtube video link.")

if st.button("💬 New Chat"):
  st.session_state.messages = []
  st.rerun()

apply_styles()

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    chunks = multi_ai_agent.run(prompt, stream=True)
    response = st.write_stream(as_stream(chunks))
  st.session_state.messages.append({"role": "assistant", "content": response})