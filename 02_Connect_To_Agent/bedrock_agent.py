# agent invocation code will go here
from config import bedrock_agent_client, AGENT_ID, ALIAS_ID, parse_event_stream
import json

def invoke_agent(user_message: str):
    """
    Sends user input text to AWS Bedrock Agent
    """
    try:
        response = bedrock_agent_client.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=ALIAS_ID,
            sessionId="streamlit-session",
            inputText=user_message
        )
        # Extract the streaming text response from EventStream
        return parse_event_stream(response)
    except Exception as ex:
        return f"Error: {str(ex)}"

