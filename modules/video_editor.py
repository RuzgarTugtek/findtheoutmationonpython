import os
from moviepy.config import change_settings

# Senin bilgisayarına özel ImageMagick yolu
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from config import OUTPUT_DIR, AUDIO_DIR, HOOK_DURATION, ANSWER_DURATION, FPS, RENDER_THREADS

def create_segment(soru_path, cevap_path, is_last=False):
    # Soru Ekranı
    clip_q = ImageClip(soru_path).set_duration(HOOK_DURATION)
    tick_tock_path = os.path.join(AUDIO_DIR, "tick-tock.mp3")
    
    if os.path.exists(tick_tock_path):
        tick_tock = AudioFileClip(tick_tock_path).set_duration(HOOK_DURATION)
        clip_q = clip_q.set_audio(tick_tock)
    
    txt_q = TextClip("ONLY 1% CAN FIND IT!", fontsize=80, color='yellow', stroke_color='black', stroke_width=3, font='Impact', size=(1000, None), method='caption')
    txt_q = txt_q.set_position(('center', 150)).set_duration(HOOK_DURATION)
    video_q = CompositeVideoClip([clip_q, txt_q])

    # Cevap Ekranı
    if is_last:
        clip_a = ImageClip(soru_path).set_duration(ANSWER_DURATION)
        txt_a = TextClip("ANSWER IN THE COMMENTS!", fontsize=90, color='red', stroke_color='black', stroke_width=4, font='Impact', size=(1000, None), method='caption')
        txt_a = txt_a.set_position('center').set_duration(ANSWER_DURATION)
        video_a = CompositeVideoClip([clip_a, txt_a])
    else:
        clip_a = ImageClip(cevap_path).set_duration(ANSWER_DURATION)
        ding_path = os.path.join(AUDIO_DIR, "ding.mp3")
        
        if os.path.exists(ding_path):
            ding = AudioFileClip(ding_path).set_duration(2)
            clip_a = clip_a.set_audio(ding)
        video_a = clip_a

    return concatenate_videoclips([video_q, video_a])

def render_shorts(puzzle_data, video_index=1):
    segments = []
    total = len(puzzle_data)
    
    print(f"🎬 Video {video_index} klipleri birleştiriliyor...")
    for i, data in enumerate(puzzle_data):
        is_last = (i == total - 1)
        seg = create_segment(data["soru"], data["cevap"], is_last=is_last)
        segments.append(seg)
        
    final_video = concatenate_videoclips(segments)
    output_path = os.path.join(OUTPUT_DIR, f"shorts_stok_{video_index}.mp4")
    
    print(f"🚀 Render {video_index} başlıyor... (Threads: {RENDER_THREADS})")
    final_video.write_videofile(
        output_path, 
        fps=FPS, 
        codec="libx264", 
        audio_codec="aac", 
        threads=RENDER_THREADS, 
        preset="ultrafast" 
    )
    return output_path