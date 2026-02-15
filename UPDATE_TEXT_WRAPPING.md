# تحسين create_verse_image في final_generator.py

## التعديل المطلوب:

استبدل دالة `create_verse_image` (السطر 136-216) بالكود التالي:

```python
def create_verse_image(self, text, output_path, width=VIDEO_WIDTH, height=VIDEO_HEIGHT):
    """
    إنشاء صورة للآية بنص عربي صحيح مع التشكيل - خطوط احترافية
    Create image for verse with proper Arabic text and diacritics - professional fonts
    
    Args:
        text: Arabic verse text
        output_path: Where to save the image
        width: Image width
        height: Image height
    
    Returns:
        Path to created image
    """
    output_path = Path(output_path)
    
    # تحضير النص العربي للعرض الصحيح (reshaping + bidi)
    display_text = self.prepare_arabic_text(text)
    
    # إنشاء صورة شفافة
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # تحميل خط عربي احترافي يدعم التشكيل الكامل
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
    font_size = 70
    
    for font_path in arabic_fonts:
        try:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                print(f"    Using font: {Path(font_path).name}")
                break
        except:
            continue
    
    if font is None:
        try:
            font = ImageFont.truetype("arial", font_size)
        except:
            font = ImageFont.load_default()
    
    # تقسيم النص لأسطر (5-6 كلمات كحد أقصى لكل سطر)
    words = display_text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        if len(current_line) >= 6:  # حد أقصى 6 كلمات
            lines.append(' '.join(current_line))
            current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # حساب ارتفاع كل سطر
    line_height = int(font_size * 1.5)
    total_text_height = len(lines) * line_height
    
    # البدء من الثلث السفلي
    start_y = int(height * 0.70) - (total_text_height // 2)
    
    # رسم كل سطر في المنتصف
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        
        x = (width - text_width) // 2
        y = start_y + (i * line_height)
        
        # حدود سوداء
        outline_range = 5
        for adj_x in range(-outline_range, outline_range + 1):
            for adj_y in range(-outline_range, outline_range + 1):
                draw.text((x + adj_x, y + adj_y), line, font=font, fill='black')
        
        # النص الأبيض
        draw.text((x, y), line, font=font, fill='white')
    
    img.save(output_path, 'PNG')
    print(f"  ✓ Created image: {output_path.name} ({len(lines)} lines)")
    
    return output_path
```

## الميزات الجديدة:
- ✅ تقسيم تلقائي للنص (6 كلمات كحد أقصى لكل سطر)
- ✅ كل سطر في المنتصف
- ✅ مسافات مناسبة بين الأسطر
- ✅ النص في الثلث السفلي
