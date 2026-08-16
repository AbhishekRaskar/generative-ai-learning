import dotenv
import os
dotenv.load_dotenv()

# chat model import init_chat_model
# from langchain.chat_models import init_chat_model

# model class import
from langchain_groq import ChatGroq

# chat model initialization
# model = init_chat_model("groq:openai/gpt-oss-120b")

# model class initialization
model = ChatGroq(model="openai/gpt-oss-120b")

while True:
    input_text = input("You: ")
    if input_text.lower() == "exit":
        print("See you later!")
        break
    elif input_text.strip() != "":
        response = model.invoke(input_text)
        print("Chatbot:", response.content)