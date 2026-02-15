# سكربت تحديث المشروع
# هذا السكربت يقوم بأخذ نسخة احتياطية من ملفاتك الحالية قبل التحديث

$ErrorActionPreference = "Stop"

Write-Host "🔄 جاري تجهيز عملية التحديث..." -ForegroundColor Cyan

# 1. تحديد مسار النسخة الاحتياطية
$timestamp = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
$backupPath = "..\backup_$timestamp"

Write-Host "📦 جاري إنشاء نسخة احتياطية في: $backupPath" -ForegroundColor Yellow

# 2. إنشاء المجلد
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null

# 3. نسخ الملفات (تجاهل المجلدات الكبيرة وغير الضرورية)
$exclude = @(".venv", "__pycache__", "output", "temp", "test_output", "backgrounds", ".git")
Copy-Item -Path ".\*" -Destination $backupPath -Recurse -Exclude $exclude

Write-Host "✅ تم إنشاء النسخة الاحتياطية بنجاح!" -ForegroundColor Green
Write-Host "📂 مسار النسخة الاحتياطية: $backupPath" -ForegroundColor Gray
Write-Host ""
Write-Host "⬇️  الآن يمكنك نسخ الملفات الجديدة (Mise-à-jour) ولصقها هنا والموافقة على الاستبدال." -ForegroundColor Cyan
Write-Host "⚠️  تنبيه: إذا كان الملف الجديد يحتوي على config.py، تأكد من نقل مفاتيح API الخاصة بك إليه." -ForegroundColor Red
Write-Host ""
Read-Host "اضغط Enter للخروج"
