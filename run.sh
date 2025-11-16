#!/bin/bash

# Fridge Tetris Master - Quick Start Script

echo "🧊 Fridge Tetris Master - Starting up..."
echo ""

# Check if Ollama is available
if command -v ollama &> /dev/null; then
    echo "✓ Ollama found"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✓ Ollama is running"
    else
        echo "⚠️  Ollama is not running. Starting Ollama..."
        ollama serve &
        sleep 3
    fi
    
    # Check if model is available
    if ollama list | grep -q "qwen2.5-vl"; then
        echo "✓ Qwen2.5-VL model found"
    else
        echo "⚠️  Qwen2.5-VL model not found. Pulling model..."
        echo "   This may take a while..."
        ollama pull qwen2.5-vl:7b
    fi
    
    echo ""
    echo "Starting app with Ollama backend..."
    USE_OLLAMA=true python app.py
else
    echo "⚠️  Ollama not found. Using vLLM backend (requires GPU)..."
    echo ""
    python app.py
fi

