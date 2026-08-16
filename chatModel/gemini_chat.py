from dotenv import load_dotenv
import os


# chat model import init_chat_model
# from langchain.chat_models import init_chat_model


# model class import
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
# print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))

# chat model initialization
# model = init_chat_model("google_genai:gemini-2.5-flash")

# model class initialization
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

while True:
    # print("Model initialized:", model)
    text = input("You : ")
    if text.lower() == "exit":
        print("See you later!")
        break
    elif text.strip() != "":
        response = model.invoke(text)
        print("Chatbot : ", response.content)