FROM vllm/vllm-openai:latest

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install any additional dependencies if needed
RUN pip install --no-cache-dir huggingface-hub
RUN pip install -q --upgrade bitsandbytes torch transformers

# Set environment variables
ENV MODEL_NAME="Qwen/Qwen3-4B-Instruct-2507"
# ENV MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct"
ENV CUDA_VISIBLE_DEVICES="0"

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
    --max-num-seqs 4 \
    --enable-chunked-prefill \
    --max-num-batched-tokens 4096 \
    --dtype half"]
