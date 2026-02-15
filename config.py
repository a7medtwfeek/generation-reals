import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# API Keys
PEXELS_API_KEY = "KC7UgPcEyQGoZS0nhceJoVfv1mtNzG4dr015IXjrS23CFgIHNXuG3L52"

# Directories
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"
BACKGROUNDS_DIR = BASE_DIR / "backgrounds"

# Create directories if they don't exist
for directory in [TEMP_DIR, OUTPUT_DIR, BACKGROUNDS_DIR]:
    directory.mkdir(exist_ok=True)

# API Endpoints
ALQURAN_API = "https://api.alquran.cloud/v1"
EVERYAYAH_BASE = "https://everyayah.com/data"

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
VIDEO_BITRATE = "2M"
AUDIO_BITRATE = "192k"

# Font Settings (Arabic fonts)
ARABIC_FONTS = [
    "C:\\Windows\\Fonts\\scheherazade.ttf",  # Scheherazade - best for Arabic ligatures
    "C:\\Windows\\Fonts\\simpo.ttf",  # Simplified Arabic - best for full Unicode
    "C:\\Windows\\Fonts\\tahoma.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",
]

# Text Overlay Settings
TEXT_FONT_SIZE = 75
TEXT_COLOR = "white"
TEXT_OUTLINE_COLOR = "black"
TEXT_OUTLINE_WIDTH = 5
TEXT_PADDING = 40

# Pexels Settings
PEXELS_SEARCH_KEYWORDS = [
    # مساجد إسلامية
    "mosque architecture",
    "islamic mosque dome",
    "masjid minaret",
    
    # مناظر طبيعية - سماء
    "clouds sky timelapse",
    "sunset clouds",
    "night sky stars",
    "milky way galaxy",
    
    # مناظر طبيعية - جبال
    "mountain landscape",
    "mountain peak aerial",
    
    # مناظر طبيعية - ماء
    "ocean waves",
    "waterfall flowing",
    
    # مناظر طبيعية - صحراء
    "desert sand dunes"
]
PEXELS_VIDEO_ORIENTATION = "portrait"
PEXELS_VIDEO_SIZE = "hd"

