from langchain_core.messages import HumanMessage
import streamlit as st
import asyncio
import logging
import time
import os
import sys

# some path hacks to make this easy to run via the IDE
if __package__ == '' or __package__ is None:
    __package__ = 'ria'
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .agents import create_supervisor
from .react_agents import create_react_supervisor
from .utils import extract_ai_message_content

async def chat_ui():

    """Main application entry point"""
    supervisor = create_supervisor()
    # supervisor = create_react_supervisor()

    # Streamlit interface
    st.title("AI Assistant")
    logging.info("App started")

    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI Assistant."}
        ]

    # Display all previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("How can I assist you today?"):

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            start_time = time.time()
            logging.info("Generating response...")
            with st.spinner("Processing..."):
                inputs = {
                    "messages": [
                        HumanMessage(
                            content=prompt
                        )
                    ],
                }
                config = {"configurable": {"thread_id": "2", "recursion_limit": 15}}   
                # Get the final step in the stream
                final_event = None
                async for step in supervisor.astream(inputs, config=config):
                    final_event = step  # Keep updating to the latest step
                    print(final_event)
                    print("\n")
                    response_message = extract_ai_message_content(final_event)
                    print(response_message)
                    
                    for agent, content in response_message:
                        assistant_reply = f"**Agent:** `{agent}`\n\n{content}"
                        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                        st.markdown(assistant_reply)
                        st.markdown("---")        

# ================================================= #
#            Use the supervisor
# ================================================= #

async def main():
    # Example user queries to test the graph:
        # which assistants do you work with?
        # Do you respond to weather related queries?
        # How is weather in New York today?
        # calculate the result of 3 + 5
        # Get the details of jira id RG-3552 from the RG project queue.
        # Summarize the jira issue RG-457
    user_request = (
         "Can you calculate 25 multiplied by 4?"
        )

    print("User Request:", user_request)
    print("\n" + "="*80 + "\n")
    async for step in create_supervisor().astream(
    # async for step in create_react_supervisor().astream(
        {"messages": [{"role": "user", "content": user_request}]}
    ):
        for update in step.values():
            print(update)
            for message in update.get("messages", []):
                message.pretty_print()

def main_entry_point():
    # asyncio.run(chat_ui())
    asyncio.run(main())

if __name__ == "__main__":
    # asyncio.run(chat_ui())
    asyncio.run(main())