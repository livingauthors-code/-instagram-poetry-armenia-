import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import fadein, fadeout
from config import Config

class VideoCreator:
    def __init__(self):
        pass
    
    def create_poetry_video(self, audio_file, text, author, title, output_file):
        """Создает видео с поэзией"""
        try:
            print("🎬 Creating poetry video...")
            
            # Получаем случайный фон или создаем черный
            background_path = self._get_random_background()
            
            # Загружаем аудио для определения длительности
            audio_clip = AudioFileClip(audio_file)
            audio_duration = audio_clip.duration
            
            # Загружаем и подготавливаем видео-фон
            video_clip = self._prepare_background(background_path, audio_duration)
            
            # Создаем текстовые элементы
            text_clips = self._create_text_clips(title, author, text, audio_duration)
            
            # Собираем финальное видео
            final_video = CompositeVideoClip([video_clip] + text_clips)
            final_video = final_video.set_audio(audio_clip)
            
            # Рендерим видео
            print("📹 Rendering video...")
            final_video.write_videofile(
                output_file,
                fps=Config.VIDEO_FPS,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Закрываем клипы для освобождения памяти
            video_clip.close()
            audio_clip.close()
            final_video.close()
            for clip in text_clips:
                clip.close()
            
            print(f"✅ Video created successfully: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating video: {e}")
            return False
    
    def _get_random_background(self):
        """Возвращает случайный фоновый видеофайл"""
        backgrounds = []
        for file in os.listdir(Config.BACKGROUNDS_DIR):
            if file.lower().endswith(('.mp4', '.mov', '.avi')):
                backgrounds.append(os.path.join(Config.BACKGROUNDS_DIR, file))
        
        if backgrounds:
            selected = random.choice(backgrounds)
            print(f"🎥 Selected background: {selected}")
            return selected
        
        print("🎥 Using default black background")
        return None
    
    def _prepare_background(self, background_path, target_duration):
        """Подготавливает фоновое видео"""
        if background_path and os.path.exists(background_path):
            video = VideoFileClip(background_path)
            
            # Если видео короче нужной длительности, зацикливаем
            if video.duration < target_duration:
                from moviepy.editor import concatenate_videoclips
                clips = [video]
                current_duration = video.duration
                
                while current_duration < target_duration:
                    clips.append(video)
                    current_duration += video.duration
                
                video = concatenate_videoclips(clips)
            
            # Обрезаем до нужной длительности
            video = video.subclip(0, target_duration)
            
            # Добавляем fade in/out
            video = video.fx(fadein, 1).fx(fadeout, 1)
            
        else:
            # Создаем черный фон если нет видео
            video = ColorClip(
                size=Config.VIDEO_RESOLUTION, 
                color=(0, 0, 0), 
                duration=target_duration
            )
        
        return video
    
    def _create_text_clips(self, title, author, text, duration):
        """Создает текстовые элементы для видео"""
        clips = []
        
        # Заголовок (автор и название)
        title_text = f"{title}\n{author}"
        title_clip = TextClip(
            title_text,
            fontsize=50,
            color=Config.TEXT_COLOR,
            font=Config.FONT_BOLD,
            stroke_color=Config.TEXT_STROKE_COLOR,
            stroke_width=Config.TEXT_STROKE_WIDTH,
            method='caption',
            size=(Config.VIDEO_RESOLUTION[0] * 0.9, None)
        )
        title_clip = title_clip.set_duration(duration)
        title_clip = title_clip.set_position(('center', 0.1), relative=True)
        title_clip = title_clip.fx(fadein, 1).fx(fadeout, 1)
        clips.append(title_clip)
        
        # Основной текст стихотворения
        text_clip = TextClip(
            text,
            fontsize=36,
            color=Config.TEXT_COLOR,
            font=Config.FONT_PRIMARY,
            stroke_color=Config.TEXT_STROKE_COLOR,
            stroke_width=Config.TEXT_STROKE_WIDTH,
            method='caption',
            size=(Config.VIDEO_RESOLUTION[0] * 0.8, None),
            align='center'
        )
        text_clip = text_clip.set_duration(duration)
        text_clip = text_clip.set_position(('center', 0.5), relative=True)
        text_clip = text_clip.fx(fadein, 1).fx(fadeout, 1)
        clips.append(text_clip)
        
        print("📝 Text clips created")
        return clips