# Reciter List (complete list from everyayah.com)
RECITERS = {
    # عبد الباسط عبد الصمد - Abdul Basit Abdul Samad
    "abdul_basit": {
        "name_ar": "عبد الباسط عبد الصمد - مرتل",
        "name_en": "Abdul Basit - Murattal",
        "folder": "Abdul_Basit_Murattal_192kbps"
    },
    "abdul_basit_murattal_192": {
        "name_ar": "عبد الباسط - مرتل 192",
        "name_en": "Abdul Basit - Murattal 192kbps",
        "folder": "Abdul_Basit_Murattal_192kbps"
    },
    "abdul_basit_murattal_64": {
        "name_ar": "عبد الباسط - مرتل 64",
        "name_en": "Abdul Basit - Murattal 64kbps",
        "folder": "Abdul_Basit_Murattal_64kbps"
    },
    "abdul_basit_mujawwad": {
        "name_ar": "عبد الباسط - مجود",
        "name_en": "Abdul Basit - Mujawwad",
        "folder": "Abdul_Basit_Mujawwad_128kbps"
    },
    
    # مشاري العفاسي - Mishary Alafasy
    "alafasy_128": {
        "name_ar": "مشاري العفاسي",
        "name_en": "Mishary Alafasy",
        "folder": "Alafasy_128kbps"
    },
    "alafasy_64": {
        "name_ar": "مشاري العفاسي 64",
        "name_en": "Mishary Alafasy 64kbps",
        "folder": "Alafasy_64kbps"
    },
    
    # سعد الغامدي - Saad Al-Ghamidi
    "ghamadi": {
        "name_ar": "سعد الغامدي",
        "name_en": "Saad Al-Ghamidi",
        "folder": "Ghamadi_40kbps"
    },
    
    # محمود خليل الحصري - Mahmoud Khalil Al-Husary
    "husary_128": {
        "name_ar": "محمود خليل الحصري",
        "name_en": "Mahmoud Khalil Al-Husary",
        "folder": "Husary_128kbps"
    },
    "husary_64": {
        "name_ar": "محمود خليل الحصري 64",
        "name_en": "Mahmoud Khalil Al-Husary 64kbps",
        "folder": "Husary_64kbps"
    },
    "husary_mujawwad_128": {
        "name_ar": "محمود خليل الحصري - مجود",
        "name_en": "Al-Husary - Mujawwad",
        "folder": "Husary_128kbps_Mujawwad"
    },
    "husary_mujawwad_64": {
        "name_ar": "محمود خليل الحصري - مجود 64",
        "name_en": "Al-Husary - Mujawwad 64kbps",
        "folder": "Husary_Mujawwad_64kbps"
    },
    "husary_muallim": {
        "name_ar": "محمود خليل الحصري - معلم",
        "name_en": "Al-Husary - Teacher",
        "folder": "Husary_Muallim_128kbps"
    },
    
    # ماهر المعيقلي - Maher Al-Muaiqly
    "maher_128": {
        "name_ar": "ماهر المعيقلي",
        "name_en": "Maher Al-Muaiqly",
        "folder": "MaherAlMuaiqly128kbps"
    },
    "maher_64": {
        "name_ar": "ماهر المعيقلي 64",
        "name_en": "Maher Al-Muaiqly 64kbps",
        "folder": "Maher_AlMuaiqly_64kbps"
    },
    
    # عبد الرحمن السديس - Abdul Rahman Al-Sudais
    "sudais_192": {
        "name_ar": "عبد الرحمن السديس",
        "name_en": "Abdul Rahman Al-Sudais",
        "folder": "Abdurrahmaan_As-Sudais_192kbps"
    },
    "sudais_64": {
        "name_ar": "عبد الرحمن السديس 64",
        "name_en": "Abdul Rahman Al-Sudais 64kbps",
        "folder": "Abdurrahmaan_As-Sudais_64kbps"
    },
    
    # محمد صديق المنشاوي - Mohamed Siddiq Al-Minshawi
    "minshawi_murattal": {
        "name_ar": "محمد صديق المنشاوي - مرتل",
        "name_en": "Al-Minshawi - Murattal",
        "folder": "Minshawy_Murattal_128kbps"
    },
    "minshawi_mujawwad_192": {
        "name_ar": "محمد صديق المنشاوي - مجود",
        "name_en": "Al-Minshawi - Mujawwad",
        "folder": "Minshawy_Mujawwad_192kbps"
    },
    "minshawi_mujawwad_64": {
        "name_ar": "محمد صديق المنشاوي - مجود 64",
        "name_en": "Al-Minshawi - Mujawwad 64kbps",
        "folder": "Minshawy_Mujawwad_64kbps"
    },
    
    # أحمد العجمي - Ahmed Al-Ajmi
    "ajmi_128": {
        "name_ar": "أحمد العجمي",
        "name_en": "Ahmed Al-Ajmi",
        "folder": "Ahmed_ibn_Ali_al-Ajamy_128kbps_ketaballah.net"
    },
    "ajmi_64": {
        "name_ar": "أحمد العجمي 64",
        "name_en": "Ahmed Al-Ajmi 64kbps",
        "folder": "Ahmed_ibn_Ali_al-Ajamy_64kbps_QuranExplorer.Com"
    },
    
    # سعود الشريم - Saud Al-Shuraim
    "shuraim_128": {
        "name_ar": "سعود الشريم",
        "name_en": "Saud Al-Shuraim",
        "folder": "Shuraym_128kbps"
    },
    "shuraim_64": {
        "name_ar": "سعود الشريم 64",
        "name_en": "Saud Al-Shuraim 64kbps",
        "folder": "Shuraym_64kbps"
    },
    
    # عبد الله الجهني - Abdullah Al-Juhany
    "juhany": {
        "name_ar": "عبد الله الجهني",
        "name_en": "Abdullah Al-Juhany",
        "folder": "Abdullaah_3awwaad_Al-Juhaynee_128kbps"
    },
    
    # عبد الله بصفر - Abdullah Basfar
    "basfar_192": {
        "name_ar": "عبد الله بصفر",
        "name_en": "Abdullah Basfar",
        "folder": "Abdullah_Basfar_192kbps"
    },
    "basfar_64": {
        "name_ar": "عبد الله بصفر 64",
        "name_en": "Abdullah Basfar 64kbps",
        "folder": "Abdullah_Basfar_64kbps"
    },
    "basfar_32": {
        "name_ar": "عبد الله بصفر 32",
        "name_en": "Abdullah Basfar 32kbps",
        "folder": "Abdullah_Basfar_32kbps"
    },
    
    # أبو بكر الشاطري - Abu Bakr Al-Shatri
    "shatri_128": {
        "name_ar": "أبو بكر الشاطري",
        "name_en": "Abu Bakr Al-Shatri",
        "folder": "Abu_Bakr_Ash-Shaatree_128kbps"
    },
    "shatri_64": {
        "name_ar": "أبو بكر الشاطري 64",
        "name_en": "Abu Bakr Al-Shatri 64kbps",
        "folder": "Abu_Bakr_Ash-Shaatree_64kbps"
    },
    
    # علي جابر - Ali Jaber
    "ali_jaber": {
        "name_ar": "علي جابر",
        "name_en": "Ali Jaber",
        "folder": "Ali_Jaber_64kbps"
    },
    
    # علي الحذيفي - Ali Al-Hudhaify
    "hudhaify_128": {
        "name_ar": "علي الحذيفي",
        "name_en": "Ali Al-Hudhaify",
        "folder": "Hudhaify_128kbps"
    },
    "hudhaify_64": {
        "name_ar": "علي الحذيفي 64",
        "name_en": "Ali Al-Hudhaify 64kbps",
        "folder": "Hudhaify_64kbps"
    },
    "hudhaify_32": {
        "name_ar": "علي الحذيفي 32",
        "name_en": "Ali Al-Hudhaify 32kbps",
        "folder": "Hudhaify_32kbps"
    },
    
    # محمد أيوب - Muhammad Ayyub
    "ayyub_128": {
        "name_ar": "محمد أيوب",
        "name_en": "Muhammad Ayyub",
        "folder": "Muhammad_Ayyoub_128kbps"
    },
    "ayyub_64": {
        "name_ar": "محمد أيوب 64",
        "name_en": "Muhammad Ayyub 64kbps",
        "folder": "Muhammad_Ayyoub_64kbps"
    },
    "ayyub_32": {
        "name_ar": "محمد أيوب 32",
        "name_en": "Muhammad Ayyub 32kbps",
        "folder": "Muhammad_Ayyoub_32kbps"
    },
    
    # محمد جبريل - Muhammad Jibreel
    "jibreel_128": {
        "name_ar": "محمد جبريل",
        "name_en": "Muhammad Jibreel",
        "folder": "Muhammad_Jibreel_128kbps"
    },
    "jibreel_64": {
        "name_ar": "محمد جبريل 64",
        "name_en": "Muhammad Jibreel 64kbps",
        "folder": "Muhammad_Jibreel_64kbps"
    },
    
    # ناصر القطامي - Nasser Al-Qatami
    "qatami": {
        "name_ar": "ناصر القطامي",
        "name_en": "Nasser Al-Qatami",
        "folder": "Nasser_Alqatami_128kbps"
    },
    
    # ياسر الدوسري - Yasser Al-Dosari
    "dosari": {
        "name_ar": "ياسر الدوسري",
        "name_en": "Yasser Al-Dosari",
        "folder": "Dussary_128kbps"
    },
    
    # محمد الطبلاوي - Muhammad Al-Tablawi
    "tablawi_128": {
        "name_ar": "محمد الطبلاوي",
        "name_en": "Muhammad Al-Tablawi",
        "folder": "Mohammad_al_Tablaway_128kbps"
    },
    "tablawi_64": {
        "name_ar": "محمد الطبلاوي 64",
        "name_en": "Muhammad Al-Tablawi 64kbps",
        "folder": "Mohammad_al_Tablaway_64kbps"
    },
    
    # بندر بليلة - Bandar Baleela
    "bandar_baleela": {
        "name_ar": "بندر بليلة",
        "name_en": "Bandar Baleela",
        "folder": "Bandar_Baleela_64kbps"
    },
    
    # أحمد نعينع - Ahmed Neana
    "ahmed_neana": {
        "name_ar": "أحمد نعينع",
        "name_en": "Ahmed Neana",
        "folder": "Ahmed_Neana_128kbps"
    },
    
    # إبراهيم الأخضر - Ibrahim Akhdar
    "ibrahim_akhdar_64": {
        "name_ar": "إبراهيم الأخضر",
        "name_en": "Ibrahim Akhdar",
        "folder": "Ibrahim_Akhdar_64kbps"
    },
    "ibrahim_akhdar_32": {
        "name_ar": "إبراهيم الأخضر 32",
        "name_en": "Ibrahim Akhdar 32kbps",
        "folder": "Ibrahim_Akhdar_32kbps"
    },
    
    # خالد القحطاني - Khalid Al-Qahtani
    "qahtani": {
        "name_ar": "خالد القحطاني",
        "name_en": "Khalid Al-Qahtani",
        "folder": "Khaalid_Abdullaah_al-Qahtaanee_192kbps"
    },
    
    # هاني الرفاعي - Hani Rifai
    "hani_rifai_192": {
        "name_ar": "هاني الرفاعي",
        "name_en": "Hani Rifai",
        "folder": "Hani_Rifai_192kbps"
    },
    "hani_rifai_64": {
        "name_ar": "هاني الرفاعي 64",
        "name_en": "Hani Rifai 64kbps",
        "folder": "Hani_Rifai_64kbps"
    },
    
    # محسن القاسم - Muhsin Al-Qasim
    "muhsin_qasim": {
        "name_ar": "محسن القاسم",
        "name_en": "Muhsin Al-Qasim",
        "folder": "Muhsin_Al_Qasim_192kbps"
    },
    
    # صلاح البدير - Salah Al-Budair
    "salah_budair": {
        "name_ar": "صلاح البدير",
        "name_en": "Salah Al-Budair",
        "folder": "Salah_Al_Budair_128kbps"
    },
    
    # صلاح بوخاطر - Salah Bukhatir
    "salah_bukhatir": {
        "name_ar": "صلاح بوخاطر",
        "name_en": "Salah Bukhatir",
        "folder": "Salaah_AbdulRahman_Bukhatir_128kbps"
    },
    
    # عبد الله مطرود - Abdullah Matroud
    "abdullah_matroud": {
        "name_ar": "عبد الله مطرود",
        "name_en": "Abdullah Matroud",
        "folder": "Abdullah_Matroud_128kbps"
    },
    
    # أكرم العلاقمي - Akram AlAlaqimy
    "akram_alaqimy": {
        "name_ar": "أكرم العلاقمي",
        "name_en": "Akram AlAlaqimy",
        "folder": "Akram_AlAlaqimy_128kbps"
    },
    
    # علي حجاج السويسي - Ali Hajjaj AlSuesy
    "ali_hajjaj": {
        "name_ar": "علي حجاج السويسي",
        "name_en": "Ali Hajjaj AlSuesy",
        "folder": "Ali_Hajjaj_AlSuesy_128kbps"
    },
    
    # أيمن سويد - Ayman Sowaid
    "ayman_sowaid": {
        "name_ar": "أيمن سويد",
        "name_en": "Ayman Sowaid",
        "folder": "Ayman_Sowaid_64kbps"
    },
    
    # فارس عباد - Fares Abbad
    "fares_abbad": {
        "name_ar": "فارس عباد",
        "name_en": "Fares Abbad",
        "folder": "Fares_Abbad_64kbps"
    },
    
    # خليفة الطنيجي - Khalefa Al-Tunaiji
    "khalefa_tunaiji": {
        "name_ar": "خليفة الطنيجي",
        "name_en": "Khalefa Al-Tunaiji",
        "folder": "khalefa_al_tunaiji_64kbps"
    },
    
    # محمود علي البنا - Mahmoud Ali Al-Banna
    "mahmoud_banna": {
        "name_ar": "محمود علي البنا",
        "name_en": "Mahmoud Ali Al-Banna",
        "folder": "mahmoud_ali_al_banna_32kbps"
    },
    
    # محمد عبد الكريم - Muhammad AbdulKareem
    "muhammad_abdulkareem": {
        "name_ar": "محمد عبد الكريم",
        "name_en": "Muhammad AbdulKareem",
        "folder": "Muhammad_AbdulKareem_128kbps"
    },
    
    # مصطفى إسماعيل - Mustafa Ismail
    "mustafa_ismail": {
        "name_ar": "مصطفى إسماعيل",
        "name_en": "Mustafa Ismail",
        "folder": "Mustafa_Ismail_48kbps"
    },
    
    # نبيل الرفاعي - Nabil Rifai
    "nabil_rifai": {
        "name_ar": "نبيل الرفاعي",
        "name_en": "Nabil Rifai",
        "folder": "Nabil_Rifa3i_48kbps"
    },
    
    # سهل ياسين - Sahl Yassin
    "sahl_yassin": {
        "name_ar": "سهل ياسين",
        "name_en": "Sahl Yassin",
        "folder": "Sahl_Yassin_128kbps"
    },
    
    # ياسر سلامة - Yaser Salamah
    "yaser_salamah": {
        "name_ar": "ياسر سلامة",
        "name_en": "Yaser Salamah",
        "folder": "Yaser_Salamah_128kbps"
    },
    
    # كريم منصوري - Karim Mansoori
    "karim_mansoori": {
        "name_ar": "كريم منصوري",
        "name_en": "Karim Mansoori",
        "folder": "Karim_Mansoori_40kbps"
    },
    
    # برهيزجار - Parhizgar
    "parhizgar": {
        "name_ar": "برهيزجار",
        "name_en": "Parhizgar",
        "folder": "Parhizgar_48kbps"
    }
}

