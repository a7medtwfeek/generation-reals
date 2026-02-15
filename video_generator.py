import subprocess
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap
from quran_api import QuranAPI
from pexels_api import PexelsAPI
from config import (
    TEMP_DIR, OUTPUT_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS,
    VIDEO_BITRATE, AUDIO_BITRATE, TEXT_FONT_SIZE, TEXT_COLOR,
    TEXT_PADDING, ARABIC_FONTS
)


class VideoGenerator:
    """Generate Quran verse videos with background, audio, and text overlays"""
    
    def __init__(self):
        self.quran_api = QuranAPI()
        self.pexels_api = PexelsAPI()
        self.temp_dir = TEMP_DIR
        self.output_dir = OUTPUT_DIR
        
        # Check FFmpeg availability
        self.check_ffmpeg()
    
    def check_ffmpeg(self):
        """Check if FFmpeg is available"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, 
                                  encoding='utf-8',
                                  errors='ignore',
                                  timeout=5)
            print("✓ FFmpeg found")
            return True
        except FileNotFoundError:
            print("✗ ERROR: FFmpeg not found!")
            print("Please install FFmpeg:")
            print("1. Download from: https://www.gyan.dev/ffmpeg/builds/")
            print("2. Extract to C:\\ffmpeg")
            print("3. Add C:\\ffmpeg\\bin to PATH")
            print("4. Restart terminal")
            return False
        except Exception as e:
            print(f"Warning: Could not check FFmpeg: {e}")
            return False
    
    def find_arabic_font(self):
        """Find available Arabic font on system"""
        for font in ARABIC_FONTS:
            try:
                if os.path.exists(font):
                    print(f"Using font: {font}")
                    return font
                # Try as font name
                ImageFont.truetype(font, TEXT_FONT_SIZE)
                print(f"Using font: {font}")
                return font
            except:
                continue
        
        # Fallback to default
        print("Warning: Using default font (Arabic may not render correctly)")
        return "arial"
    
    def create_text_overlay(self, text, output_path, width=VIDEO_WIDTH, height=VIDEO_HEIGHT):
        """
        Create an image with Arabic text overlay
        
        Args:
            text: Arabic text to display
            output_path: Where to save the image
            width: Image width
            height: Image height
        
        Returns:
            Path to created image
        """
        print(f"Creating text overlay...")
        
        # Create transparent image
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Load Arabic font
        font_path = self.find_arabic_font()
        try:
            font = ImageFont.truetype(font_path, TEXT_FONT_SIZE)
        except Exception as e:
            print(f"Warning: Could not load font {font_path}: {e}")
            try:
                # Try system default
                font = ImageFont.truetype("arial", TEXT_FONT_SIZE)
            except:
                font = ImageFont.load_default()
        
        # Split text into lines
        lines = text.split('\n')
        
        # Calculate total height
        total_height = 0
        line_dimensions = []
        for line in lines:
            if line.strip():
                # Use anchor parameter for better text rendering
                bbox = draw.textbbox((0, 0), line, font=font, anchor="mm")
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                line_dimensions.append((line, line_width, line_height))
                total_height += line_height + 20
        
        # Start position (center vertically)
        y_position = (height - total_height) // 2
        
        for line, line_width, line_height in line_dimensions:
            # Center horizontally
            x_position = (width - line_width) // 2
            
            # Draw text with outline for better visibility
            outline_range = 3
            for adj_x in range(-outline_range, outline_range + 1):
                for adj_y in range(-outline_range, outline_range + 1):
                    draw.text((x_position + adj_x, y_position + adj_y), 
                             line, font=font, fill='black', anchor="mm")
            
            # Draw main text
            draw.text((x_position, y_position), line, font=font, fill='white', anchor="mm")
            
            y_position += line_height + 20
        
        # Save image
        output_path = Path(output_path)
        img.save(output_path, 'PNG')
        print(f"✓ Text overlay created: {output_path.name}")
        
        return output_path
    
    def merge_audio_files(self, audio_files, output_path):
        """
        Concatenate multiple audio files into one
        
        Args:
            audio_files: List of audio file paths
            output_path: Output audio file path
        
        Returns:
            Path to merged audio file
        """
        if len(audio_files) == 1:
            print("Single audio file, no merge needed")
            return audio_files[0]
        
        print(f"Merging {len(audio_files)} audio files...")
        
        # Create concat file for FFmpeg
        concat_file = self.temp_dir / "concat_list.txt"
        
        with open(concat_file, 'w', encoding='utf-8') as f:
            for audio_file in audio_files:
                # Use forward slashes for FFmpeg on Windows
                audio_path = str(audio_file.absolute()).replace('\\', '/')
                f.write(f"file '{audio_path}'\n")
        
        # Merge using FFmpeg
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            str(output_path)
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, 
                                  encoding='utf-8', errors='ignore')
            print(f"✓ Merged {len(audio_files)} audio files")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"✗ Error merging audio:")
            print(f"Command: {' '.join(cmd)}")
            stderr_output = e.stderr if e.stderr else "(No error message)"
            print(f"STDERR: {stderr_output}")
            return None
        except FileNotFoundError:
            print("✗ ERROR: FFmpeg not found!")
            print("Please install FFmpeg and add it to PATH")
            return None
    
    def create_video(self, background_video, audio_file, text_overlay, output_path, duration=None):
        """
        Create final video by combining background, audio, and text
        
        Args:
            background_video: Path to background video
            audio_file: Path to audio file
            text_overlay: Path to text overlay image (PNG with transparency)
            output_path: Output video path
            duration: Optional duration (if None, uses audio duration)
        
        Returns:
            Path to created video
        """
        output_path = Path(output_path)
        
        print("Creating final video...")
        print(f"  Background: {background_video.name if isinstance(background_video, Path) else background_video}")
        print(f"  Audio: {audio_file.name if isinstance(audio_file, Path) else audio_file}")
        print(f"  Text overlay: {text_overlay.name if isinstance(text_overlay, Path) else text_overlay}")
        
        # FFmpeg command
        cmd = [
            'ffmpeg', '-y',
            '-stream_loop', '-1',  # Loop background video
            '-i', str(background_video),
            '-i', str(audio_file),
            '-i', str(text_overlay),
            '-filter_complex',
            f'[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,crop={VIDEO_WIDTH}:{VIDEO_HEIGHT}[bg];'
            f'[bg][2:v]overlay=(W-w)/2:(H-h)/2[outv]',
            '-map', '[outv]',
            '-map', '1:a',
            '-c:v', 'mpeg4',  # Use mpeg4 instead of libx264 (available in all FFmpeg builds)
            '-q:v', '3',  # Quality (1-31, lower is better, 3 is high quality)
            '-c:a', 'aac',
            '-b:a', AUDIO_BITRATE,
            '-r', str(VIDEO_FPS),
            '-shortest',  # End when audio ends
            '-movflags', '+faststart',
            str(output_path)
        ]
        
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, 
                                  encoding='utf-8', errors='ignore', timeout=300)
            print(f"✓ Video created successfully: {output_path.name}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"✗ FFmpeg error:")
            # Safely get stderr - may be None if encoding failed
            stderr_output = e.stderr if e.stderr else "(No error message - encoding issue)"
            print(f"STDERR: {stderr_output}")
            
            # Check for common errors only if stderr is available
            if e.stderr:
                if "does not contain any stream" in e.stderr:
                    print("\nPossible issue: Background video might be corrupted or empty")
                elif "No such filter" in e.stderr:
                    print("\nPossible issue: FFmpeg version might be outdated")
            return None
        except FileNotFoundError:
            print("✗ ERROR: FFmpeg not found!")
            return None
        except subprocess.TimeoutExpired:
            print("✗ ERROR: FFmpeg took too long (>5 minutes). Process killed.")
            return None

    
    def generate(self, reciter_id, surah_number, verse_start, verse_end, progress_callback=None):
        """
        Main generation workflow
        
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
            print("\n" + "="*60)
            print(f"Starting video generation:")
            print(f"  Reciter: {reciter_id}")
            print(f"  Surah: {surah_number}")
            print(f"  Verses: {verse_start}-{verse_end}")
            print("="*60 + "\n")
            
            # Step 1: Fetch verse texts
            update_progress(10, "جاري تحميل نصوص الآيات...")
            verses = self.quran_api.get_verse_text(surah_number, verse_start, verse_end)
            
            if not verses:
                update_progress(0, "فشل تحميل نصوص الآيات")
                print("✗ Failed to fetch verse texts from API")
                return None
            
            print(f"✓ Fetched {len(verses)} verses")
            
            # Combine verse texts
            full_text = "\n\n".join([
                f"﴿ {verse['text']} ﴾ [{verse['number']}]"
                for verse in verses
            ])
            
            # Step 2: Download audio files
            update_progress(25, "جاري تحميل ملفات الصوت...")
            audio_dir = self.temp_dir / f"audio_{surah_number}_{verse_start}_{verse_end}"
            audio_files = self.quran_api.download_verse_range_audio(
                reciter_id, surah_number, verse_start, verse_end, audio_dir
            )
            
            if not audio_files:
                update_progress(0, "فشل تحميل ملفات الصوت")
                print("✗ Failed to download audio files")
                return None
            
            print(f"✓ Downloaded {len(audio_files)} audio files")
            
            # Step 3: Merge audio files
            update_progress(40, "جاري دمج ملفات الصوت...")
            merged_audio = self.temp_dir / f"merged_audio_{surah_number}_{verse_start}_{verse_end}.mp3"
            final_audio = self.merge_audio_files(audio_files, merged_audio)
            
            if not final_audio:
                update_progress(0, "فشل دمج ملفات الصوت")
                return None
            
            # Step 4: Get background video
            update_progress(55, "جاري تحميل فيديو الخلفية...")
            background_video = self.pexels_api.get_cached_or_download()
            
            if not background_video:
                update_progress(0, "فشل تحميل فيديو الخلفية")
                print("✗ Failed to get background video")
                return None
            
            print(f"✓ Background video ready")
            
            # Step 5: Create text overlay
            update_progress(70, "جاري إنشاء النص...")
            text_overlay = self.temp_dir / f"text_overlay_{surah_number}_{verse_start}_{verse_end}.png"
            self.create_text_overlay(full_text, text_overlay)
            
            # Step 6: Create final video
            update_progress(85, "جاري إنشاء الفيديو النهائي...")
            
            # Build output filename
            reciter_name = self.quran_api.get_reciters()[reciter_id]["name_en"].replace(" ", "_")
            surah_name = self.quran_api.get_surahs()[surah_number]
            
            output_filename = f"{reciter_name}_{surah_name}_verse{verse_start}-{verse_end}.mp4"
            output_path = self.output_dir / output_filename
            
            final_video = self.create_video(
                background_video,
                final_audio,
                text_overlay,
                output_path
            )
            
            if final_video:
                update_progress(100, "تم إنشاء الفيديو بنجاح!")
                print(f"\n{'='*60}")
                print(f"✓ SUCCESS! Video created:")
                print(f"  {final_video}")
                print(f"{'='*60}\n")
                return final_video
            else:
                update_progress(0, "فشل إنشاء الفيديو النهائي")
                return None
        
        except Exception as e:
            update_progress(0, f"خطأ: {str(e)}")
            print(f"\n✗ ERROR in generate: {e}")
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
    # Test video generation
    print("Testing Video Generator...")
    generator = VideoGenerator()
    
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
