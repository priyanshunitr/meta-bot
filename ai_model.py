import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
model = ChatOpenAI()

chat_history = [
    SystemMessage(content = 'You are a helpful assistant')
]

with open (r'D:\old\Dev\meta-bot\chat_history.txt') as f:
    chat_history.extend(f.readlines())

print ('chat_history : ', chat_history)

# user = input("You: ")
template = ChatPromptTemplate([
    ('system', 'You are a helpful AI assistant'),
    MessagesPlaceholder ( variable_name = 'recorded_chats')
])

# chat_history = [
#     SystemMessage(content='You are a helpful AI assistant')
# ]

# template = ChatPromptTemplate([
#     MessagesPlaceholder(variable_name='recorded_chats')
# ])


async def generate_reply(message: str):
    # Add user message
    chat_history.append(HumanMessage(content=message))

    # Build prompt
    prompt = template.invoke({
        'recorded_chats': chat_history
    })

    # Get response
    result = await model.ainvoke(prompt)

    # Store AI response
    chat_history.append(AIMessage(content=result.content))

    return result.content