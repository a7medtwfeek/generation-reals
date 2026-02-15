"""
فلترة فيديوهات Pexels - نسخة بسيطة مع فلترة tags
تستخدم PexelsAPI مع الفلترة التلقائية
"""

from pexels_api import PexelsAPI
from config import PEXELS_SEARCH_KEYWORDS, BACKGROUNDS_DIR
import random


def download_filtered_videos(count=5):
    """تحميل فيديوهات مفلترة"""
    print(f"\n{'='*60}")
    print(f"🎬 Downloading Filtered Pexels Videos")
    print(f"{'='*60}")
    print(f"\n📋 Safety Features:")
    print(f"   ✓ Keyword filtering")
    print(f"   ✓ Tags filtering (no people, animals, churches)")
    print(f"   ✓ Islamic-appropriate content only")
    
    api = PexelsAPI()
    downloaded = []
    
    for i in range(count):
        print(f"\n{'─'*60}")
        print(f"📥 Video {i+1}/{count}")
        print(f"{'─'*60}")
        
        # Use the built-in filtered download
        video_path = api.download_random_video(
            save_dir=BACKGROUNDS_DIR,
            max_attempts=15
        )
        
        if video_path:
            downloaded.append(video_path)
            print(f"   ✅ Success! ({len(downloaded)}/{count})")
        else:
            print(f"   ❌ Failed to find safe video")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Downloaded: {len(downloaded)}/{count} videos")
    print(f"📁 Location: {BACKGROUNDS_DIR}")
    
    if downloaded:
        print(f"\n📋 Files:")
        for path in downloaded:
            print(f"   • {path.name}")
    
    return downloaded


def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("🎬 Simple Pexels Video Downloader")
    print("   (With Automatic Safety Filtering)")
    print("="*60)
    
    # Ask user
    try:
        count = int(input("\n📊 How many videos to download? (default: 5): ") or "5")
    except ValueError:
        count = 5
    
    # Download
    downloaded = download_filtered_videos(count)
    
    if downloaded:
        print(f"\n🎉 Done! {len(downloaded)} videos ready.")
    else:
        print("\n😞 No videos downloaded.")


if __name__ == "__main__":
    main()
