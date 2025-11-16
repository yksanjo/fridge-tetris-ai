"""
Example usage of Fridge Tetris Master
This script demonstrates how to use the FridgeTetrisMaster class programmatically
"""

from app import FridgeTetrisMaster
from PIL import Image

# Initialize the master
# Option 1: Using Ollama (easiest)
master = FridgeTetrisMaster(use_ollama=True, ollama_url="http://localhost:11434")

# Option 2: Using vLLM (requires GPU)
# master = FridgeTetrisMaster(
#     model_name="Qwen/Qwen2.5-VL-7B-Instruct",
#     use_ollama=False
# )

# Load your images
current_fridge = Image.open("path/to/your/fridge.jpg")
new_groceries = Image.open("path/to/your/groceries.jpg")

# Get packing instructions
text_output, image_output = master.organize_fridge(
    current_fridge=current_fridge,
    new_groceries=new_groceries,
    mode="Normal"  # or "Chaos" for laughs
)

# Print the instructions
print("Packing Instructions:")
print(text_output)

# Save the annotated image if available
if image_output:
    image_output.save("annotated_fridge.png")
    print("\nAnnotated image saved to annotated_fridge.png")

