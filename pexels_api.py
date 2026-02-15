import requests
import random
from pathlib import Path
from config import PEXELS_API_KEY, PEXELS_SEARCH_KEYWORDS, PEXELS_VIDEO_ORIENTATION, BACKGROUNDS_DIR


class PexelsAPI:
    """Handler for Pexels API to fetch background videos"""
    
    # كلمات محظورة - إذا ظهرت في tags أو description نرفض الفيديو
    FORBIDDEN_WORDS = [
        # أشخاص
        'people', 'person', 'man', 'woman', 'child', 'human', 'face', 'portrait',
        'crowd', 'group', 'boy', 'girl', 'baby', 'adult', 'hand', 'hands',
        'walking', 'running', 'standing', 'sitting', 'talking', 'dancing',
        
        # حيوانات
        'animal', 'dog', 'cat', 'bird', 'fish', 'horse', 'cow', 'sheep',
        'lion', 'tiger', 'elephant', 'monkey', 'bear', 'deer', 'rabbit',
        'chicken', 'duck', 'goose', 'eagle', 'pigeon', 'butterfly', 'bee',
        'insect', 'spider', 'snake', 'lizard', 'frog', 'wildlife', 'pet',
        'camel', 'goat', 'donkey', 'buffalo',
        
        # كنائس ومعابد غير إسلامية
        'church', 'cathedral', 'chapel', 'temple', 'synagogue', 'pagoda',
        'shrine', 'monastery', 'convent', 'cross', 'crucifix', 'buddha',
        'hindu', 'christian', 'jesus', 'christ', 'mary', 'saint',
        
        # محتوى غير مناسب
        'party', 'club', 'bar', 'alcohol', 'wine', 'beer', 'dance', 'concert',
        'festival', 'celebration', 'wedding', 'bride', 'groom'
    ]
    
    def __init__(self, api_key=PEXELS_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/videos"
        self.headers = {
            "Authorization": api_key
        }
    
    def is_video_safe(self, video_obj):
        """
        فحص إذا كان الفيديو آمن بناءً على tags و description
        
        Returns:
            True إذا كان آمن، False إذا كان يحتوي على محتوى محظور
        """
        # Get tags and description
        tags = video_obj.get('tags', [])
        url = video_obj.get('url', '')
        
        # Convert tags to lowercase text
        tags_text = ' '.join(tags).lower() if tags else ''
        url_text = url.lower()
        
        # Check for forbidden words
        for word in self.FORBIDDEN_WORDS:
            if word in tags_text or word in url_text:
                print(f"      ⚠ Rejected: contains '{word}'")
                return False
        
        return True
    
    def search_videos(self, query, orientation="portrait", size="medium", per_page=15):
        """
        Search for videos on Pexels
        
        Args:
            query: Search keywords
            orientation: portrait, landscape, or square
            size: medium, large, or small
            per_page: Number of results (max 80)
        
        Returns:
            List of video objects
        """
        try:
            params = {
                "query": query,
                "orientation": orientation,
                "size": size,
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
            print(f"Error searching Pexels: {e}")
            return []
    
    def get_video_url(self, video_obj, quality="hd"):
        """
        Extract video URL from Pexels video object
        
        Args:
            video_obj: Video object from Pexels API
            quality: hd, sd, or hls
        
        Returns:
            Video download URL
        """
        video_files = video_obj.get("video_files", [])
        
        # Try to find HD portrait video first
        for vf in video_files:
            if vf.get("quality") == quality and vf.get("width", 0) <= 1080:
                return vf.get("link")
        
        # Fallback to any available video
        if video_files:
            return video_files[0].get("link")
        
        return None
    
    def download_video(self, video_url, output_path):
        """
        Download video from URL
        
        Args:
            video_url: Direct video URL
            output_path: Where to save the video
        
        Returns:
            Path to downloaded file or None
        """
        try:
            response = requests.get(video_url, stream=True, timeout=30)
            response.raise_for_status()
            
            output_path = Path(output_path)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"Downloaded video to {output_path}")
            return output_path
        
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video: {e}")
            return None
    
    def get_random_background(self, output_path=None, max_attempts=10):
        """
        Get a random Islamic/peaceful background video WITH SAFETY FILTERING
        
        Args:
            output_path: Optional path to save video
            max_attempts: Maximum attempts to find safe video
        
        Returns:
            Path to downloaded video or None
        """
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            
            # Select random keyword
            keyword = random.choice(PEXELS_SEARCH_KEYWORDS)
            
            print(f"   🔍 Attempt {attempts}/{max_attempts}: Searching for '{keyword}'")
            videos = self.search_videos(keyword, orientation=PEXELS_VIDEO_ORIENTATION, per_page=20)
            
            if not videos:
                print("      No videos found, trying alternative...")
                keyword = "mountain landscape"
                videos = self.search_videos(keyword, orientation=PEXELS_VIDEO_ORIENTATION, per_page=20)
            
            if not videos:
                print("      Failed to fetch videos")
                continue
            
            # Shuffle and try to find safe video
            random.shuffle(videos)
            
            for video in videos:
                # Check if video is safe
                if not self.is_video_safe(video):
                    continue  # Skip unsafe video
                
                # Video is safe, try to download
                print(f"      ✅ Safe video found: ID {video.get('id')}")
                video_url = self.get_video_url(video, quality="hd")
                
                if not video_url:
                    continue
                
                # Download video
                if output_path is None:
                    output_path = BACKGROUNDS_DIR / f"pexels_{video['id']}.mp4"
                
                result = self.download_video(video_url, output_path)
                if result:
                    return result
        
        print(f"   ❌ Could not find safe video after {max_attempts} attempts")
        return None
    
    def download_random_video(self, save_dir=None, filename=None, max_attempts=10):
        """
        Download a unique random background video WITH SAFETY FILTERING
        
        Args:
            save_dir: Directory to save video (default: BACKGROUNDS_DIR)
            filename: Custom filename (default: pexels_{id}.mp4)
            max_attempts: Maximum attempts to find safe video
        
        Returns:
            Path to downloaded video or None
        """
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            
            keyword = random.choice(PEXELS_SEARCH_KEYWORDS)
            
            print(f"      🔍 Attempt {attempts}/{max_attempts}: {keyword}")
            videos = self.search_videos(keyword, orientation=PEXELS_VIDEO_ORIENTATION, per_page=20)
            
            if not videos:
                videos = self.search_videos("mountain landscape", orientation=PEXELS_VIDEO_ORIENTATION, per_page=20)
            
            if not videos:
                continue
            
            # Shuffle and try to find safe video
            random.shuffle(videos)
            
            for video in videos:
                # Check if video is safe
                if not self.is_video_safe(video):
                    continue
                
                # Safe video found
                print(f"      ✅ Safe video: ID {video.get('id')}")
                video_url = self.get_video_url(video, quality="hd")
                
                if not video_url:
                    continue
                
                if save_dir is None:
                    save_dir = BACKGROUNDS_DIR
                
                save_dir = Path(save_dir)
                
                if filename is None:
                    filename = f"pexels_{video['id']}.mp4"
                
                output_path = save_dir / filename
                
                result = self.download_video(video_url, output_path)
                if result:
                    return result
        
        print(f"      ❌ No safe video found after {max_attempts} attempts")
        return None

    
    def get_cached_or_download(self):
        """
        Use cached video if available, otherwise download new one
        
        Returns:
            Path to background video
        """
        # Check for existing cached videos
        cached_videos = list(BACKGROUNDS_DIR.glob("pexels_*.mp4"))
        
        if cached_videos and len(cached_videos) > 0:
            # Use random cached video
            video_path = random.choice(cached_videos)
            print(f"Using cached background: {video_path}")
            return video_path
        
        # Download new video
        print("No cached videos found, downloading from Pexels...")
        return self.get_random_background()


if __name__ == "__main__":
    # Test the API
    api = PexelsAPI()
    video_path = api.get_random_background()
    if video_path:
        print(f"Success! Video saved to: {video_path}")
    else:
        print("Failed to download video")
