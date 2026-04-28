import os

# Ana Dizin Yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Asset Yolları
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
OVERLAYS_DIR = os.path.join(ASSETS_DIR, "overlays")

# Video Ayarları
HOOK_DURATION = 10  # Sorunun ekranda kalma süresi
ANSWER_DURATION = 3 # Cevabın ekranda kalma süresi
FPS = 30
RENDER_THREADS = 4  # Render hızını artırmak için çekirdek kullanımı