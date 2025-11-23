# 🧊 Fridge Tetris Master

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![GitHub stars](https://img.shields.io/github/stars/yksanjo/fridge-tetris-ai?style=social)](https://github.com/yksanjo/fridge-tetris-ai/stargazers) [![GitHub forks](https://img.shields.io/github/forks/yksanjo/fridge-tetris-ai.svg)](https://github.com/yksanjo/fridge-tetris-ai/network/members)
[![GitHub issues](https://img.shields.io/github/issues/yksanjo/fridge-tetris-ai.svg)](https://github.com/yksanjo/fridge-tetris-ai/issues) [![Last commit](https://img.shields.io/github/last-commit/yksanjo/fridge-tetris-ai.svg)](https://github.com/yksanjo/fridge-tetris-ai/commits/main)


The world's most judgmental refrigerator organizer with perfect 3D spatial reasoning. Uses Qwen3-VL to analyze your fridge and groceries, then provides optimal (or hilariously terrible) 3D packing instructions with arrows and savage commentary.

## Features

- 📸 **Dual Image Analysis**: Takes photos of your current fridge state and new groceries
- 🎯 **Optimal 3D Packing**: Uses Qwen3-VL's spatial reasoning to create the most efficient packing order
- 🎨 **Visual Annotations**: Draws colored arrows and labels directly on the image showing where each item goes
- 🔥 **Savage Commentary**: Roasts you if you bought too much or something dumb
- 😈 **Chaos Mode**: Intentionally terrible packing arrangements for laughs (milk on top of eggs, etc.)

## Quick Start

### Option 1: Using Ollama (Easiest)

1. **Install Ollama** (if not already installed):
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Or download from https://ollama.ai
   ```

2. **Pull the Qwen2.5-VL model**:
   ```bash
   ollama pull qwen2.5-vl:7b
   # Or for the larger model:
   # ollama pull qwen2.5-vl:72b
   ```

3. **Start Ollama** (if not running):
   ```bash
   ollama serve
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the app**:
   ```bash
   USE_OLLAMA=true python app.py
   ```

6. **Open your browser** to `http://localhost:7860`

### Option 2: Using vLLM (For Production/GPU)

1. **Install vLLM and dependencies**:
   ```bash
   pip install vllm qwen-vl-utils
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   python app.py
   ```

   The app will automatically load `Qwen/Qwen2.5-VL-7B-Instruct` from HuggingFace.

3. **For a different model**, edit `app.py`:
   ```python
   master = FridgeTetrisMaster(
       model_name="Qwen/Qwen2.5-VL-72B-Instruct",  # or your preferred model
       use_ollama=False
   )
   ```

## Usage

1. **Take a photo of your current fridge** - Make sure it shows:
   - All shelves clearly visible
   - Existing items and their positions
   - Empty spaces

2. **Take a photo of your new groceries** - Can be:
   - On a counter or table
   - In shopping bags
   - Anywhere clearly visible

3. **Choose your mode**:
   - **Normal**: Maximum efficiency and cold-chain logic
   - **Chaos**: Intentionally terrible but technically possible packing (for entertainment)

4. **Click "Organize My Fridge!"** and get roasted while learning the optimal packing order!

## Example Output

```
Step 3: "Take the oat milk (the one pretending to be barista edition) and slide it 
behind the half-dead kombucha on the middle shelf, far left. Yes, all the way back. 
Stop treating your fridge like a museum display."

[Image with neon-green arrow from oat milk carton to exact gap behind kombucha]
```

## Configuration

### Environment Variables

- `USE_OLLAMA`: Set to `"true"` to use Ollama instead of vLLM (default: `"false"`)
- `OLLAMA_URL`: Ollama API URL (default: `"http://localhost:11434"`)
- `SERVER_NAME`: Gradio server hostname (default: `"0.0.0.0"`)
- `SERVER_PORT`: Gradio server port (default: `"7860"`)
- `SHARE`: Set to `"true"` to create a public Gradio share link (default: `"false"`)

### Customizing the Prompt

Edit `prompt.txt` to customize the AI's personality and instructions. The prompt is loaded automatically when the app starts.

## System Requirements

### For Ollama:
- CPU or GPU (GPU recommended for faster inference)
- 8GB+ RAM for 7B model, 32GB+ for 72B model
- Ollama installed and running

### For vLLM:
- NVIDIA GPU with CUDA support (recommended)
- 8GB+ VRAM for 7B model, 80GB+ for 72B model
- Python 3.8+

## Troubleshooting

### "Model not loaded" error
- **Ollama**: Make sure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull qwen2.5-vl:7b`)
- **vLLM**: Check that you have enough GPU memory and CUDA is properly installed

### "Could not process images" error
- Ensure both images are valid and in a supported format (PNG, JPEG, etc.)
- Try resizing very large images

### Slow inference
- Use a GPU if available
- Try the smaller 7B model instead of 72B
- Reduce image resolution if images are very large

## Deployment

### Local Network
```bash
python app.py
# Access from other devices on your network at http://YOUR_IP:7860
```

### Public Share Link
```bash
SHARE=true python app.py
# Gradio will provide a public URL
```

### Docker (Coming Soon)
Docker deployment instructions will be added soon.

## How It Works

1. **Image Processing**: Both images are converted to base64 and sent to the vision-language model
2. **Spatial Analysis**: Qwen3-VL analyzes:
   - Existing items in the fridge with bounding boxes
   - Available spaces and shelf positions
   - New groceries to be packed
   - 3D depth and spatial relationships
3. **Packing Plan**: The model generates a numbered step-by-step packing plan
4. **Visualization**: The model outputs an annotated image with arrows and labels
5. **Commentary**: Brutally honest feedback about your shopping choices

## Contributing

Contributions welcome! Areas for improvement:
- Better image preprocessing
- Support for more vision models
- Batch processing multiple fridges
- Mobile app version
- Integration with shopping list apps

## License

MIT License - Feel free to use this for your own projects!

## Credits

Built with:
- [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL) - Vision-language model
- [Gradio](https://gradio.app/) - Web interface
- [vLLM](https://github.com/vllm-project/vllm) - Fast LLM inference
- [Ollama](https://ollama.ai/) - Local LLM runner

## Disclaimer

Chaos mode is for entertainment purposes only. Please don't actually pack your fridge according to chaos mode instructions - your food will spoil and you'll be sad. 😅

---

**Ready to get roasted? Upload those fridge photos and let's organize!** 🎯

