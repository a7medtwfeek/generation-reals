"""
سكريبت لإصلاح indentation في final_generator.py
"""

# اقرأ الملف
with open('final_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ابحث عن السطر الذي يبدأ بـ "def create_verse_image"
fixed_lines = []
fix_mode = False

for i, line in enumerate(lines):
    # إذا وصلنا للدالة create_verse_image بدون indentation
    if line.strip().startswith('def create_verse_image'):
        fix_mode = True
        # أضف 4 مسافات (indentation)
        fixed_lines.append('    ' + line)
    # إذا كنا في fix mode وليس سطر فارغ
    elif fix_mode:
        # إذا وصلنا لدالة جديدة في نفس المستوى، أوقف التصليح
        if line.strip().startswith('def ') and not line.startswith('    '):
            fix_mode = False
            fixed_lines.append(line)
        # إذا السطر فارغ أو تعليق
        elif line.strip() == '' or line.strip().startswith('#'):
            # تحقق إذا كان التعليق في المستوى الخارجي
            if not line.startswith('    ') and line.strip().startswith('#'):
                # هذا تعليق خارجي - أوقف fix mode
                fix_mode = False
            fixed_lines.append(line)
        else:
            # أضف indentation
            if not line.startswith('    '):
                fixed_lines.append('    ' + line)
            else:
                fixed_lines.append(line)
    else:
        fixed_lines.append(line)

# احفظ الملف المصلح
with open('final_generator_fixed.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("✓ تم إصلاح الملف!")
print("الملف الجديد: final_generator_fixed.py")
print("\nلتطبيق التصليح:")
print("1. احذف final_generator.py القديم")
print("2. غيّر اسم final_generator_fixed.py إلى final_generator.py")
