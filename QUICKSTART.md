# Quick Start Guide

Get Fridge Tetris Master running in 5 minutes!

## Prerequisites

- Python 3.8+
- Ollama installed (recommended for easiest setup) OR vLLM with GPU

## Fastest Setup (Ollama)

### 1. Install Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai
```

### 2. Pull the Model
```bash
ollama pull qwen2.5-vl:7b
```

### 3. Install Dependencies
```bash
cd fridge-tetris-master
pip install -r requirements.txt
```

### 4. Run the App
```bash
USE_OLLAMA=true python app.py
```

### 5. Open Browser
Navigate to `http://localhost:7860`

## Using vLLM (GPU Required)

### 1. Install vLLM
```bash
pip install vllm qwen-vl-utils
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

The model will download automatically from HuggingFace (may take a while on first run).

## First Use

1. Take a clear photo of your fridge (showing shelves and existing items)
2. Take a photo of your new groceries
3. Upload both images in the web interface
4. Choose "Normal" or "Chaos" mode
5. Click "Organize My Fridge!"
6. Get roasted! 🔥

## Troubleshooting

**Ollama not found?**
- Make sure Ollama is installed and running: `ollama serve`
- Check if the model is pulled: `ollama list`

**Out of memory?**
- Use the 7B model instead of 72B
- Close other applications
- Reduce image sizes

**Slow inference?**
- Use GPU if available
- Try smaller images
- Use Ollama with GPU acceleration

## Next Steps

- Read the full [README.md](README.md) for advanced configuration
- Customize the prompt in `prompt.txt` to change the AI's personality
- Deploy to a server for sharing with friends

Happy organizing! 🧊

