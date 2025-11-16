"""
Fridge Tetris Master - The world's most judgmental refrigerator organizer
Uses Qwen3-VL to analyze fridge contents and provide optimal 3D packing instructions
"""

import gradio as gr
import os
from pathlib import Path
from typing import Tuple, Optional
import base64
from io import BytesIO
from PIL import Image

# Try to import Qwen VL utilities and vLLM
try:
    from qwen_vl_utils import process_vision_info
    QWEN_AVAILABLE = True
except ImportError:
    QWEN_AVAILABLE = False
    print("Warning: qwen_vl_utils not available. Install with: pip install qwen-vl-utils")

try:
    from vllm import LLM, SamplingParams
    VLLM_AVAILABLE = True
except ImportError:
    VLLM_AVAILABLE = False
    print("Warning: vllm not available. Install with: pip install vllm")

# Alternative: Ollama support
try:
    import requests
    import json
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class FridgeTetrisMaster:
    def __init__(self, model_name: str = "Qwen/Qwen2.5-VL-7B-Instruct", use_ollama: bool = False, ollama_url: str = "http://localhost:11434"):
        """
        Initialize the Fridge Tetris Master
        
        Args:
            model_name: Model name for vLLM (if not using Ollama)
            use_ollama: Whether to use Ollama instead of vLLM
            ollama_url: Ollama API URL
        """
        self.use_ollama = use_ollama
        self.ollama_url = ollama_url
        self.llm = None
        
        # Load the prompt
        prompt_path = Path(__file__).parent / "prompt.txt"
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                self.base_prompt = f.read()
        else:
            self.base_prompt = "You are Fridge Tetris Master. Analyze the fridge and groceries, then provide optimal packing instructions."
        
        # Initialize model if not using Ollama
        if not use_ollama and VLLM_AVAILABLE:
            try:
                print(f"Loading model: {model_name}")
                self.llm = LLM(model=model_name, trust_remote_code=True)
                print("Model loaded successfully!")
            except Exception as e:
                print(f"Error loading vLLM model: {e}")
                print("Falling back to Ollama mode. Make sure Ollama is running.")
                self.use_ollama = True
    
    def image_to_base64(self, image) -> Optional[str]:
        """Convert PIL Image or numpy array to base64 string"""
        if image is None:
            return None
        
        try:
            # Handle Gradio Image input (can be PIL Image, numpy array, or file path)
            if isinstance(image, str):
                img = Image.open(image)
            elif isinstance(image, Image.Image):
                img = image
            else:
                # Assume numpy array
                img = Image.fromarray(image)
            
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return img_str
        except Exception as e:
            print(f"Error converting image: {e}")
            return None
    
    def call_ollama(self, current_fridge_b64: str, new_groceries_b64: str, mode: str) -> Tuple[str, Optional[str]]:
        """Call Ollama API for inference"""
        if not OLLAMA_AVAILABLE:
            return "Error: Ollama not available. Install requests library.", None
        
        try:
            # Prepare the prompt
            mode_instruction = "Normal mode: maximum efficiency and cold-chain logic" if mode == "Normal" else "Chaos mode: intentionally terrible but technically possible packing with evil commentary"
            full_prompt = f"{self.base_prompt}\n\nMode: {mode}\n{mode_instruction}"
            
            # Prepare messages for Ollama
            # Ollama expects images as base64 strings in the content array
            messages = [
                {
                    "role": "user",
                    "content": full_prompt,
                    "images": [current_fridge_b64, new_groceries_b64]
                }
            ]
            
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": "qwen2.5-vl:7b",  # Adjust model name as needed
                    "messages": messages,
                    "stream": False
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                text_output = result.get("message", {}).get("content", "No response from model")
                return text_output, None
            else:
                return f"Error: Ollama API returned status {response.status_code}", None
                
        except Exception as e:
            return f"Error calling Ollama: {str(e)}", None
    
    def call_vllm(self, current_fridge_b64: str, new_groceries_b64: str, mode: str) -> Tuple[str, Optional[str]]:
        """Call vLLM for inference"""
        if self.llm is None:
            return "Error: vLLM model not loaded", None
        
        try:
            # Prepare the prompt
            mode_instruction = "Normal mode: maximum efficiency and cold-chain logic" if mode == "Normal" else "Chaos mode: intentionally terrible but technically possible packing with evil commentary"
            full_prompt = f"{self.base_prompt}\n\nMode: {mode}\n{mode_instruction}"
            
            # Prepare messages
            messages = [{
                "role": "user",
                "content": [
                    {"type": "image", "image": f"data:image/png;base64,{current_fridge_b64}"},
                    {"type": "image", "image": f"data:image/png;base64,{new_groceries_b64}"},
                    {"type": "text", "text": full_prompt}
                ]
            }]
            
            # Process vision info if available
            if QWEN_AVAILABLE:
                messages = process_vision_info(messages)
            
            # Generate response
            sampling_params = SamplingParams(
                max_tokens=2048,
                temperature=0.7 if mode == "Normal" else 0.9  # Higher temp for chaos mode
            )
            
            outputs = self.llm.chat(messages, sampling_params=sampling_params)
            
            if outputs and len(outputs) > 0:
                text_output = outputs[0].outputs[0].text
                # Try to extract image if available
                image_output = None
                if hasattr(outputs[0].outputs[0], 'image'):
                    image_output = outputs[0].outputs[0].image
                return text_output, image_output
            else:
                return "Error: No response from model", None
                
        except Exception as e:
            return f"Error calling vLLM: {str(e)}", None
    
    def organize_fridge(self, current_fridge, new_groceries, mode: str = "Normal") -> Tuple[str, Optional[str]]:
        """
        Main function to organize the fridge
        
        Args:
            current_fridge: Image of current fridge state
            new_groceries: Image of new groceries
            mode: "Normal" or "Chaos"
        
        Returns:
            Tuple of (text_output, image_output)
        """
        # Convert images to base64
        current_fridge_b64 = self.image_to_base64(current_fridge)
        new_groceries_b64 = self.image_to_base64(new_groceries)
        
        if current_fridge_b64 is None or new_groceries_b64 is None:
            return "Error: Could not process images. Please ensure both images are valid.", None
        
        # Call appropriate backend
        if self.use_ollama:
            return self.call_ollama(current_fridge_b64, new_groceries_b64, mode)
        else:
            return self.call_vllm(current_fridge_b64, new_groceries_b64, mode)


