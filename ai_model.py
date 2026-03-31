from fastapi import FastAPI, Response, Request
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import asyncio

load_dotenv ()

model = ChatOpenAI()

chat_history = [
    SystemMessage(content = 'You are a helpful assistant')
]

template = ChatPromptTemplate([
    ('system', 'You are a helpful AI assistant'),
    MessagesPlaceholder ( variable_name = 'recorded_chats')
])

async def generate_reply(message: str):
    while True:
        if message == "exit":
            break

        chat_history.append(HumanMessage(content = ("User: " + message)))
        prompt = template.invoke({'recorded_chats': chat_history })

        result = await model.ainvoke (prompt)

        chat_history.append(AIMessage(content=("Bot: " + result.content)))

        return result.content

#print(asyncio.run(generate_reply("Who are you?")))
