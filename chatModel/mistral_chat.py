# You have to learn about the mistral chat model.
# and intergrate it into the existing codebase.

from langchain_mistralai import ChatMistralAI

from dotenv import load_dotenv
load_dotenv()   

model = ChatMistralAI(model="mistral-medium-3-5")

while True:
    text = input("You : ")
    result = model.invoke(text)
    if (text.strip() == "exit"):
        print("See you later..!")
        break
    elif (text.strip() != ""):    
        print(f"Assistant : {result.content}")