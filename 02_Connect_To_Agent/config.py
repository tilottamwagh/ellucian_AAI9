import boto3
import os 
from dotenv import load_dotenv

load_dotenv()

REGION = os.getenv("AWS_REGION")
AGENT_ID = os.getenv("BEDROCK_AGENT_ID")
ALIAS_ID = os.getenv("BEDROCK_AGENT_ALIAS_ID")

bedrock_agent_client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION,
)

# Bedrock Agent response parser
# streaming data from EventStream format to text output
def parse_event_stream(response) -> str:
            """
            Parse the EventStream 'completion' in the Bedrock Agent response and
            return the assembled text output.
            """
            message_output = ""

            try:
                event_stream = response.get('completion')
                if event_stream is None:
                    return "Agent returned empty response."

                for event in event_stream:
                    # Handle chunk events containing the actual response text
                    if 'chunk' in event:
                        chunk = event['chunk']
                        if 'bytes' in chunk:
                            raw_bytes = chunk['bytes']
                            if raw_bytes:
                                try:
                                    decoded_text = raw_bytes.decode('utf-8')
                                    if decoded_text.strip():
                                        try:
                                            chunk_data = json.loads(decoded_text)
                                        except json.JSONDecodeError:
                                            # Not JSON — treat as plain text
                                            message_output += decoded_text
                                            continue

                                        # If chunk_data is a structured chunk, extract nested bytes
                                        if chunk_data.get('type') == 'chunk' and 'bytes' in chunk_data:
                                            try:
                                                text_data = json.loads(chunk_data['bytes'])
                                                if 'outputText' in text_data:
                                                    message_output += text_data['outputText']
                                            except Exception:
                                                # If nested bytes aren't JSON, append raw nested content
                                                message_output += chunk_data.get('bytes', '')
                                        # If chunk_data directly contains outputText
                                        elif 'outputText' in chunk_data:
                                            message_output += chunk_data['outputText']

                                except Exception:
                                    # On any decode/parsing error, try to append raw bytes representation
                                    try:
                                        message_output += raw_bytes.decode('utf-8', errors='ignore')
                                    except Exception:
                                        pass

                    # Other event types can be ignored or logged externally
                    elif 'trace' in event:
                        pass
                    else:
                        pass

            except Exception as e:
                raise RuntimeError(f"Error processing EventStream: {e}")

            return message_output.strip() if message_output else "Agent returned empty response."
