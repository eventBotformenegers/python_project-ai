import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    thread = openai.beta.threads.create()
    print(f"Ваш thread_id: {thread.id}") 