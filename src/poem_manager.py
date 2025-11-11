import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import random
from config import Config

class PoemManager:
    def __init__(self):
        self.poems_df = self._load_poems()
        self.posted_poems = self._load_posted_poems()
    
    def _load_poems(self):
        """Загружает базу данных стихов"""
        if not os.path.exists(Config.POEMS_CSV):
            # Создаем пример базы данных
            sample_data = {
                'author': ['А.С. Пушкин', 'М.Ю. Лермонтов', 'С.А. Есенин', 'А.А. Ахматова'],
                'title': ['Я помню чудное мгновенье', 'Парус', 'Береза', 'Муза'],
                'text': [
                    'Я помню чудное мгновенье:\nПередо мной явилась ты,\nКак мимолетное виденье,\nКак гений чистой красоты.',
                    'Белеет парус одинокой\nВ тумане моря голубом!..\nЧто ищет он в стране далекой?\nЧто кинул он в краю родном?..',
                    'Белая береза\nПод моим окном\nПринакрылась снегом,\nТочно серебром.',
                    'Когда я ночью жду ее прихода,\nЖизнь, кажется, висит на волоске.\nЧто почести, что юность, что свобода\nПред милой гостьей с дудочкой в руке?'
                ]
            }
            df = pd.DataFrame(sample_data)
            df.to_csv(Config.POEMS_CSV, index=False, encoding='utf-8')
            print("✅ Created sample poems database")
            return df
        
        print("✅ Loaded existing poems database")
        return pd.read_csv(Config.POEMS_CSV, encoding='utf-8')
    
    def _load_posted_poems(self):
        """Загружает список уже опубликованных стихов"""
        if os.path.exists(Config.POSTED_POEMS_FILE):
            with open(Config.POSTED_POEMS_FILE, 'r', encoding='utf-8') as f:
                posted = set(line.strip() for line in f)
            print(f"✅ Loaded {len(posted)} posted poems")
            return posted
        print("✅ No posted poems history found")
        return set()
    
    def get_random_poem(self):
        """Возвращает случайное непубликовавшееся стихотворение"""
        available_poems = self.poems_df[~self.poems_df['title'].isin(self.posted_poems)]
        
        if available_poems.empty:
            # Если все стихи опубликованы, очищаем историю
            print("🔄 All poems posted, resetting history...")
            self.posted_poems.clear()
            available_poems = self.poems_df
        
        poem = available_poems.sample(n=1).iloc[0]
        print(f"📖 Selected poem: {poem['title']} by {poem['author']}")
        return poem['author'], poem['title'], poem['text']
    
    def mark_as_posted(self, title):
        """Помечает стихотворение как опубликованное"""
        self.posted_poems.add(title)
        with open(Config.POSTED_POEMS_FILE, 'a', encoding='utf-8') as f:
            f.write(title + '\n')
        print(f"✅ Marked '{title}' as posted")
    
    def get_available_backgrounds(self):
        """Возвращает список доступных фоновых видео"""
        backgrounds = []
        for file in os.listdir(Config.BACKGROUNDS_DIR):
            if file.lower().endswith(('.mp4', '.mov', '.avi')):
                backgrounds.append(os.path.join(Config.BACKGROUNDS_DIR, file))
        
        if backgrounds:
            print(f"✅ Found {len(backgrounds)} background videos")
        else:
            print("⚠️ No background videos found")
        
        return backgrounds
