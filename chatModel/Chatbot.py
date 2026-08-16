from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

model = ChatMistralAI(model="mistral-small-2603")

history = [
    SystemMessage(content="You are a funny assistant that responds in a humorous way to the user."),
]
while True:
    text = input("You : ")
    history.append(HumanMessage(content=text))
    result = model.invoke(history)
    history.append(AIMessage(content=result.content))
    if (text.strip() == "exit"):
        print("See you later..!")
        break
    elif (text.strip() != ""):    
        print(f"Assistant : {result.content}")

print("Conversation history:", history)        