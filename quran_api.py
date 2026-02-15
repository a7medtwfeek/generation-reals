import requests
from pathlib import Path
from urllib.parse import quote
from config import ALQURAN_API, EVERYAYAH_BASE, RECITERS, SURAHS


class QuranAPI:
    """Handler for Quran-related APIs"""
    
    def __init__(self):
        self.alquran_base = ALQURAN_API
        self.everyayah_base = EVERYAYAH_BASE
    
    def get_surahs(self):
        """
        Get list of all Surahs
        
        Returns:
            Dictionary of surah numbers and names
        """
        return SURAHS
    
    def get_reciters(self):
        """
        Get list of available reciters
        
        Returns:
            Dictionary of reciter information
        """
        return RECITERS
    
    def get_verse_text(self, surah_number, verse_start, verse_end):
        """
        Fetch Arabic text for verse(s) from api.alquran.cloud
        
        Args:
            surah_number: Surah number (1-114)
            verse_start: Starting verse number
            verse_end: Ending verse number
        
        Returns:
            List of verse texts with verse numbers
        """
        verses = []
        
        try:
            for verse_num in range(verse_start, verse_end + 1):
                # Fetch verse from API
                url = f"{self.alquran_base}/ayah/{surah_number}:{verse_num}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("code") == 200:
                    verse_data = data.get("data", {})
                    verse_text = verse_data.get("text", "")
                    
                    verses.append({
                        "number": verse_num,
                        "text": verse_text,
                        "surah": surah_number,
                        "surah_name": SURAHS.get(surah_number, "")
                    })
                else:
                    print(f"API error for verse {surah_number}:{verse_num}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching verse text: {e}")
        
        return verses
    
    def get_audio_url(self, reciter_id, surah_number, verse_number):
        """
        Build URL for verse audio from everyayah.com
        
        Args:
            reciter_id: Reciter identifier from RECITERS dict
            surah_number: Surah number (1-114)
            verse_number: Verse number
        
        Returns:
            Audio file URL
        """
        reciter_info = RECITERS.get(reciter_id)
        if not reciter_info:
            return None
        
        folder = reciter_info["folder"]
        
        # Format: surah number (3 digits) + verse number (3 digits)
        file_name = f"{surah_number:03d}{verse_number:03d}.mp3"
        
        # Build URL
        url = f"{self.everyayah_base}/{folder}/{file_name}"
        
        return url
    
    def download_audio(self, reciter_id, surah_number, verse_number, output_path):
        """
        Download audio file for a specific verse
        
        Args:
            reciter_id: Reciter identifier
            surah_number: Surah number
            verse_number: Verse number
            output_path: Where to save the audio file
        
        Returns:
            Path to downloaded file or None
        """
        url = self.get_audio_url(reciter_id, surah_number, verse_number)
        
        if not url:
            print(f"Invalid reciter ID: {reciter_id}")
            return None
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded audio: {output_path.name}")
            return output_path
        
        except requests.exceptions.RequestException as e:
            print(f"Error downloading audio from {url}: {e}")
            return None
    
    def download_verse_range_audio(self, reciter_id, surah_number, verse_start, verse_end, output_dir):
        """
        Download audio files for a range of verses
        
        Args:
            reciter_id: Reciter identifier
            surah_number: Surah number
            verse_start: Starting verse
            verse_end: Ending verse
            output_dir: Directory to save audio files
        
        Returns:
            List of downloaded audio file paths
        """
        audio_files = []
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for verse_num in range(verse_start, verse_end + 1):
            file_name = f"{surah_number:03d}{verse_num:03d}.mp3"
            output_path = output_dir / file_name
            
            downloaded = self.download_audio(reciter_id, surah_number, verse_num, output_path)
            
            if downloaded:
                audio_files.append(downloaded)
            else:
                print(f"Failed to download verse {verse_num}")
        
        return audio_files


if __name__ == "__main__":
    # Test the API
    api = QuranAPI()
    
    # Test verse text
    print("Testing verse text fetch...")
    verses = api.get_verse_text(1, 1, 3)
    for verse in verses:
        print(f"Verse {verse['number']}: {verse['text']}")
    
    # Test audio download
    print("\nTesting audio download...")
    from config import TEMP_DIR
    audio_path = api.download_audio("abdul_basit", 1, 1, TEMP_DIR / "test.mp3")
    if audio_path:
        print(f"Audio downloaded successfully to {audio_path}")
