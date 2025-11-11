import os
from gtts import gTTS
import tempfile
from pydub import AudioSegment
from pydub.effects import normalize
from config import Config

class AudioGenerator:
    def __init__(self):
        pass
    
    def text_to_speech(self, text, output_file):
        """Преобразует текст в речь с улучшенным качеством"""
        try:
            print("🔊 Generating audio from text...")
            
            # Создаем временный файл для gTTS
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Генерируем речь с помощью gTTS
            tts = gTTS(text=text, lang='ru', slow=False)
            tts.save(temp_path)
            
            # Обрабатываем аудио для улучшения качества
            audio = AudioSegment.from_mp3(temp_path)
            
            # Нормализуем громкость
            audio = normalize(audio)
            
            # Сохраняем результат
            audio.export(output_file, format="mp3", bitrate="192k")
            
            # Удаляем временный файл
            os.unlink(temp_path)
            
            print("✅ Audio generated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            return False
    
    def get_background_music(self):
        """Возвращает случайную фоновую музыку если есть"""
        music_files = []
        for file in os.listdir(Config.MUSIC_DIR):
            if file.lower().endswith(('.mp3', '.wav')):
                music_files.append(os.path.join(Config.MUSIC_DIR, file))
        
        if music_files:
            selected_music = random.choice(music_files)
            print(f"🎵 Selected background music: {selected_music}")
            return selected_music
        
        print("ℹ️ No background music found")
        return None
    
    def mix_audio(self, speech_file, output_file):
        """Смешивает речь с фоновой музыкой"""
        try:
            # Загружаем речь
            speech = AudioSegment.from_mp3(speech_file)
            
            # Получаем фоновую музыку
            background_music = self.get_background_music()
            
            if background_music:
                print("🎵 Mixing audio with background music...")
                # Загружаем и настраиваем музыку
                music = AudioSegment.from_file(background_music)
                
                # Обрезаем музыку под длину речи
                if len(music) > len(speech):
                    music = music[:len(speech)]
                else:
                    # Если музыка короче, зацикливаем ее
                    repeats = (len(speech) // len(music)) + 1
                    music = music * repeats
                    music = music[:len(speech)]
                
                # Уменьшаем громкость музыки
                music = music - (20 - (Config.BACKGROUND_MUSIC_VOLUME * 10))
                
                # Смешиваем
                mixed = speech.overlay(music)
                mixed.export(output_file, format="mp3", bitrate="192k")
                print("✅ Audio mixed with background music")
            else:
                # Если музыки нет, просто копируем речь
                speech.export(output_file, format="mp3", bitrate="192k")
                print("✅ Audio saved without background music")
            
            return True
            
        except Exception as e:
            print(f"❌ Error mixing audio: {e}")
            return False
