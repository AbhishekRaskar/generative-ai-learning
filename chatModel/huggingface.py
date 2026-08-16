from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")

print("Token loaded:", bool(token))

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Flash",
    huggingfacehub_api_token=token
)

model = ChatHuggingFace(llm=llm)

while True:
    input_text = input("You: ")
    if input_text.lower() == "exit":
        print("See you later!")
        break
    elif input_text.strip() != "":
        response = model.invoke(input_text)
        print("Chatbot:", response.content)
