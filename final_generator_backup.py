"""
مُولِّد فيديوهات آيات القرآن - النسخة النهائية
Final Quran Video Generator

المميزات:
- نص عربي نظيف بدون placeholders
- كل آية = فيديو مستقل (ayah_1.mp4, ayah_2.mp4, ...)
- دمج كل الفيديوهات في فيديو نهائي واحد
- تنظيف تلقائي للملفات المؤقتة
"""

import subprocess
import os
import re
from pathlib import Path
from mutagen.mp3 import MP3
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
from quran_api import QuranAPI
from pexels_api import PexelsAPI
from config import (
    TEMP_DIR, OUTPUT_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS,
    AUDIO_BITRATE
)


class FinalVideoGenerator:
    """
    مُولِّد الفيديو النهائي
    Final video generator with clean Arabic text and individual verse videos
    """
    
    def __init__(self):
        self.quran_api = QuranAPI()
        self.pexels_api = PexelsAPI()
        self.temp_dir = TEMP_DIR
        self.output_dir = OUTPUT_DIR
        
        # Check FFmpeg
        self.check_ffmpeg()
    
    def check_ffmpeg(self):
        """Check if FFmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, 
                         encoding='utf-8', 
                         errors='ignore',
                         timeout=5)
            print("✓ FFmpeg found")
            return True
        except FileNotFoundError:
            print("✗ ERROR: FFmpeg not found!")
            print("Download from: https://www.gyan.dev/ffmpeg/builds/")
            return False
    
    def clean_arabic_text(self, text):
        """
        تنظيف النص العربي من أي placeholders أو إضافات
        Clean Arabic text from any placeholders or additions
        
        Args:
            text: Raw Arabic text from API
        
        Returns:
            Clean Arabic text
        """
        # إزالة أي أرقام بين أقواس مربعة مثل [1]
        text = re.sub(r'\[.*?\]', '', text)
        
        # إزالة أي placeholders مثل {الايات}
        text = re.sub(r'\{.*?\}', '', text)
        
        # إزالة مسافات زائدة
        text = ' '.join(text.split())
        
        # إزالة أي أحرف غير عربية أو تشكيل أو مسافات
        # نبقي فقط: الحروف العربية، التشكيل، المسافات، علامات الترقيم العربية
        # text = re.sub(r'[^\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF\s]', '', text)
        
        return text.strip()
    
    def prepare_arabic_text(self, text):
        """
        تحضير النص العربي للعرض الصحيح (RTL + تشكيل)
        Prepare Arabic text for proper display (RTL + reshaping)
        
        Args:
            text: Clean Arabic text
        
        Returns:
            Properly shaped and ordered text for display
        """
        # تنظيف النص أولاً
        clean_text = self.clean_arabic_text(text)
        
        # إعادة تشكيل الحروف العربية (ربط الحروف)
        reshaped_text = arabic_reshaper.reshape(clean_text)
        
        # تطبيق خوارزمية RTL
        bidi_text = get_display(reshaped_text)
        
        return bidi_text
    
    def get_audio_duration(self, audio_path):
        """
        الحصول على مدة ملف الصوت بالثواني
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
            print(f"Warning: Could not get audio duration using mutagen: {e}")
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
                return 5.0  # Default 5 seconds
    
    def create_verse_image(self, text, output_path, width=VIDEO_WIDTH, height=VIDEO_HEIGHT):
        """
        إنشاء صورة للآية بنص عربي صحيح مع التشكيل
        Create image for verse with proper Arabic text and diacritics
        
        Args:
            text: Arabic verse text
            output_path: Where to save the image
            width: Image width
            height: Image height
        
        Returns:
            Path to created image
        """
        output_path = Path(output_path)
        
        # تحضير النص العربي للعرض الصحيح
        display_text = self.prepare_arabic_text(text)
        
        # إنشاء صورة شفافة
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # تحميل خط عربي احترافي يدعم التشكيل الكامل
        # Professional Arabic fonts with full Unicode + diacritics support
        fonts_dir = Path(__file__).parent / "fonts"
        arabic_fonts = [
            # Professional fonts (best quality)
            str(fonts_dir / "Amiri-Regular.ttf"),
            str(fonts_dir / "Scheherazade-Regular.ttf"),
            str(fonts_dir / "NotoNaskhArabic-Regular.ttf"),
            # Windows fonts (fallback)
            "C:\\Windows\\Fonts\\simpo.ttf",
            "C:\\Windows\\Fonts\\tahoma.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
        ]
        
        font = None
        font_size = 70  # حجم مناسب
        
        for font_path in arabic_fonts:
            try:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    print(f"    Using font: {Path(font_path).name}")
                    break
            except Exception as e:
                continue
        
        # إذا لم ينجح أي خط، استخدم الافتراضي
        if font is None:
            try:
                font = ImageFont.truetype("arial", font_size)
            except:
                font = ImageFont.load_default()
                print("    Warning: Using default font (tashkeel may not display)")
        
        # حساب موضع النص (في الثلث السفلي من الشاشة)
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # وضع النص في المنتصف أفقياً، وفي الثلث السفلي عمودياً
        x = (width - text_width) // 2
        y = int(height * 0.70)  # 70% من الأعلى = الثلث السفلي
        
        # رسم النص مع حدود سوداء سميكة للوضوح
        outline_range = 5  # حدود أسمك
        for adj_x in range(-outline_range, outline_range + 1):
            for adj_y in range(-outline_range, outline_range + 1):
                draw.text((x + adj_x, y + adj_y), display_text, 
                         font=font, fill='black')
        
        # رسم النص الأساسي باللون الأبيض
        draw.text((x, y), display_text, font=font, fill='white')
        
        # حفظ الصورة
        img.save(output_path, 'PNG')
        print(f"  ✓ Created image: {output_path.name}")
        
        return output_path

    
    def create_individual_verse_video(self, verse_text, audio_path, output_path, verse_number):
        """
        إنشاء فيديو مستقل لآية واحدة مع فيديو خلفية فريد
        Create individual video for one verse with unique background
        
        Args:
            verse_text: Clean verse text
            audio_path: Path to verse audio
            output_path: Output video path (e.g., ayah_1.mp4)
            verse_number: Verse number for naming
        
        Returns:
            Path to created video or None
        """
        output_path = Path(output_path)
        
        print(f"\n  Creating video for verse {verse_number}...")
        
        # 1. تحميل فيديو خلفية فريد لهذه الآية
        print(f"    Downloading unique background video...")
        background_video = self.pexels_api.download_random_video(
            save_dir=self.temp_dir,
            filename=f"bg_verse_{verse_number}.mp4"
        )
        
        if not background_video:
            print(f"    ⚠️  Failed to download unique background, using cached")
            background_video = self.pexels_api.get_cached_or_download()
        else:
            print(f"    ✓ Unique background downloaded")
        
        # 2. إنشاء صورة الآية
        image_path = self.temp_dir / f"verse_{verse_number}_image.png"
        self.create_verse_image(verse_text, image_path)
        
        # 3. الحصول على مدة الصوت
        duration = self.get_audio_duration(audio_path)
        print(f"    Audio duration: {duration:.2f}s")
        
        # 4. إنشاء الفيديو
        # تكرار الخلفية، إضافة النص، إضافة الصوت
        cmd = [
            'ffmpeg', '-y',
            '-stream_loop', '-1',  # تكرار الخلفية
            '-i', str(background_video),
            '-i', str(audio_path),
            '-i', str(image_path),
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
            '-shortest',  # ينتهي عندما ينتهي الصوت
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True,
                         encoding='utf-8', errors='ignore', timeout=120)
            print(f"    ✓ Video created: {output_path.name}")
            return output_path
        except Exception as e:
            print(f"    ✗ Failed to create video: {e}")
            return None
    
    def merge_videos(self, video_paths, output_path):
        """
        دمج كل الفيديوهات المستقلة في فيديو واحد نهائي
        Merge all individual videos into one final video
        
        Args:
            video_paths: List of video file paths
            output_path: Output final video path
        
        Returns:
            Path to final video or None
        """
        if not video_paths:
            print("No videos to merge!")
            return None
        
        if len(video_paths) == 1:
            # فيديو واحد فقط، نسخه مباشرة
            video_paths[0].rename(output_path)
            print(f"✓ Single video moved to: {output_path.name}")
            return output_path
        
        print(f"\nMerging {len(video_paths)} videos into final video...")
        
        # إنشاء ملف concat لـ FFmpeg
        concat_file = self.temp_dir / "concat_list.txt"
        with open(concat_file, 'w', encoding='utf-8') as f:
            for video_path in video_paths:
                # استخدام مسارات مطلقة مع forward slashes
                abs_path = str(video_path.absolute()).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
        # دمج الفيديوهات
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',  # نسخ بدون إعادة ترميز (أسرع)
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True,
                         encoding='utf-8', errors='ignore', timeout=300)
            print(f"✓ Final video created: {output_path.name}")
            return output_path
        except Exception as e:
            print(f"✗ Failed to merge videos: {e}")
            return None
    
    def cleanup_temp_files(self, keep_final=True):
        """
        تنظيف الملفات المؤقتة
        Cleanup temporary files
        
        Args:
            keep_final: Keep final video (default: True)
        """
        try:
            count = 0
            for file in self.temp_dir.glob("*"):
                if file.is_file():
                    file.unlink()
                    count += 1
            
            print(f"\n✓ Cleaned up {count} temporary files")
        except Exception as e:
            print(f"Warning: Could not clean all temp files: {e}")
    
    def generate(self, reciter_id, surah_number, verse_start, verse_end, progress_callback=None):
        """
        سير العمل الرئيسي لتوليد الفيديو
        Main workflow for video generation
        
        Args:
            reciter_id: معرف القارئ
            surah_number: رقم السورة
            verse_start: رقم الآية الأولى
            verse_end: رقم الآية الأخيرة
            progress_callback: دالة callback للتقدم (اختياري)
        
        Returns:
            مسار الفيديو النهائي أو None
        """
        def update_progress(step, message):
            if progress_callback:
                progress_callback(step, message)
            print(f"[{step}%] {message}")
        
        try:
            print("\n" + "="*70)
            print("Final Video Generation - توليد الفيديو النهائي")
            print(f"  Reciter: {reciter_id}")
            print(f"  Surah: {surah_number}")
            print(f"  Verses: {verse_start}-{verse_end}")
            print("="*70)
            
            # الخطوة 1: جلب نصوص الآيات من API
            update_progress(10, "جاري تحميل نصوص الآيات...")
            verses = self.quran_api.get_verse_text(surah_number, verse_start, verse_end)
            
            if not verses:
                update_progress(0, "فشل تحميل نصوص الآيات")
                return None
            
            print(f"\n✓ Fetched {len(verses)} verses from API")
            
            # الخطوة 2: تحميل ملفات الصوت
            update_progress(20, "جاري تحميل ملفات الصوت...")
            audio_dir = self.temp_dir / f"audio_{surah_number}_{verse_start}_{verse_end}"
            audio_files = self.quran_api.download_verse_range_audio(
                reciter_id, surah_number, verse_start, verse_end, audio_dir
            )
            
            if not audio_files or len(audio_files) != len(verses):
                update_progress(0, "فشل تحميل ملفات الصوت")
                return None
            
            print(f"✓ Downloaded {len(audio_files)} audio files")
            
            # الخطوة 3: تحميل فيديو الخلفية
            update_progress(30, "جاري تحميل فيديو الخلفية...")
            background_video = self.pexels_api.get_cached_or_download()
            
            if not background_video:
                update_progress(0, "فشل تحميل فيديو الخلفية")
                return None
            
            print(f"✓ Background video ready: {background_video.name}")
            
            # الخطوة 4: إنشاء فيديو مستقل لكل آية
            update_progress(40, "جاري إنشاء فيديوهات الآيات المستقلة...")
            
            individual_videos = []
            total_verses = len(verses)
            
            for i, (verse, audio_file) in enumerate(zip(verses, audio_files), 1):
                # تنظيف نص الآية
                clean_text = self.clean_arabic_text(verse['text'])
                
                # اسم الفيديو المستقل
                verse_video_name = f"ayah_{i}.mp4"
                verse_video_path = self.temp_dir / verse_video_name
                
                # إنشاء الفيديو
                video_path = self.create_individual_verse_video(
                    verse_text=clean_text,
                    audio_path=audio_file,
                    output_path=verse_video_path,
                    verse_number=i
                )
                
                if video_path:
                    individual_videos.append(video_path)
                
                # تحديث التقدم
                progress = 40 + int((i / total_verses) * 40)
                update_progress(progress, f"تم إنشاء فيديو الآية {i}/{total_verses}")
            
            if len(individual_videos) != total_verses:
                update_progress(0, "فشل إنشاء بعض الفيديوهات")
                return None
            
            print(f"\n✓ Created {len(individual_videos)} individual verse videos")
            
            # الخطوة 5: دمج كل الفيديوهات في فيديو نهائي واحد
            update_progress(85, "جاري دمج الفيديوهات...")
            
            # بناء اسم الفيديو النهائي
            reciter_name = self.quran_api.get_reciters()[reciter_id]["name_en"].replace(" ", "_")
            surah_name = self.quran_api.get_surahs()[surah_number]
            
            final_filename = f"{reciter_name}_{surah_name}_verses{verse_start}-{verse_end}_FINAL.mp4"
            final_output_path = self.output_dir / final_filename
            
            final_video = self.merge_videos(individual_videos, final_output_path)
            
            if not final_video:
                update_progress(0, "فشل دمج الفيديوهات")
                return None
            
            # الخطوة 6: تنظيف الملفات المؤقتة
            update_progress(95, "جاري تنظيف الملفات المؤقتة...")
            self.cleanup_temp_files()
            
            # النجاح!
            update_progress(100, "تم إنشاء الفيديو بنجاح!")
            
            print("\n" + "="*70)
            print("✓ SUCCESS! Final video created:")
            print(f"  📹 {final_video.name}")
            print(f"  📁 {final_video.parent}")
            file_size = final_video.stat().st_size / (1024 * 1024)
            print(f"  💾 Size: {file_size:.2f} MB")
            print("="*70 + "\n")
            
            return final_video
        
        except Exception as e:
            update_progress(0, f"خطأ: {str(e)}")
            print(f"\n✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    print("Testing Final Video Generator...")
    print("="*70)
    
    generator = FinalVideoGenerator()
    
    def progress(step, msg):
        pass  # التقدم يُطبع تلقائياً
    
    # اختبار: الفاتحة، الآيات 1-3
    video_path = generator.generate(
        reciter_id="abdul_basit",
        surah_number=1,
        verse_start=1,
        verse_end=3,
        progress_callback=progress
    )
    
    if video_path:
        print(f"\n✅ Test successful!")
        print(f"Video: {video_path}")
    else:
        print("\n❌ Test failed!")
