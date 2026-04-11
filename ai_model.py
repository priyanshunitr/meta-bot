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
    ('system', "You are a professional assistant for Clinqo. You MUST answer the user's question using the provided context first. If the answer is in the context, use it. If not, check the chat history. Only if both are empty should you say you don't know.\n\nCRITICAL CONTEXT:\n{context}"),
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
    context_text = context_data[0] if isinstance(context_data, tuple) else context_data
    
    print(f"\n--- DEBUG ---\nUser Message: {message}")
    print(f"Context Found: {context_text[:100]}...") # Printing first 100 chars
    print("-------------\n")

    # Append user message to history
    chat_history.append(HumanMessage(content=message))

    # Invoke prompt with variables
    prompt_data = {
        'context': context_text,
        'recorded_chats': chat_history,
        'input': message
    }
    prompt = template.invoke(prompt_data)

    # Get response
    result = await model.ainvoke(prompt)

    # Store AI response
    chat_history.append(AIMessage(content=result.content))

    return result.content