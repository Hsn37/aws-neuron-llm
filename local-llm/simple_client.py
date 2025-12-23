#!/usr/bin/env python3
"""
Simple vLLM Client Example
A minimal example to get started quickly with your local vLLM server.
"""

from openai import OpenAI

# Create client pointing to local vLLM server
client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1"
)

prompt = """
Formulate a construction plan to build a hospital.
"""

# Simple chat request
# Note: Increased max_tokens from 200 to 2000 for longer responses
# Your prompt is ~2000 tokens, this allows for substantial output
response = client.chat.completions.create(
    model="Qwen/Qwen3-4B-Instruct-2507",
    # model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=2000,  # Increased for longer outputs with your long prompts
    temperature=0.7,
    stream=True,  # Enable streaming for faster perceived response
)

# Stream the response for better UX
for chunk in response:
    if hasattr(chunk, 'choices') and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
print()  # Final newline


