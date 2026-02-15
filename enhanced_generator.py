"""
مُولِّد فيديوهات آيات القرآن - نسخة محسّنة
Enhanced Quran Video Generator with Verse-by-Verse Synchronization

المميزات:
- معالجة صحيحة للنص العربي (RTL + تشكيل)
- كل آية تظهر منفصلة متزامنة مع صوتها
- استخدام ImageMagick للنصوص العربية
- مزامنة دقيقة بين الصور والصوت
"""

import subprocess
import os
import sys
from pathlib import Path
from mutagen.mp3 import MP3
import arabic_reshaper
from bidi.algorithm import get_display
from quran_api import QuranAPI
from pexels_api import PexelsAPI
from config import (
    TEMP_DIR, OUTPUT_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS,
    AUDIO_BITRATE
)


class EnhancedVideoGenerator:
    """
    مُولِّد فيديو محسّن مع مزامنة الآيات
    Enhanced video generator with verse synchronization
    """
    
    def __init__(self):
        self.quran_api = QuranAPI()
        self.pexels_api = PexelsAPI()
        self.temp_dir = TEMP_DIR
        self.output_dir = OUTPUT_DIR
        
        # Check dependencies
        self.check_dependencies()
    
    def check_dependencies(self):
        """Check if FFmpeg and ImageMagick are available"""
        # Check FFmpeg
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, 
                         encoding='utf-8', 
                         errors='ignore',
                         timeout=5)
            print("✓ FFmpeg found")
        except FileNotFoundError:
            print("✗ ERROR: FFmpeg not found!")
            print("Download from: https://www.gyan.dev/ffmpeg/builds/")
        
        # Check ImageMagick
        try:
            subprocess.run(['magick', '-version'], 
                         capture_output=True,
                         encoding='utf-8',
                         errors='ignore',
                         timeout=5)
            print("✓ ImageMagick found")
        except FileNotFoundError:
            print("⚠️  ImageMagick not found - will use Pillow instead")
            print("For better Arabic text: https://imagemagick.org/script/download.php")
    
    def get_audio_duration(self, audio_path):
        """
        Get duration of audio file in seconds
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Duration in seconds (float)
        """
        try:
            audio = MP3(str(audio_path))
            return audio.info.length
        except Exception as e:
            print(f"Warning: Could not get audio duration: {e}")
            # Fallback: use ffprobe
            try:
                cmd = [
                    'ffprobe', '-v', 'error',
                    '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1',
                    str(audio_path)
                ]
                result = subprocess.run(cmd, capture_output=True, 
                                      encoding='utf-8', errors='ignore')
                return float(result.stdout.strip())
            except:
                return 5.0  # Default 5 seconds if all else fails
    
    def prepare_arabic_text(self, text):
        """
        Prepare Arabic text for proper display (RTL + reshaping)
        
        Args:
            text: Arabic text
        
        Returns:
            Properly shaped and ordered text for display
        """
        # Reshape Arabic text (connect letters properly)
        reshaped_text = arabic_reshaper.reshape(text)
        
        # Apply bidirectional algorithm for RTL
        bidi_text = get_display(reshaped_text)
        
        return bidi_text
    
    def create_verse_image_imagemagick(self, text, output_path, width=VIDEO_WIDTH, height=VIDEO_HEIGHT):
        """
        Create image with Arabic text using ImageMagick
        
        Args:
            text: Arabic text to display
            output_path: Where to save the image
            width: Image width
            height: Image height
        
        Returns:
            Path to created image
        """
        output_path = Path(output_path)
        
        # Prepare Arabic text for proper display
        display_text = self.prepare_arabic_text(text)
        
        # ImageMagick command
        # Using -gravity center for centering
        # -direction right-to-left for RTL
        cmd = [
            'magick',
            '-size', f'{width}x{height}',
            'xc:transparent',  # Transparent background
            '-font', 'Arial',  # Use system Arabic font
            '-pointsize', '60',
            '-fill', 'white',
            '-stroke', 'black',
            '-strokewidth', '2',
            '-gravity', 'center',
            '-annotate', '+0+0', display_text,
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True,
                         encoding='utf-8', errors='ignore')
            print(f"✓ Created image with ImageMagick: {output_path.name}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"ImageMagick failed, falling back to Pillow")
            return self.create_verse_image_pillow(text, output_path, width, height)
        except FileNotFoundError:
            print("ImageMagick not found, using Pillow")
            return self.create_verse_image_pillow(text, output_path, width, height)
    
    def create_verse_image_pillow(self, text, output_path, width=VIDEO_WIDTH, height=VIDEO_HEIGHT):
        """
        Create image with Arabic text using Pillow (fallback)
        
        Args:
            text: Arabic text to display
            output_path: Where to save the image
            width: Image width
            height: Image height
        
        Returns:
            Path to created image
        """
        from PIL import Image, ImageDraw, ImageFont
        
        output_path = Path(output_path)
        
        # Prepare Arabic text for proper display
        display_text = self.prepare_arabic_text(text)
        
        # Create transparent image
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center position
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw text with outline
        outline_range = 3
        for adj_x in range(-outline_range, outline_range + 1):
            for adj_y in range(-outline_range, outline_range + 1):
                draw.text((x + adj_x, y + adj_y), display_text, 
                         font=font, fill='black')
        
        # Draw main text
        draw.text((x, y), display_text, font=font, fill='white')
        
        # Save
        img.save(output_path, 'PNG')
        print(f"✓ Created image with Pillow: {output_path.name}")
        
        return output_path
    
    def create_verse_images(self, verses, audio_files):
        """
        Create individual images for each verse
        
        Args:
            verses: List of verse dictionaries
            audio_files: List of audio file paths
        
        Returns:
            List of tuples (image_path, duration)
        """
        verse_data = []
        
        for i, (verse, audio_file) in enumerate(zip(verses, audio_files)):
            # Get audio duration
            duration = self.get_audio_duration(audio_file)
            
            # Create verse text
            verse_text = f"﴿ {verse['text']} ﴾\n[{verse['number']}]"
            
            # Create image
            image_path = self.temp_dir / f"verse_{verse['surah']}_{verse['number']}.png"
            
            # Try ImageMagick first, fallback to Pillow
            self.create_verse_image_imagemagick(verse_text, image_path)
            
            verse_data.append({
                'image': image_path,
                'audio': audio_file,
                'duration': duration,
                'verse_number': verse['number']
            })
            
            print(f"  Verse {verse['number']}: {duration:.2f}s")
        
        return verse_data
    
    def create_video_with_verse_sync(self, background_video, verse_data, output_path):
        """
        Create video with verse-by-verse synchronization
        
        Args:
            background_video: Path to background video
            verse_data: List of dicts with image, audio, duration
            output_path: Output video path
        
        Returns:
            Path to created video
        """
        output_path = Path(output_path)
        
        print("Creating synchronized video...")
        print(f"  Background: {background_video.name if isinstance(background_video, Path) else background_video}")
        print(f"  Verses: {len(verse_data)}")
        
        # Step 1: Create individual verse videos
        verse_videos = []
        for i, vdata in enumerate(verse_data):
            verse_video = self.temp_dir / f"verse_video_{i}.mp4"
            
            # Create video for this verse
            # Loop background, overlay text, add audio, set duration
            cmd = [
                'ffmpeg', '-y',
                '-stream_loop', '-1',
                '-i', str(background_video),
                '-i', str(vdata['audio']),
                '-i', str(vdata['image']),
                '-filter_complex',
                f'[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,'
                f'crop={VIDEO_WIDTH}:{VIDEO_HEIGHT}[bg];'
                f'[bg][2:v]overlay=(W-w)/2:(H-h)/2[outv]',
                '-map', '[outv]',
                '-map', '1:a',
                '-c:v', 'mpeg4',
                '-q:v', '3',
                '-c:a', 'aac',
                '-b:a', AUDIO_BITRATE,
                '-r', str(VIDEO_FPS),
                '-shortest',  # End when audio ends
                str(verse_video)
            ]
            
            try:
                subprocess.run(cmd, check=True, capture_output=True,
                             encoding='utf-8', errors='ignore', timeout=120)
                verse_videos.append(verse_video)
                print(f"  ✓ Created verse {i+1} video")
            except Exception as e:
                print(f"  ✗ Failed to create verse {i+1} video: {e}")
                return None
        
        # Step 2: Concatenate all verse videos
        if len(verse_videos) == 1:
            # Only one verse, just rename
            verse_videos[0].rename(output_path)
            print(f"✓ Video created: {output_path.name}")
            return output_path
        
        # Create concat file
        concat_file = self.temp_dir / "concat_videos.txt"
        with open(concat_file, 'w', encoding='utf-8') as f:
            for vv in verse_videos:
                f.write(f"file '{vv.absolute()}'\n")
        
        # Concatenate
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True,
                         encoding='utf-8', errors='ignore', timeout=300)
            print(f"✓ Final video created: {output_path.name}")
            return output_path
        except Exception as e:
            print(f"✗ Failed to concatenate videos: {e}")
            return None
    
    def generate(self, reciter_id, surah_number, verse_start, verse_end, progress_callback=None):
        """
        Main generation workflow with verse synchronization
        
        Args:
            reciter_id: Reciter identifier
            surah_number: Surah number
            verse_start: Starting verse
            verse_end: Ending verse
            progress_callback: Optional callback function(step, message)
        
        Returns:
            Path to generated video or None
        """
        def update_progress(step, message):
            if progress_callback:
                progress_callback(step, message)
            print(f"[{step}%] {message}")
        
        try:
            print("\n" + "="*70)
            print(f"Enhanced Video Generation:")
            print(f"  Reciter: {reciter_id}")
            print(f"  Surah: {surah_number}")
            print(f"  Verses: {verse_start}-{verse_end}")
            print("="*70 + "\n")
            
            # Step 1: Fetch verse texts
            update_progress(10, "جاري تحميل نصوص الآيات...")
            verses = self.quran_api.get_verse_text(surah_number, verse_start, verse_end)
            
            if not verses:
                update_progress(0, "فشل تحميل نصوص الآيات")
                return None
            
            print(f"✓ Fetched {len(verses)} verses")
            
            # Step 2: Download audio files
            update_progress(25, "جاري تحميل ملفات الصوت...")
            audio_dir = self.temp_dir / f"audio_{surah_number}_{verse_start}_{verse_end}"
            audio_files = self.quran_api.download_verse_range_audio(
                reciter_id, surah_number, verse_start, verse_end, audio_dir
            )
            
            if not audio_files:
                update_progress(0, "فشل تحميل ملفات الصوت")
                return None
            
            print(f"✓ Downloaded {len(audio_files)} audio files")
            
            # Step 3: Get background video
            update_progress(40, "جاري تحميل فيديو الخلفية...")
            background_video = self.pexels_api.get_cached_or_download()
            
            if not background_video:
                update_progress(0, "فشل تحميل فيديو الخلفية")
                return None
            
            print(f"✓ Background video ready")
            
            # Step 4: Create verse images with duration info
            update_progress(55, "جاري إنشاء صور الآيات...")
            verse_data = self.create_verse_images(verses, audio_files)
            
            if not verse_data:
                update_progress(0, "فشل إنشاء صور الآيات")
                return None
            
            print(f"✓ Created {len(verse_data)} verse images")
            
            # Step 5: Create synchronized video
            update_progress(75, "جاري إنشاء الفيديو المتزامن...")
            
            # Build output filename
            reciter_name = self.quran_api.get_reciters()[reciter_id]["name_en"].replace(" ", "_")
            surah_name = self.quran_api.get_surahs()[surah_number]
            
            output_filename = f"{reciter_name}_{surah_name}_verse{verse_start}-{verse_end}_synced.mp4"
            output_path = self.output_dir / output_filename
            
            final_video = self.create_video_with_verse_sync(
                background_video,
                verse_data,
                output_path
            )
            
            if final_video:
                update_progress(100, "تم إنشاء الفيديو بنجاح!")
                print(f"\n{'='*70}")
                print(f"✓ SUCCESS! Synchronized video created:")
                print(f"  {final_video}")
                print(f"{'='*70}\n")
                return final_video
            else:
                update_progress(0, "فشل إنشاء الفيديو النهائي")
                return None
        
        except Exception as e:
            update_progress(0, f"خطأ: {str(e)}")
            print(f"\n✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def cleanup_temp_files(self):
        """Remove temporary files"""
        try:
            count = 0
            for file in self.temp_dir.glob("*"):
                if file.is_file():
                    file.unlink()
                    count += 1
            print(f"Cleaned up {count} temporary files")
        except Exception as e:
            print(f"Error cleaning temp files: {e}")


if __name__ == "__main__":
    print("Testing Enhanced Video Generator...")
    generator = EnhancedVideoGenerator()
    
    def progress(step, msg):
        print(f"Progress: {step}% - {msg}")
    
    video_path = generator.generate(
        reciter_id="abdul_basit",
        surah_number=1,  # Al-Fatiha
        verse_start=1,
        verse_end=3,
        progress_callback=progress
    )
    
    if video_path:
        print(f"\n✓ Video generated: {video_path}")
    else:
        print("\n✗ Video generation failed")
