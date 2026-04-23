import io
import torch
import requests
import traceback
import uvicorn
from typing import Any, Optional
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from transformers import AutoProcessor, AutoModelForImageTextToText

# --- CONFIGURATION ---
# Using your provided Fanar Key
FANAR_API_KEY = "EAwYyPhpNKiiAV9mguCtBSBij9iayirt"
FANAR_API_URL = "https://api.fanar.qa/v1/chat/completions"

class SmolViewer:
    def __init__(self):
        print("🛰️ Loading SmolVLM (Vision Engine) on GPU...")
        self.model_id = "HuggingFaceTB/SmolVLM-Instruct"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # 1. Load Processor
        self.processor: Any = AutoProcessor.from_pretrained(self.model_id)
      
        model_instance: Any = AutoModelForImageTextToText.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16, 
            _attn_implementation="eager" 
        )
        
        self.model: Any = model_instance.to(self.device)
        self.model.eval()
        
        print(f"SmolVLM is LIVE on {self.device}!")

    def translate_to_egyptian(self, english_description: str) -> str:
        """
        Takes the raw English output from SmolVLM and uses Fanar 
        to turn it into friendly Egyptian Arabic.
        """
        headers = {
            "Authorization": f"Bearer {FANAR_API_KEY}",
            "Content-Type": "application/json"
        }
        
        vlm_prompt = f"""
        You are Viora, an intelligent assistant for blind students.
        I will give you an English description of what the camera sees. 
        Translate it into friendly, helpful, and natural EGYPTIAN ARABIC.
        Keep it concise but clear about object positions.

        English Description: {english_description}
        Egyptian Arabic: """

        payload = {
            "model": "Fanar",
            "messages": [{"role": "user", "content": vlm_prompt}],
            "temperature": 0.5 
        }

        try:
            response = requests.post(FANAR_API_URL, headers=headers, json=payload, timeout=12)
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Translation Error: {e}")
            return "مش قادرة أوصف اللي قدامي بالظبط دلوقتي، ممكن تحاول تاني؟"

    def analyze(self, image_bytes: bytes) -> str:
        """Processes the image and returns the final Egyptian Arabic text."""
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            
            # Formulating the vision prompt
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": "Describe this scene briefly for a blind person. Mention key objects and their locations (left, right, or center)."}
                    ]
                }
            ]
            
            # Prepare inputs
            prompt = self.processor.apply_chat_template(messages, add_generation_prompt=True)
            inputs = self.processor(text=prompt, images=[image], return_tensors="pt").to(self.device)
            
            # Generate English Description
            with torch.no_grad():
                generated_ids = self.model.generate(**inputs, max_new_tokens=100)
            
            # Decode output
            generated_texts = self.processor.batch_decode(
                generated_ids[:, inputs["input_ids"].size(1):], 
                skip_special_tokens=True
            )
            
            raw_english = generated_texts[0].strip()
            print(f"🇬🇧 VLM (English): {raw_english}")
            
            # Convert to Egyptian Arabic via Fanar
            egyptian_arabic = self.translate_to_egyptian(raw_english)
            return egyptian_arabic

        except Exception as e:
            print(f"❌ Vision Engine Error: {e}")
            traceback.print_exc()
            return "Viora is having trouble seeing clearly."

# --- FASTAPI APP ---
app = FastAPI(title="Viora Vision Server", description="Handles SmolVLM + Egyptian Translation")
viewer = SmolViewer()

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        content = await file.read()
        description = viewer.analyze(content)
        print(f"🇪🇬 Final Output: {description}")
        
        return {
            "status": "success", 
            "viora_reply": description
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)