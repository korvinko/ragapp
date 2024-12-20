#!/bin/bash

# Start Ollama in the background.
ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 10

echo "🔴 Retrieving model..."
ollama pull qwen2.5:7b-instruct
ollama pull rjmalagon/gte-qwen2-1.5b-instruct-embed-f16
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid