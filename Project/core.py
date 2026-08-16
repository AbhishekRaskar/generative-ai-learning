from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI


model = ChatMistralAI(model="mistral-small-2603")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break
    result = model.invoke(user_input)
    print(f"Assistant: {result.content}")
