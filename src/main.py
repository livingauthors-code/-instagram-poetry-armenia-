import os
import sys
import time

# ⬇️ ДОБАВЬ ЭТИ СТРОКИ ДЛЯ ИМПОРТА ИЗ КОРНЕВОЙ ПАПКИ
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from poem_manager import PoemManager
from audio_generator import AudioGenerator
from video_creator import VideoCreator
from instagram_poster import InstagramPoster

def main():
    print("=" * 50)
    print("🚀 ARMENIAN POETRY INSTAGRAM BOT")
    print("📍 Timezone: Asia/Yerevan (UTC+4)")
    print("=" * 50)
    
    # Инициализация менеджеров
    poem_manager = PoemManager()
    audio_gen = AudioGenerator()
    video_creator = VideoCreator()
    
    # Получаем случайное стихотворение
    author, title, text = poem_manager.get_random_poem()
    print(f"📖 Selected: '{title}' by {author}")
    
    # Создаем уникальные имена файлов
    timestamp = int(time.time())
    audio_file = os.path.join(Config.AUDIO_DIR, f"audio_{timestamp}.mp3")
    final_audio_file = os.path.join(Config.AUDIO_DIR, f"final_audio_{timestamp}.mp3")
    video_file = os.path.join(Config.VIDEO_DIR, f"video_{timestamp}.mp4")
    
    try:
        # Шаг 1: Генерация аудио
        print("\n🎯 Step 1: Audio Generation")
        if not audio_gen.text_to_speech(text, audio_file):
            raise Exception("Audio generation failed")
        
        # Шаг 2: Смешивание с музыкой
        print("\n🎯 Step 2: Audio Mixing")
        if not audio_gen.mix_audio(audio_file, final_audio_file):
            # Если не удалось смешать, используем оригинальное аудио
            final_audio_file = audio_file
        
        # Шаг 3: Создание видео
        print("\n🎯 Step 3: Video Creation")
        if not video_creator.create_poetry_video(final_audio_file, text, author, title, video_file):
            raise Exception("Video creation failed")
        
        # Шаг 4: Подготовка описания
        caption = f"{title} - {author}\n\n{text}\n\n" + " ".join(Config.HASHTAGS)
        caption = caption[:Config.MAX_CAPTION_LENGTH]
        
        # Шаг 5: Публикация в Instagram (только если указаны логин/пароль)
        insta_username = os.environ.get("INSTAGRAM_USERNAME")
        insta_password = os.environ.get("INSTAGRAM_PASSWORD")
        
        if insta_username and insta_password:
            print("\n🎯 Step 4: Instagram Publication")
            poster = InstagramPoster(insta_username, insta_password)
            poster.setup_driver()
            
            if poster.login():
                if poster.upload_video(video_file, caption):
                    poem_manager.mark_as_posted(title)
                    print("✅ Publication completed successfully!")
                else:
                    print("⚠️ Instagram upload failed, but video was created")
            else:
                print("⚠️ Instagram login failed, but video was created")
            
            poster.close()
        else:
            print("\nℹ️ Instagram credentials not provided")
            print(f"📁 Video created: {video_file}")
            print("💡 Add INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD secrets to enable auto-posting")
        
        # Очистка временных файлов
        print("\n🧹 Cleaning temporary files...")
        if os.path.exists(audio_file):
            os.remove(audio_file)
        if os.path.exists(final_audio_file) and final_audio_file != audio_file:
            os.remove(final_audio_file)
            
        print("\n🎉 BOT EXECUTION COMPLETED!")
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
