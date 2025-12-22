from openai import OpenAI

# Create client pointing to local vLLM server
client = OpenAI(
    api_key="EMPTY",
    base_url="https://d1bef824060e.ngrok-free.app/v1"
)

prompt_template = """
Be a friendly and helpful assistant.
"""

messages = [
    {"role": "system", "content": prompt_template}
]

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        break
    messages.append({"role": "user", "content": user_input})

    # Simple chat request
    stream = client.chat.completions.create(
        # model="Qwen/Qwen2.5-3B-Instruct",
        model="Qwen/Qwen3-4B-Instruct-2507",
        messages=messages,
        temperature=0.7,
        stream=True,
        stream_options={
            "include_usage": True,
        }
    )

    assistant_msg = ""
    print("Assistant: ", end="", flush=True)
    for chunk in stream:
        if chunk.choices:
            chunk_content = chunk.choices[0].delta.content
            print(chunk_content, end="", flush=True)
            assistant_msg += chunk_content
        else:
            break
        
    print()
    messages.append({"role": "assistant", "content": assistant_msg})
