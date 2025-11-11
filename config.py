import os

class Config:
    # Пути к файлам
    BACKGROUNDS_DIR = "assets/backgrounds"
    FONTS_DIR = "assets/fonts"
    MUSIC_DIR = "assets/music"
    OUTPUT_DIR = "output"
    AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
    VIDEO_DIR = os.path.join(OUTPUT_DIR, "videos")
    DATA_DIR = "data"
    
    # Файлы данных
    POEMS_CSV = os.path.join(DATA_DIR, "poems.csv")
    POSTED_POEMS_FILE = os.path.join(DATA_DIR, "posted_poems.txt")
    
    # Настройки видео
    VIDEO_RESOLUTION = (1080, 1920)  # Вертикальное для Instagram
    VIDEO_FPS = 24
    BACKGROUND_MUSIC_VOLUME = 0.1
    
    # Настройки текста
    FONT_PRIMARY = "Arial"  # Стандартный шрифт
    FONT_BOLD = "Arial-Bold"
    TEXT_COLOR = "white"
    TEXT_STROKE_COLOR = "black"
    TEXT_STROKE_WIDTH = 2
    
    # Instagram настройки
    MAX_CAPTION_LENGTH = 2200
    HASHTAGS = [
        "#поэзия", "#стихи", "#литература", "#поэты", "#русскаяпоэзия",
        "#классика", "#чтение", "#искусство", "#культура",
        # Армянские хештеги
        "#Армения", "#Ереван", "#Армения🇦🇲", "#Armenia",
        "#армянскаякультура", "#поэзияармении", "#армянскаяпоэзия",
        "#ереван2024", "#русскаяпоэзиявармении"
    ]

# Создаем директории при импорте
for directory in [Config.BACKGROUNDS_DIR, Config.FONTS_DIR, Config.MUSIC_DIR,
                  Config.AUDIO_DIR, Config.VIDEO_DIR, Config.DATA_DIR]:
    os.makedirs(directory, exist_ok=True)
