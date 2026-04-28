import os
import random
from PIL import Image, ImageDraw
from config import WORKSPACE_DIR, OVERLAYS_DIR, BASE_DIR

def get_next_overlay():
    """Listeden sıradaki objeyi seçer ve nerede kaldığını hafızaya kaydeder."""
    overlay_list = [
        "diamond.png", "eye.png", "cat.png", "potion.png", 
        "spongebob.png", "shrek.png", "creeper.png", "frog.png", "x_mark.png"
    ]
    
    tracker_file = os.path.join(BASE_DIR, "overlay_tracker.txt")
    
    try:
        with open(tracker_file, "r") as f:
            current_index = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        current_index = 0
        
    selected_overlay = overlay_list[current_index % len(overlay_list)]
    
    next_index = (current_index + 1) % len(overlay_list)
    with open(tracker_file, "w") as f:
        f.write(str(next_index))
        
    return selected_overlay

def create_puzzle_pairs(base_images):
    puzzle_data = []
    selected_overlay_name = get_next_overlay()
    print(f"🎯 Bu video için seçilen gizli obje: {selected_overlay_name}")
    
    overlay_path = os.path.join(OVERLAYS_DIR, selected_overlay_name)
    
    if not os.path.exists(overlay_path):
        raise FileNotFoundError(f"'{selected_overlay_name}' dosyası bulunamadı!")

    # İzleyiciyi 5-6 saniye tutacak altın oran
    overlay = Image.open(overlay_path).convert("RGBA")
    overlay = overlay.resize((45, 45)) 

    for idx, img_path in enumerate(base_images):
        base = Image.open(img_path).convert("RGBA")
        w, h = base.size
        
        pad_x, pad_y = 150, 300
        rand_x = random.randint(pad_x, w - pad_x)
        rand_y = random.randint(pad_y, h - pad_y)

        # Soru Görseli
        question_img = base.copy()
        question_img.paste(overlay, (rand_x, rand_y), overlay)
        q_path = os.path.join(WORKSPACE_DIR, f"{idx}_soru.png")
        question_img.save(q_path, format="PNG")

        # Cevap Görseli (Kırmızı Daire)
        answer_img = question_img.copy()
        draw = ImageDraw.Draw(answer_img)
        radius = 70
        left_up = (rand_x + 17 - radius, rand_y + 17 - radius) # 35'in yarısına göre hizalandı
        right_down = (rand_x + 17 + radius, rand_y + 17 + radius)
        
        draw.ellipse([left_up, right_down], outline="red", width=12)
        a_path = os.path.join(WORKSPACE_DIR, f"{idx}_cevap.png")
        answer_img.save(a_path, format="PNG")

        puzzle_data.append({
            "soru": q_path,
            "cevap": a_path
        })
    
    return puzzle_data