import chainlit as cl
import json
from my_secrets import Secrets
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
)
from typing import cast
from rich import print


@cl.on_chat_start
async def start():
    secrets = Secrets()

    external_client = AsyncOpenAI(
        base_url=secrets.gemini_api_url,
        api_key=secrets.gemini_api_key,
    )

    set_tracing_disabled(True)

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=OpenAIChatCompletionsModel(
            model=secrets.gemini_api_model,
            openai_client=external_client,
        ),
    )

    cl.user_session.set("agent", agent)
    cl.user_session.set("history", [])

    await cl.Message(
        content="Hello! I am your assistant. How can I help you today?"
    ).send()


@cl.on_message
async def main(message: cl.Message):

    msg = cl.Message(content="")

    assistant_response = ""  # Initialize empty string before streaming

    agent: Agent = cast(Agent, cl.user_session.get("agent"))

    history = cl.user_session.get("history") or []

    # User ka message history mein add karo
    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_streamed(starting_agent=agent, input=history)

        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                assistant_response += token
                await msg.stream_token(token)

        await msg.update()

        # Assistant ka final response bhi history mein add karo
        history.append({"role": "assistant", "content": assistant_response})
        cl.user_session.set("history", history)

        # Har message ke baad history ko JSON file mein save karo
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

        print("[green]Chat history saved after this message[/green]")

    except Exception as e:
        msg.content = f"An error occurred while processing your request, Please try again.\nError: {e}"
        await msg.update()


