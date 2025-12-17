FROM vllm/vllm-openai:latest

# Set environment variables
ENV MODEL_NAME="Qwen/Qwen2.5-3B-Instruct"

# Expose the API port
EXPOSE 8000

# Start vLLM server
ENTRYPOINT ["sh", "-c", \
    "vllm serve ${MODEL_NAME} \
    --max-model-len 4096 \
    --max-num-seqs 32 \
    --host 0.0.0.0 \
    --port 8000"]