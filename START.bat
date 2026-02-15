@echo off
chcp 65001 >nul
echo ========================================
echo مُولِّد فيديوهات آيات القرآن الكريم
echo Quran Video Generator
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ⚠️  البيئة الافتراضية غير موجودة
    echo Creating virtual environment...
    python -m venv .venv
    echo ✅ تم إنشاء البيئة الافتراضية
    echo.
)

REM Activate virtual environment
echo 🔄 تفعيل البيئة الافتراضية...
call .venv\Scripts\activate.bat

REM Check if requirements are installed
echo 🔍 التحقق من المكتبات المطلوبة...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo ⚠️  المكتبات غير مثبتة
    echo Installing requirements...
    pip install -r requirements.txt
    echo ✅ تم تثبيت المكتبات
    echo.
)

REM Run the application
echo.
echo ========================================
echo 🚀 تشغيل التطبيق...
echo ========================================
echo.
echo ✨ المميزات:
echo   ✓ نص عربي نظيف بدون placeholders
echo   ✓ كل آية = فيديو مستقل
echo   ✓ دمج تلقائي في فيديو نهائي واحد
echo   ✓ تنظيف تلقائي للملفات المؤقتة
echo.
echo 🌐 الخادم سيعمل على: http://localhost:5000
echo.
echo 📌 اضغط Ctrl+C للإيقاف
echo ========================================
echo.

python main_final.py

pause
