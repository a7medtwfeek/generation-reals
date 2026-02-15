# 🚀 دليل البدء السريع | Quick Start Commands

## للمستخدمين الجدد | For New Users

### 1️⃣ تشخيص المشاكل
```bash
python diagnose.py
```
✅ يفحص FFmpeg، المكتبات، الإنترنت، والملفات

### 2️⃣ اختبار سريع  
```bash
python test_generator.py
```
✅ ينشئ فيديو تجريبي (آية واحدة)

### 3️⃣ تشغيل التطبيق
```bash
python main.py
```
✅ ثم افتح: http://localhost:5000

---

## إذا واجهت مشكلة | If You Have Issues

### الخطأ: "FFmpeg not found"
```bash
# تحقق من FFmpeg
ffmpeg -version

# إذا لم يعمل، حمّله من:
# https://www.gyan.dev/ffmpeg/builds/
```

### الخطأ: "فشل في إنشاء الفيديو"
```bash
# 1. شغّل المُشخص
python diagnose.py

# 2. شاهد رسائل الخطأ
# 3. راجع TROUBLESHOOTING.md
```

### الخطأ: "Module not found"
```bash
pip install -r requirements.txt
```

---

## ملفات مفيدة | Useful Files

- `README.md` - الدليل الكامل
- `TROUBLESHOOTING.md` - حل المشاكل
- `diagnose.py` - فحص النظام
- `test_generator.py` - اختبار التوليد

---

## أوامر سريعة | Quick Commands

```bash
# الانتقال للمجلد
cd "c:\Users\Ahmed\Videos\توليد1"

# تشخيص
python diagnose.py

# اختبار
python test_generator.py

# تشغيل
python main.py
```

---

**مهم:** شغّل `diagnose.py` أولاً قبل أي شيء!
