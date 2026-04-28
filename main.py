import os
from config import WORKSPACE_DIR, OUTPUT_DIR
from modules.image_gen import generate_images  # AI Görsel üretme modülün
from modules.puzzle_maker import create_puzzle_pairs
from modules.video_editor import render_shorts

def clean_workspace():
    """Çalışma alanındaki eski dosyaları temizler (klasörleri atlayarak WinError 5'i çözer)."""
    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for file in os.listdir(WORKSPACE_DIR):
        file_path = os.path.join(WORKSPACE_DIR, file)
        # Sadece dosyaysa sil, klasörse atla!
        if os.path.isfile(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    print("🚀 Tam Otomatik Shorts Fabrikası Başlatılıyor...")
    
    # Kullanıcıdan stok sayısını al (boş basarsa 1 kabul et)
    v_sayisi_input = input("Kaç adet stok video üretilsin? (Örn: 5): ")
    v_sayisi = int(v_sayisi_input) if v_sayisi_input.isdigit() else 1
    
    for i in range(1, v_sayisi + 1):
        print(f"\n--- 📦 Üretim Hattı: Video {i}/{v_sayisi} Başladı ---")
        
        clean_workspace()
        print("[1/4] Çalışma alanı temizlendi.")
        
        # 1. Aşama: AI ile Görsel Üretimi (Stable Diffusion devreye girer)
        print("[2/4] Stable Diffusion görselleri üretiyor (RTX devrede)...")
        base_images = generate_images(count=4)  
        
        # 2. Aşama: Obje Gizleme ve Soru/Cevap Çiftleri
        puzzle_data = create_puzzle_pairs(base_images)
        print("[3/4] Gizli objeler yerleştirildi ve cevaplar hazırlandı.")
        
        # 3. Aşama: Video Kurgusu ve Render
        final_video_path = render_shorts(puzzle_data, video_index=i)
        print(f"✅ Video {i} başarıyla '{final_video_path}' konumuna kaydedildi.")

    print(f"\n🎉 Fabrika görevi tamamladı! {v_sayisi} adet video stokta hazır.")