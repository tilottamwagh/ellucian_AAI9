# streamlit code
import streamlit as st
from bedrock_agent import invoke_agent

st.title("AWS Bedrock Agent Chat")
st.write("Chat with your AWS Bedrock Agent!")
user_input = st.text_input("user: ", "") 
if st.button("Send"):
    if user_input:
        with st.spinner("Waiting for agent response..."):
            response = invoke_agent(user_input)
        st.success("Agent response received!")
        st.write(f"agent: {response}")
    else:
        st.warning("Please enter a message to send to the agent.")

