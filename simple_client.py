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

# Simple chat request
response = client.chat.completions.create(
    model="Qwen/Qwen2.5-3B-Instruct",
    messages=[
        {"role": "user", "content": "Hello! Tell me a joke."}
    ],
    max_tokens=200,
)

print(response.choices[0].message.content)

