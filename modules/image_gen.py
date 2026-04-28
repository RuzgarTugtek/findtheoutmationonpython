import os
import requests
import base64
from io import BytesIO
from PIL import Image
from config import WORKSPACE_DIR

def generate_images(count=4):
    """Stable Diffusion API'sine bağlanıp belirtilen sayıda görsel üretir."""
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    
    # Promptunu kendi kanalının konseptine göre değiştirebilirsin
    payload = {
        "prompt": "isometric puzzle game scene, highly detailed, cyberpunk city, neon lights, 8k resolution, vibrant colors",
        "negative_prompt": "blurry, text, watermark, low quality, deformed, characters",
        "steps": 20,
        "width": 512,
        "height": 512,
        "batch_size": count
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"❌ API Hatası: {response.status_code}. Stable Diffusion açık mı ve --api komutu aktif mi?")
        
    r = response.json()
    generated_paths = []
    
    for i, img_b64 in enumerate(r['images']):
        image = Image.open(BytesIO(base64.b64decode(img_b64.split(",", 1)[0])))
        img_path = os.path.join(WORKSPACE_DIR, f"{i}_base.png")
        image.save(img_path, format="PNG")
        generated_paths.append(img_path)
        
    return generated_paths