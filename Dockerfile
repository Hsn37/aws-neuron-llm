FROM vllm/vllm-openai:latest

# Set environment variables
ENV MODEL_NAME="google/gemma-2-27b-it"
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
    --quantization bitsandbytes \
    --load-format bitsandbytes \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.90 \
    --max-num-seqs 8 \
    --enable-chunked-prefill \
    --max-num-batched-tokens 8192 \
    --trust-remote-code"]
