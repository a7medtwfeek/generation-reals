"""
فلترة فيديوهات Pexels باستخدام AI Vision
يستبعد الفيديوهات التي تحتوي على:
- أشخاص
- حيوانات
- محتوى غير متوافق مع الشريعة الإسلامية

يقبل فقط:
- مناظر طبيعية
- مساجد إسلامية
- مناظر سماوية (غيوم، نجوم، إلخ)
"""

import requests
import random
import os
import tempfile
import subprocess
from pathlib import Path
from config import PEXELS_API_KEY, BACKGROUNDS_DIR
import google.generativeai as genai
from PIL import Image
import io

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# كلمات البحث المفلترة - مناظر طبيعية ومساجد فقط
FILTERED_KEYWORDS = [
    "mosque architecture",
    "islamic mosque",
    "masjid",
    "nature landscape",
    "mountain scenery",
    "ocean waves",
    "clouds sky",
    "sunset sky",
    "stars night sky",
    "forest nature",
    "waterfall nature",
    "desert landscape",
    "northern lights",
    "milky way stars"
]


class VideoFilterAPI:
    """فلترة الفيديوهات باستخدام AI Vision"""
    
    def __init__(self, api_key=PEXELS_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/videos"
        self.headers = {"Authorization": api_key}
        self.model = None
        
        # Initialize Gemini model if API key is available
        if GEMINI_API_KEY:
            try:
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("✓ Gemini AI Vision initialized")
            except Exception as e:
                print(f"⚠ Could not initialize Gemini: {e}")
    
    def search_videos(self, query, orientation="portrait", per_page=20):
        """البحث عن فيديوهات في Pexels"""
        try:
            params = {
                "query": query,
                "orientation": orientation,
                "per_page": per_page
            }
            
            response = requests.get(
                f"{self.base_url}/search",
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            data = response.json()
            return data.get("videos", [])
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching Pexels: {e}")
            return []
    
    def extract_frame_from_video(self, video_url):
        """استخراج إطار من الفيديو للتحليل"""
        try:
            # Download a small portion of the video
            response = requests.get(video_url, stream=True, timeout=15)
            response.raise_for_status()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video:
                # Download only first 2MB for speed
                downloaded = 0
                max_size = 2 * 1024 * 1024  # 2MB
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp_video.write(chunk)
                        downloaded += len(chunk)
                        if downloaded >= max_size:
                            break
                
                tmp_video_path = tmp_video.name
            
            # Extract frame using ffmpeg
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_frame:
                tmp_frame_path = tmp_frame.name
            
            # Extract frame at 2 seconds
            cmd = [
                'ffmpeg', '-i', tmp_video_path,
                '-ss', '00:00:02',
                '-vframes', '1',
                '-q:v', '2',
                '-y',
                tmp_frame_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            # Load image
            img = Image.open(tmp_frame_path)
            
            # Cleanup
            os.unlink(tmp_video_path)
            os.unlink(tmp_frame_path)
            
            return img
        
        except Exception as e:
            print(f"⚠ Error extracting frame: {e}")
            return None
    
    def analyze_video_content(self, image):
        """تحليل محتوى الفيديو باستخدام AI Vision"""
        if not self.model or not image:
            return None
        
        try:
            prompt = """
            Analyze this image and determine if it contains:
            1. Any humans or people (even partially visible)
            2. Any animals (including birds, fish, insects, etc.)
            3. Any inappropriate content for Islamic context
            
            Respond ONLY with a JSON object in this exact format:
            {
                "has_humans": true/false,
                "has_animals": true/false,
                "is_appropriate": true/false,
                "description": "brief description of what you see",
                "category": "mosque/nature/sky/water/mountain/other"
            }
            
            Be very strict: if you see ANY sign of humans or animals, mark it as true.
            """
            
            response = self.model.generate_content([prompt, image])
            result_text = response.text.strip()
            
            # Extract JSON from response
            import json
            # Remove markdown code blocks if present
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            return result
        
        except Exception as e:
            print(f"⚠ Error analyzing content: {e}")
            return None
    
    def is_video_acceptable(self, video_obj):
        """التحقق من قبول الفيديو"""
        try:
            # Get video URL
            video_files = video_obj.get("video_files", [])
            if not video_files:
                return False
            
            # Find a suitable quality video
            video_url = None
            for vf in video_files:
                if vf.get("quality") in ["hd", "sd"] and vf.get("width", 0) <= 1080:
                    video_url = vf.get("link")
                    break
            
            if not video_url and video_files:
                video_url = video_files[0].get("link")
            
            if not video_url:
                return False
            
            print(f"   📹 Analyzing video ID: {video_obj.get('id')}...")
            
            # Extract frame
            frame = self.extract_frame_from_video(video_url)
            if not frame:
                print("   ⚠ Could not extract frame, skipping...")
                return False
            
            # Analyze content
            analysis = self.analyze_video_content(frame)
            if not analysis:
                print("   ⚠ Could not analyze content, skipping...")
                return False
            
            # Check criteria
            has_humans = analysis.get("has_humans", True)
            has_animals = analysis.get("has_animals", True)
            is_appropriate = analysis.get("is_appropriate", False)
            
            print(f"   📊 Analysis: {analysis.get('description', 'N/A')}")
            print(f"   👤 Humans: {has_humans} | 🐾 Animals: {has_animals} | ✓ Appropriate: {is_appropriate}")
            
            # Accept only if no humans, no animals, and appropriate
            is_acceptable = not has_humans and not has_animals and is_appropriate
            
            if is_acceptable:
                print(f"   ✅ ACCEPTED - Category: {analysis.get('category', 'unknown')}")
            else:
                print(f"   ❌ REJECTED")
            
            return is_acceptable
        
        except Exception as e:
            print(f"   ❌ Error checking video: {e}")
            return False
    
    def download_video(self, video_url, output_path):
        """تحميل الفيديو"""
        try:
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            output_path = Path(output_path)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"   💾 Downloaded to: {output_path.name}")
            return output_path
        
        except Exception as e:
            print(f"   ❌ Download error: {e}")
            return None
    
    def get_filtered_video(self, max_attempts=10):
        """الحصول على فيديو مفلتر"""
        keyword = random.choice(FILTERED_KEYWORDS)
        print(f"\n🔍 Searching for: '{keyword}'")
        
        videos = self.search_videos(keyword, orientation="portrait", per_page=20)
        
        if not videos:
            print("❌ No videos found")
            return None
        
        print(f"📦 Found {len(videos)} videos, filtering...")
        
        # Shuffle to get variety
        random.shuffle(videos)
        
        attempts = 0
        for video in videos:
            if attempts >= max_attempts:
                print(f"⚠ Reached max attempts ({max_attempts})")
                break
            
            attempts += 1
            print(f"\n🔄 Attempt {attempts}/{max_attempts}")
            
            if self.is_video_acceptable(video):
                # Download the video
                video_files = video.get("video_files", [])
                video_url = None
                
                for vf in video_files:
                    if vf.get("quality") == "hd" and vf.get("width", 0) <= 1080:
                        video_url = vf.get("link")
                        break
                
                if not video_url and video_files:
                    video_url = video_files[0].get("link")
                
                if video_url:
                    output_path = BACKGROUNDS_DIR / f"pexels_{video['id']}.mp4"
                    downloaded = self.download_video(video_url, output_path)
                    if downloaded:
                        return downloaded
        
        print("\n❌ Could not find acceptable video after all attempts")
        return None
    
    def download_multiple_filtered_videos(self, count=5):
        """تحميل عدة فيديوهات مفلترة"""
        print(f"\n{'='*60}")
        print(f"🎯 Starting filtered video download: {count} videos")
        print(f"{'='*60}")
        
        downloaded = []
        
        for i in range(count):
            print(f"\n{'─'*60}")
            print(f"📥 Downloading video {i+1}/{count}")
            print(f"{'─'*60}")
            
            video_path = self.get_filtered_video(max_attempts=15)
            
            if video_path:
                downloaded.append(video_path)
                print(f"\n✅ Success! Total downloaded: {len(downloaded)}/{count}")
            else:
                print(f"\n⚠ Failed to download video {i+1}")
        
        print(f"\n{'='*60}")
        print(f"📊 SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successfully downloaded: {len(downloaded)}/{count}")
        print(f"📁 Location: {BACKGROUNDS_DIR}")
        
        if downloaded:
            print(f"\n📋 Downloaded files:")
            for path in downloaded:
                print(f"   • {path.name}")
        
        return downloaded


def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("🎬 Pexels Video Filter - Islamic Content Only")
    print("="*60)
    print("\n📋 Filter Criteria:")
    print("   ✓ No humans")
    print("   ✓ No animals")
    print("   ✓ Nature landscapes only")
    print("   ✓ Islamic mosques only")
    print("   ✓ Shariah-compliant content")
    
    # Check if Gemini API key is set
    if not GEMINI_API_KEY:
        print("\n⚠ WARNING: GEMINI_API_KEY not set!")
        print("Please set your Gemini API key:")
        print("   export GEMINI_API_KEY='your-api-key-here'")
        print("\nGet your free API key at: https://makersuite.google.com/app/apikey")
        return
    
    # Initialize filter
    filter_api = VideoFilterAPI()
    
    # Ask user how many videos to download
    try:
        count = int(input("\n📊 How many filtered videos to download? (default: 5): ") or "5")
    except ValueError:
        count = 5
    
    # Download filtered videos
    downloaded = filter_api.download_multiple_filtered_videos(count)
    
    if downloaded:
        print(f"\n🎉 Done! {len(downloaded)} videos ready for use.")
    else:
        print("\n😞 No videos were downloaded. Please try again.")


if __name__ == "__main__":
    main()