# Initialize the master
master = FridgeTetrisMaster(
    use_ollama=os.getenv("USE_OLLAMA", "false").lower() == "true",
    ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434")
)


def fridge_master_interface(current_fridge, new_groceries, mode):
    """Gradio interface function"""
    if current_fridge is None:
        return "Please upload an image of your current fridge state.", None
    if new_groceries is None:
        return "Please upload an image of your new groceries.", None
    
    text_output, image_output = master.organize_fridge(current_fridge, new_groceries, mode)
    
    # If we got an annotated image, return it; otherwise return the original fridge image
    output_image = image_output if image_output else current_fridge
    
    return text_output, output_image


# Create Gradio interface
def create_interface():
    with gr.Blocks(title="Fridge Tetris Master", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🧊 Fridge Tetris Master
        
        The world's most judgmental refrigerator organizer with perfect 3D spatial reasoning.
        
        **How to use:**
        1. Take a photo of your current fridge (showing shelves, existing items, empty spaces)
        2. Take a photo of your new groceries (on counter, table, or in bags)
        3. Choose your mode: Normal (optimal packing) or Chaos (intentionally terrible)
        4. Get roasted while learning the optimal packing order!
        """)
        
        with gr.Row():
            with gr.Column():
                current_fridge_input = gr.Image(
                    label="Current Fridge State",
                    type="pil",
                    sources=["upload", "webcam", "clipboard"]
                )
                new_groceries_input = gr.Image(
                    label="New Groceries",
                    type="pil",
                    sources=["upload", "webcam", "clipboard"]
                )
                mode_radio = gr.Radio(
                    choices=["Normal", "Chaos"],
                    value="Normal",
                    label="Mode",
                    info="Normal: Optimal packing | Chaos: Intentionally terrible (for laughs)"
                )
                organize_btn = gr.Button("Organize My Fridge! 🎯", variant="primary", size="lg")
            
            with gr.Column():
                text_output = gr.Textbox(
                    label="Packing Instructions",
                    lines=20,
                    max_lines=30,
                    show_copy_button=True
                )
                image_output = gr.Image(
                    label="Annotated Fridge Layout",
                    type="pil"
                )
        
        organize_btn.click(
            fn=fridge_master_interface,
            inputs=[current_fridge_input, new_groceries_input, mode_radio],
            outputs=[text_output, image_output]
        )
        
        gr.Markdown("""
        ### 💡 Tips:
        - Make sure both images are clear and well-lit
        - The fridge photo should show all shelves and existing items
        - The groceries photo should show all items you want to pack
        - Chaos mode is for entertainment - don't actually pack your fridge that way!
        """)
    
    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name=os.getenv("SERVER_NAME", "0.0.0.0"),
        server_port=int(os.getenv("SERVER_PORT", "7860")),
        share=os.getenv("SHARE", "false").lower() == "true"
    )

