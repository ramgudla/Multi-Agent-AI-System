from typing import List

# Helper function to recursively extract 'content' from all AIMessage instances
def extract_ai_message_content(stream) -> List[str]:
    # Extract AIMessage contents into an array as {key: value}
    ai_message_contents = []

    for key, value in stream.items():
            # We expect a 'messages' key
            if value is None:
                continue
            messages = value['messages']
            if isinstance(messages, list):  # Skip ToolMessages or others
                continue
            ai_message_contents.append((key, messages.content)) # Assuming messages is an AIMessage
            # print("ai_message_contents...\n")
            # print(ai_message_contents)
            # if isinstance(messages, dict):  # AIMessage will typically be a dict
            #     ai_message_contents.append((key, messages.content))
            #     # if 'content' in messages:
            #     #     ai_message_contents.append({key: messages['content']})
            # elif isinstance(messages, list):  # Skip ToolMessages or others
            #     continue
        
    return ai_message_contents