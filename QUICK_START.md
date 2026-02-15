# 🚀 دليل التشغيل السريع
# Quick Start Guide

## للمستخدمين الجدد | For New Users

### 1️⃣ استنساخ المشروع | Clone the Project

```bash
git clone https://github.com/YOUR_USERNAME/quran-video-generator.git
cd quran-video-generator
```

### 2️⃣ إنشاء بيئة افتراضية | Create Virtual Environment

**على Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**على Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ تثبيت المتطلبات | Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ تثبيت FFmpeg | Install FFmpeg

**Windows:**
1. حمل FFmpeg من: https://www.gyan.dev/ffmpeg/builds/
2. فك الضغط ونسخ المجلد إلى `C:\ffmpeg`
3. أضف `C:\ffmpeg\bin` إلى متغير البيئة PATH

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

**التحقق من التثبيت:**
```bash
ffmpeg -version
```

### 5️⃣ تشغيل التطبيق | Run the Application

```bash
python main_final.py
```

### 6️⃣ فتح المتصفح | Open Browser

افتح المتصفح واذهب إلى:
```
http://localhost:5000
```

---

## ✨ الاستخدام | Usage

1. **اختر القارئ** من القائمة المنسدلة (أكثر من 60 قارئ متاح)
2. **اختر السورة** من قائمة السور (114 سورة)
3. **حدد نطاق الآيات**:
   - من الآية: رقم الآية الأولى
   - إلى الآية: رقم الآية الأخيرة
4. **اضغط "إنشاء الفيديو"**
5. **انتظر** حتى ينتهي الإنشاء (سترى شريط التقدم)
6. **حمل الفيديو** الناتج

---

## 📁 مكان الملفات | File Locations

- **الفيديوهات الناتجة:** `output/`
- **الملفات المؤقتة:** `temp/` (تُحذف تلقائياً)
- **كاش الخلفيات:** `backgrounds/`

---

## ⚙️ الإعدادات الأساسية | Basic Settings

لتخصيص التطبيق، افتح ملف `config.py` وعدل:

```python
# أبعاد الفيديو (عمودي للريلز)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920

# حجم الخط
TEXT_FONT_SIZE = 60

# جودة الفيديو
VIDEO_BITRATE = "2M"
```

---

## 🔧 استكشاف الأخطاء | Troubleshooting

### المشكلة: `FFmpeg not found`
**الحل:** تأكد من تثبيت FFmpeg وإضافته للـ PATH

### المشكلة: `ModuleNotFoundError`
**الحل:** تأكد من تفعيل البيئة الافتراضية وتثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

### المشكلة: الخط العربي لا يظهر
**الحل:** تأكد من وجود خطوط عربية في مجلد `fonts/`

### المشكلة: فشل تحميل الخلفيات
**الحل:** تحقق من اتصال الإنترنت

---

## 📚 مزيد من المعلومات | More Information

- **الدليل الكامل:** [README.md](README.md)
- **دليل التحديث:** [UPDATE_GUIDE.md](UPDATE_GUIDE.md)
- **دليل GitHub:** [GITHUB_DEPLOY.md](GITHUB_DEPLOY.md)
- **استكشاف الأخطاء:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🎯 مثال سريع | Quick Example

```bash
# 1. استنساخ المشروع
git clone https://github.com/YOUR_USERNAME/quran-video-generator.git
cd quran-video-generator

# 2. إعداد البيئة
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. تشغيل التطبيق
python main_final.py

# 4. افتح المتصفح
# http://localhost:5000
```

---

**بالتوفيق! 🌟**

للدعم والمساعدة، راجع [TROUBLESHOOTING.md](TROUBLESHOOTING.md) أو افتح Issue على GitHub.