# Surah Names (all 114 surahs)
SURAHS = {
    1: "الفاتحة", 2: "البقرة", 3: "آل عمران", 4: "النساء", 5: "المائدة",
    6: "الأنعام", 7: "الأعراف", 8: "الأنفال", 9: "التوبة", 10: "يونس",
    11: "هود", 12: "يوسف", 13: "الرعد", 14: "إبراهيم", 15: "الحجر",
    16: "النحل", 17: "الإسراء", 18: "الكهف", 19: "مريم", 20: "طه",
    21: "الأنبياء", 22: "الحج", 23: "المؤمنون", 24: "النور", 25: "الفرقان",
    26: "الشعراء", 27: "النمل", 28: "القصص", 29: "العنكبوت", 30: "الروم",
    31: "لقمان", 32: "السجدة", 33: "الأحزاب", 34: "سبأ", 35: "فاطر",
    36: "يس", 37: "الصافات", 38: "ص", 39: "الزمر", 40: "غافر",
    41: "فصلت", 42: "الشورى", 43: "الزخرف", 44: "الدخان", 45: "الجاثية",
    46: "الأحقاف", 47: "محمد", 48: "الفتح", 49: "الحجرات", 50: "ق",
    51: "الذاريات", 52: "الطور", 53: "النجم", 54: "القمر", 55: "الرحمن",
    56: "الواقعة", 57: "الحديد", 58: "المجادلة", 59: "الحشر", 60: "الممتحنة",
    61: "الصف", 62: "الجمعة", 63: "المنافقون", 64: "التغابن", 65: "الطلاق",
    66: "التحريم", 67: "الملك", 68: "القلم", 69: "الحاقة", 70: "المعارج",
    71: "نوح", 72: "الجن", 73: "المزمل", 74: "المدثر", 75: "القيامة",
    76: "الإنسان", 77: "المرسلات", 78: "النبأ", 79: "النازعات", 80: "عبس",
    81: "التكوير", 82: "الإنفطار", 83: "المطففين", 84: "الإنشقاق", 85: "البروج",
    86: "الطارق", 87: "الأعلى", 88: "الغاشية", 89: "الفجر", 90: "البلد",
    91: "الشمس", 92: "الليل", 93: "الضحى", 94: "الشرح", 95: "التين",
    96: "العلق", 97: "القدر", 98: "البينة", 99: "الزلزلة", 100: "العاديات",
    101: "القارعة", 102: "التكاثر", 103: "العصر", 104: "الهمزة", 105: "الفيل",
    106: "قريش", 107: "الماعون", 108: "الكوثر", 109: "الكافرون", 110: "النصر",
    111: "ال��سد", 112: "الإخلاص", 113: "الفلق", 114: "الناس"
}
