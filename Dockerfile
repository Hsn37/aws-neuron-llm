FROM vllm/vllm-openai:latest

# Set environment variables
ENV MODEL_NAME="Qwen/Qwen2.5-3B-Instruct"
ENV CUDA_VISIBLE_DEVICES="0"

# Install any additional dependencies if needed
RUN pip install --no-cache-dir huggingface-hub

# Expose the API port
EXPOSE 8000

# Start vLLM server with T4-optimized settings
# T4 has 16GB memory, so we configure accordingly
ENTRYPOINT ["sh", "-c", \
    "vllm serve ${MODEL_NAME} \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 1 \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.90 \
    --max-num-seqs 32 \
    --trust-remote-code"]
