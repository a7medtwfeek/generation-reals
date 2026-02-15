# 📝 أوامر رفع المشروع على GitHub
# Commands to Upload Project to GitHub

## ⚡ الأوامر السريعة | Quick Commands

افتح PowerShell في مجلد المشروع ونفذ الأوامر التالية بالترتيب:

### 1️⃣ التحقق من Git
```powershell
git --version
```
إذا لم يكن مثبت، حمله من: https://git-scm.com/download/win

---

### 2️⃣ إعداد Git (المرة الأولى فقط)
```powershell
# ضع اسمك وبريدك الإلكتروني
git config --global user.name "اسمك"
git config --global user.email "your.email@example.com"
```

---

### 3️⃣ التحقق من حالة المشروع
```powershell
cd "c:\Users\Ahmed\Videos\تولي001\توليد1"
git status
```

---

### 4️⃣ إضافة جميع الملفات
```powershell
git add .
```

---

### 5️⃣ عمل Commit
```powershell
git commit -m "Initial commit: Quran Video Generator with main_final.py"
```

---

### 6️⃣ إنشاء Repository على GitHub

1. افتح https://github.com
2. سجل دخول
3. اضغط **"New"** أو **"+"** → **"New repository"**
4. املأ البيانات:
   - **Repository name**: `quran-video-generator`
   - **Description**: `مُولِّد فيديوهات آيات القرآن الكريم`
   - اختر **Public** أو **Private**
   - **لا تختر** "Initialize with README"
5. اضغط **"Create repository"**

---

### 7️⃣ ربط المشروع بـ GitHub
```powershell
# استبدل YOUR_USERNAME باسم المستخدم الخاص بك على GitHub
git remote add origin https://github.com/YOUR_USERNAME/quran-video-generator.git
```

---

### 8️⃣ التحقق من اسم الفرع الرئيسي
```powershell
git branch
```

إذا كان الفرع اسمه `master`، غيره لـ `main`:
```powershell
git branch -M main
```

---

### 9️⃣ رفع المشروع على GitHub
```powershell
git push -u origin main
```

---

## 🔐 إذا طلب منك تسجيل الدخول

GitHub لا يقبل كلمة المرور العادية بعد الآن. استخدم **Personal Access Token**:

### إنشاء Token:
1. اذهب إلى: https://github.com/settings/tokens
2. اضغط **"Generate new token"** → **"Generate new token (classic)"**
3. اختر اسم للـ Token (مثل: `quran-video-generator`)
4. اختر Scope: **repo** (كامل)
5. اضغط **"Generate token"**
6. **انسخ الـ Token فوراً** (لن تراه مرة أخرى!)

### استخدام Token:
عند طلب كلمة المرور، استخدم الـ Token بدلاً منها.

أو استخدم:
```powershell
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/quran-video-generator.git
```

---

## ✅ التحقق من النجاح

بعد الرفع، افتح:
```
https://github.com/YOUR_USERNAME/quran-video-generator
```

يجب أن ترى جميع ملفات المشروع!

---

## 🔄 تحديث المشروع لاحقاً

عند إجراء تعديلات جديدة:

```powershell
# 1. إضافة التغييرات
git add .

# 2. عمل commit
git commit -m "وصف التحديث"

# 3. رفع التحديثات
git push
```

---

## 🎯 نسخ سريع للأوامر الكاملة

```powershell
# الانتقال للمشروع
cd "c:\Users\Ahmed\Videos\تولي001\توليد1"

# التحقق من الحالة
git status

# إضافة الملفات
git add .

# عمل commit
git commit -m "Initial commit: Quran Video Generator with main_final.py"

# ربط بـ GitHub (استبدل YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/quran-video-generator.git

# تغيير اسم الفرع إلى main
git branch -M main

# رفع المشروع
git push -u origin main
```

---

## ❓ استكشاف الأخطاء الشائعة

### `fatal: not a git repository`
**الحل:**
```powershell
git init
```

### `fatal: remote origin already exists`
**الحل:**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/quran-video-generator.git
```

### `error: failed to push some refs`
**الحل:**
```powershell
git pull origin main --rebase
git push origin main
```

---

**بالتوفيق! 🚀**
