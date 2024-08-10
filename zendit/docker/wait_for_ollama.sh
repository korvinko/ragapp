#!/bin/bash

# Start Ollama in the background.
ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieving model..."
ollama pull llama3.1:8b
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid