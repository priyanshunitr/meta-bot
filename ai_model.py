import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from query import get_context

load_dotenv()
model = ChatOpenAI()

chat_history = []

chat_history_file = os.path.join(os.path.dirname(__file__), 'chat_history.txt')
with open(chat_history_file) as f:
    chat_history.extend(f.readlines())

print ('chat_history : ', chat_history)

template = ChatPromptTemplate([
    ('system', "You are a helpful assistant for a company named Clinqo. Use the following context and previous chat history to answer the user's question.\n\nContext:\n{context}"),
    MessagesPlaceholder(variable_name='recorded_chats'),
    ('human', "{input}")
])

# chat_history = [
#     SystemMessage(content='You are a helpful AI assistant')
# ]

# template = ChatPromptTemplate([
#     MessagesPlaceholder(variable_name='recorded_chats')
# ])


async def generate_reply(message: str):
    context_data = get_context(message)
    
    # Ensure we are passing a string, not a tuple
    context_text = context_data[0] if isinstance(context_data, tuple) else context_data

    # Append user message to history
    chat_history.append(HumanMessage(content=message))

    # Invoke prompt with variables
    prompt = template.invoke({
        'context': context_text,
        'recorded_chats': chat_history,
        'input': message
    })

    # Get response
    result = await model.ainvoke(prompt)

    # Store AI response
    chat_history.append(AIMessage(content=result.content))

    return result.content