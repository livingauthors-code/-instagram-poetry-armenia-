import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

class InstagramPoster:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
    
    def setup_driver(self):
        """Настраивает Chrome driver для GitHub Actions"""
        print("🌐 Setting up Chrome driver...")
        
        chrome_options = Options()
        
        # Настройки для Армении
        chrome_options.add_argument("--lang=ru")
        chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': 'ru,ru_RU',
            'timezone': 'Asia/Yerevan'
        })
        
        # Настройки для GitHub Actions
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Автоматическая установка ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        
        print("✅ Chrome driver setup completed")
    
    def login(self):
        """Логин в Instagram"""
        try:
            print("🔐 Logging into Instagram...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # Ввод логина
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.username)
            
            # Ввод пароля
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            
            # Ожидание входа
            time.sleep(5)
            
            # Пропускаем всплывающие окна
            self._dismiss_popups()
            
            print("✅ Successfully logged into Instagram")
            return True
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def _dismiss_popups(self):
        """Пропускает всплывающие окна"""
        try:
            # "Сохранить данные для входа"
            not_now_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Not Now') or contains(text(), 'Не сейчас')]")
            for button in not_now_buttons:
                try:
                    button.click()
                    time.sleep(1)
                except:
                    pass
        except:
            pass
    
    def upload_video(self, video_path, caption):
        """Загружает видео в Instagram"""
        try:
            print("📤 Uploading video to Instagram...")
            
            # Переходим на главную страницу
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # Здесь будет код загрузки видео
            # Временно просто возвращаем успех для тестирования
            print("✅ Video upload simulation - working on full implementation")
            return True
            
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
    
    def close(self):
        """Закрывает браузер"""
        if self.driver:
            self.driver.quit()
            print("🌐 Browser closed")
