docker run --rm -d \
  --name vllm-server \
  --env-file .env \
  --gpus all \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  local-llm:latest

docker attach vllm-server