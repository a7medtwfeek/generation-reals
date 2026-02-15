"""
مراجعة وفلترة الفيديوهات الموجودة في مجلد backgrounds
يستخدم AI Vision لفحص الفيديوهات وحذف أي فيديو يحتوي على أشخاص أو حيوانات
"""

import os
import tempfile
import subprocess
from pathlib import Path
import google.generativeai as genai
from PIL import Image

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

from config import BACKGROUNDS_DIR


class VideoReviewer:
    """مراجعة الفيديوهات الموجودة"""
    
    def __init__(self):
        self.model = None
        
        if GEMINI_API_KEY:
            try:
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("✓ Gemini AI Vision initialized")
            except Exception as e:
                print(f"⚠ Could not initialize Gemini: {e}")
    
    def extract_frame(self, video_path, timestamp=2):
        """استخراج إطار من الفيديو"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_frame:
                tmp_frame_path = tmp_frame.name
            
            cmd = [
                'ffmpeg', '-i', str(video_path),
                '-ss', f'00:00:0{timestamp}',
                '-vframes', '1',
                '-q:v', '2',
                '-y',
                tmp_frame_path
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode != 0:
                print(f"      ⚠ FFmpeg error, trying different timestamp...")
                # Try at 0 seconds
                cmd[4] = '00:00:00'
                result = subprocess.run(cmd, capture_output=True)
            
            if os.path.exists(tmp_frame_path) and os.path.getsize(tmp_frame_path) > 0:
                img = Image.open(tmp_frame_path)
                os.unlink(tmp_frame_path)
                return img
            
            return None
        
        except Exception as e:
            print(f"      ❌ Error extracting frame: {e}")
            return None
    
    def analyze_content(self, image):
        """تحليل محتوى الصورة"""
        if not self.model or not image:
            return None
        
        try:
            prompt = """
            Analyze this image carefully and determine:
            1. Are there any humans or people visible? (even partially, in background, or silhouettes)
            2. Are there any animals visible? (including birds, fish, insects, any living creature)
            3. Is this content appropriate for Islamic religious context?
            
            Respond ONLY with a JSON object:
            {
                "has_humans": true/false,
                "has_animals": true/false,
                "is_appropriate": true/false,
                "description": "brief description",
                "confidence": "high/medium/low"
            }
            
            Be VERY strict: if you see ANY sign of humans or animals, mark as true.
            """
            
            response = self.model.generate_content([prompt, image])
            result_text = response.text.strip()
            
            import json
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            return result
        
        except Exception as e:
            print(f"      ⚠ Analysis error: {e}")
            return None
    
    def review_video(self, video_path):
        """مراجعة فيديو واحد"""
        print(f"\n   📹 Reviewing: {video_path.name}")
        
        # Extract frame
        frame = self.extract_frame(video_path)
        if not frame:
            print(f"      ⚠ Could not extract frame - SKIPPING")
            return None
        
        # Analyze
        analysis = self.analyze_content(frame)
        if not analysis:
            print(f"      ⚠ Could not analyze - SKIPPING")
            return None
        
        # Display results
        print(f"      📊 {analysis.get('description', 'N/A')}")
        print(f"      👤 Humans: {analysis.get('has_humans', 'unknown')}")
        print(f"      🐾 Animals: {analysis.get('has_animals', 'unknown')}")
        print(f"      ✓ Appropriate: {analysis.get('is_appropriate', 'unknown')}")
        print(f"      🎯 Confidence: {analysis.get('confidence', 'unknown')}")
        
        has_humans = analysis.get('has_humans', True)
        has_animals = analysis.get('has_animals', True)
        is_appropriate = analysis.get('is_appropriate', False)
        
        is_acceptable = not has_humans and not has_animals and is_appropriate
        
        return {
            'path': video_path,
            'acceptable': is_acceptable,
            'analysis': analysis
        }
    
    def review_all_videos(self, auto_delete=False):
        """مراجعة جميع الفيديوهات"""
        print(f"\n{'='*60}")
        print(f"🔍 Reviewing All Videos in backgrounds/")
        print(f"{'='*60}")
        
        if not self.model:
            print("\n❌ ERROR: Gemini AI not initialized!")
            print("Please set GEMINI_API_KEY environment variable.")
            return
        
        # Get all videos
        videos = list(BACKGROUNDS_DIR.glob("*.mp4"))
        
        if not videos:
            print("\n📭 No videos found in backgrounds/")
            return
        
        print(f"\n📦 Found {len(videos)} videos")
        
        acceptable = []
        rejected = []
        skipped = []
        
        for i, video_path in enumerate(videos, 1):
            print(f"\n{'─'*60}")
            print(f"Video {i}/{len(videos)}")
            
            result = self.review_video(video_path)
            
            if result is None:
                skipped.append(video_path)
                print(f"      ⚠ SKIPPED")
            elif result['acceptable']:
                acceptable.append(video_path)
                print(f"      ✅ ACCEPTABLE")
            else:
                rejected.append(video_path)
                print(f"      ❌ REJECTED")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"📊 REVIEW SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Acceptable: {len(acceptable)}")
        print(f"❌ Rejected: {len(rejected)}")
        print(f"⚠ Skipped: {len(skipped)}")
        
        # Show rejected files
        if rejected:
            print(f"\n❌ REJECTED FILES:")
            for path in rejected:
                print(f"   • {path.name}")
            
            # Ask to delete
            if not auto_delete:
                print(f"\n⚠ Do you want to DELETE rejected files?")
                response = input("Type 'yes' to confirm deletion: ").strip().lower()
                auto_delete = response == 'yes'
            
            if auto_delete:
                print(f"\n🗑️ Deleting rejected files...")
                for path in rejected:
                    try:
                        path.unlink()
                        print(f"   ✓ Deleted: {path.name}")
                    except Exception as e:
                        print(f"   ✗ Failed to delete {path.name}: {e}")
                
                print(f"\n✅ Cleanup complete!")
            else:
                print(f"\n⚠ Rejected files NOT deleted.")
        
        # Show acceptable files
        if acceptable:
            print(f"\n✅ ACCEPTABLE FILES:")
            for path in acceptable:
                print(f"   • {path.name}")


def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("🔍 Video Reviewer - AI Content Analysis")
    print("="*60)
    
    if not GEMINI_API_KEY:
        print("\n❌ ERROR: GEMINI_API_KEY not set!")
        print("\nPlease set your Gemini API key:")
        print("   $env:GEMINI_API_KEY=\"your-api-key-here\"  (PowerShell)")
        print("   set GEMINI_API_KEY=your-api-key-here      (CMD)")
        print("\nGet your free API key at:")
        print("   https://makersuite.google.com/app/apikey")
        return
    
    reviewer = VideoReviewer()
    
    # Ask for auto-delete option
    print("\n⚠ Auto-delete rejected videos?")
    auto_delete = input("Type 'yes' to auto-delete, or press Enter to ask later: ").strip().lower() == 'yes'
    
    reviewer.review_all_videos(auto_delete=auto_delete)
    
    print(f"\n🎉 Review complete!")


if __name__ == "__main__":
    main()
