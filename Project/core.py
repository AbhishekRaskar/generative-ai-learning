from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI


model = ChatMistralAI(
    model="mistral-small-2603"
)

result = model.invoke("Hello, how are you?")

print(result.content)