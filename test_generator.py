"""
اختبار سريع لمولد الفيديو
Quick test for video generator
"""

from video_generator import VideoGenerator
from quran_api import QuranAPI
from pexels_api import PexelsAPI

print("\n" + "="*70)
print("اختبار مُولِّد الفيديو - Video Generator Test")
print("="*70 + "\n")

# Test 1: Initialize
print("1. Initializing generator...")
try:
    generator = VideoGenerator()
    print("   ✅ Generator initialized\n")
except Exception as e:
    print(f"   ❌ Failed: {e}\n")
    exit(1)

# Test 2: Quran API
print("2. Testing Quran API...")
try:
    api = QuranAPI()
    verses = api.get_verse_text(1, 1, 1)  # Al-Fatiha, verse 1
    if verses and len(verses) > 0:
        print(f"   ✅ Fetched verse: {verses[0]['text'][:50]}...\n")
    else:
        print("   ❌ No verses returned\n")
        exit(1)
except Exception as e:
    print(f"   ❌ Failed: {e}\n")
    exit(1)

# Test 3: Download audio
print("3. Testing audio download...")
try:
    from config import TEMP_DIR
    audio_path = api.download_audio("abdul_basit", 1, 1, TEMP_DIR / "test_audio.mp3")
    if audio_path and audio_path.exists():
        print(f"   ✅ Downloaded audio: {audio_path.stat().st_size} bytes\n")
    else:
        print("   ❌ Audio download failed\n")
        exit(1)
except Exception as e:
    print(f"   ❌ Failed: {e}\n")
    exit(1)

# Test 4: Pexels API (optional - may be slow)
print("4. Testing Pexels API...")
try:
    pexels = PexelsAPI()
    videos = pexels.search_videos("nature", per_page=1)
    if videos and len(videos) > 0:
        print(f"   ✅ Found {len(videos)} video(s)\n")
    else:
        print("   ⚠️  No videos found (will try again during generation)\n")
except Exception as e:
    print(f"   ⚠️  Pexels test failed: {e}\n")
    print("   (This is OK - will try again during generation)\n")

# Test 5: Generate video
print("5. Testing video generation...")
print("   Creating short test video (Al-Fatiha, verse 1 only)...\n")

def progress_callback(step, message):
    print(f"   [{step:3d}%] {message}")

try:
    video_path = generator.generate(
        reciter_id="abdul_basit",
        surah_number=1,
        verse_start=1,
        verse_end=1,  # Just one verse for quick test
        progress_callback=progress_callback
    )
    
    if video_path and video_path.exists():
        size_mb = video_path.stat().st_size / (1024 * 1024)
        print(f"\n   ✅ SUCCESS!")
        print(f"   📹 Video: {video_path.name}")
        print(f"   💾 Size: {size_mb:.2f} MB")
        print(f"   📁 Location: {video_path.parent}")
    else:
        print(f"\n   ❌ Video generation failed!")
        print(f"   Check the error messages above for details.")
        exit(1)

except Exception as e:
    print(f"\n   ❌ Exception during generation: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*70)
print("✅ جميع الاختبارات نجحت - ALL TESTS PASSED!")
print("="*70)
print("\nيمكنك الآن استخدام التطبيق بأمان:")
print("You can now use the application safely:")
print("\n  python main.py\n")
