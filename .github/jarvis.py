import os
import sys
import time
import json
import random
import threading
import shutil
import sqlite3
import subprocess
import webbrowser
import datetime
import math
import smtplib
import requests
import pyttsx3
import speech_recognition as sr
import cv2  
import pyautogui
import psutil
import wikipedia
import pywhatkit  
import speedtest 
import pyjokes
import tkinter as tk
import pygame 
import keyboard 
from tkinter import ttk, scrolledtext, messagebox, filedialog, Canvas, simpledialog
from cryptography.fernet import Fernet
from difflib import get_close_matches
from plyer import notification 
import xml.etree.ElementTree as ET 
from PyPDF2 import PdfReader # BOOKS
from deep_translator import GoogleTranslator # TRANSLATION
from pytubefix import YouTube # YOUTUBE
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ==============================================================================
# ⚙️ SECTOR 1: GLOBAL CONFIGURATION & ASSETS
# ==============================================================================

class Config:
    APP_NAME = "J.A.R.V.I.S | GOD MODE"
    VERSION = "16.0.0"
    
    # --- FILE SYSTEM ARCHITECTURE ---
    BASE_DIR = os.path.expanduser("~/Documents/Jarvis_GodMode")
    DB_PATH = os.path.join(BASE_DIR, "core_memory.db")
    VAULT_DIR = os.path.join(BASE_DIR, "Secure_Vault")
    LOGS_DIR = os.path.join(BASE_DIR, "Logs")
    SECURITY_DIR = os.path.join(BASE_DIR, "Security_Footage") 
    DOWNLOADS_DIR = os.path.join(BASE_DIR, "Downloads")
    KEY_FILE = os.path.join(BASE_DIR, "master_cipher.key")
    FACE_MODEL = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
    
    # --- VISUAL THEME (STARK INDUSTRIES) ---
    COLOR_BG = "#020202"      # Abyssal Black
    COLOR_FG = "#00FFFF"      # Arc Reactor Cyan
    COLOR_SEC = "#005555"     # Dim Cyan
    COLOR_ACCENT = "#FFD700"  # Jarvis Gold
    COLOR_WARN = "#FF3333"    # Critical Red
    COLOR_TEXT = "#E0E0E0"    # Off-White
    FONT_MAIN = ("Orbitron", 10)
    FONT_CONSOLE = ("Consolas", 10)
    
    # --- AI & NETWORK ---
    NEWS_URL = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
    
    # --- AUDIO ---
    SPEECH_RATE = 175

    @staticmethod
    def initialize_system():
        """Bootstrapper: Creates all necessary folders and files."""
        required_dirs = [Config.BASE_DIR, Config.VAULT_DIR, Config.LOGS_DIR, Config.SECURITY_DIR, Config.DOWNLOADS_DIR]
        for d in required_dirs:
            if not os.path.exists(d):
                os.makedirs(d)
        
        # Download Face Model (Auto-Fix)
        if not os.path.exists(Config.FACE_MODEL):
            print(">> [BOOT] Acquiring Visual Cortex (Face Model)...")
            url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
            try:
                r = requests.get(url)
                with open(Config.FACE_MODEL, 'wb') as f: f.write(r.content)
            except: pass

Config.initialize_system()

# ==============================================================================
# 💾 SECTOR 2: DATABASE & MEMORY CORE
# ==============================================================================

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._construct_schema()

    def _construct_schema(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                phone TEXT,
                email TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_contact(self, name, phone, email=""):
        try:
            self.cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name.lower(), phone, email))
            self.conn.commit()
            return f"Contact {name} added successfully."
        except sqlite3.IntegrityError:
            return f"Contact {name} already exists."

    def get_contact_phone(self, name):
        self.cursor.execute("SELECT name, phone FROM contacts")
        all_contacts = self.cursor.fetchall()
        
        # Fuzzy Match
        names = [c[0] for c in all_contacts]
        matches = get_close_matches(name.lower(), names, n=1, cutoff=0.6)
        if matches:
            target = matches[0]
            self.cursor.execute("SELECT phone FROM contacts WHERE name=?", (target,))
            return self.cursor.fetchone()[0]
        return None
    
    # --- TASK OPS ---
    def add_task(self, task):
        self.cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        self.conn.commit()

    def get_pending_tasks(self):
        self.cursor.execute("SELECT id, task FROM tasks WHERE status='Pending'")
        return self.cursor.fetchall()
        
    def complete_task(self, task_id):
        self.cursor.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
        self.conn.commit()

db = DatabaseManager()

# ==============================================================================
# 📱 SECTOR 3: SOCIAL & COMM MODULE
# ==============================================================================

class CommModule:
    @staticmethod
    def send_whatsapp(contact_name, message):
        phone = db.get_contact_phone(contact_name)
        if not phone:
            return f"Error: {contact_name} is not in your contact database."
        
        if not phone.startswith("+"):
            phone = "+91" + phone
            
        try:
            def _send():
                pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=15, tab_close=True)
            
            t = threading.Thread(target=_send)
            t.daemon = True
            t.start()
            return f"Initiating WhatsApp protocol for {contact_name}."
        except Exception as e:
            return f"WhatsApp Protocol Failed: {e}"

# ==============================================================================
# 🔒 SECTOR 4: CRYPTO-VAULT & SENTRY (SECURITY)
# ==============================================================================


class SecuritySystem:
    def __init__(self):
        self.key = self._load_key()
        self.cipher = Fernet(self.key)

    def _load_key(self):
        if not os.path.exists(Config.KEY_FILE):
            k = Fernet.generate_key()
            with open(Config.KEY_FILE, "wb") as f: f.write(k)
            return k
        return open(Config.KEY_FILE, "rb").read()

    def encrypt_file(self, file_path):
        try:
            with open(file_path, "rb") as f: data = f.read()
            encrypted = self.cipher.encrypt(data)
            filename = os.path.basename(file_path)
            dest = os.path.join(Config.VAULT_DIR, filename + ".enc")
            with open(dest, "wb") as f: f.write(encrypted)
            os.remove(file_path)
            return f"File {filename} encrypted and moved to Vault."
        except Exception as e: return f"Encryption Error: {e}"

    def decrypt_file(self, filename):
        try:
            src = os.path.join(Config.VAULT_DIR, filename)
            if not os.path.exists(src): return "File not found in Vault."
            with open(src, "rb") as f: data = f.read()
            decrypted = self.cipher.decrypt(data)
            orig_name = filename.replace(".enc", "")
            restore_path = os.path.join(Config.BASE_DIR, "Restored_" + orig_name)
            with open(restore_path, "wb") as f: f.write(decrypted)
            return f"File restored to {restore_path}"
        except Exception as e: return f"Decryption Error: {e}"

class BiometricLock:
    def __init__(self):
        self.data_path = os.path.join(Config.BASE_DIR, "Biometric_Data")
        self.trainer_file = os.path.join(Config.BASE_DIR, "Trainer.yml")
        if not os.path.exists(self.data_path): os.makedirs(self.data_path)
        
        # Initialize the Recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_cascade = cv2.CascadeClassifier(Config.FACE_MODEL)

    def train_face(self):
        cam = cv2.VideoCapture(0)
        count = 0
        print(">> [SECURITY] TRAINING BIOMETRICS... LOOK AT THE CAMERA.")
        
        while True:
            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x,y,w,h) in faces:
                count += 1
                cv2.imwrite(f"{self.data_path}/User.{count}.jpg", gray[y:y+h, x:x+w])
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.putText(frame, f"SCANNING {count}%", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                
            cv2.imshow('BIOMETRIC TRAINING', frame)
            if cv2.waitKey(100) & 0xFF == ord('q') or count >= 50:
                break
        
        cam.release()
        cv2.destroyAllWindows()
        
        print(">> [SECURITY] PROCESSING DATA...")
        faces, ids = [], []
        image_paths = [os.path.join(self.data_path, f) for f in os.listdir(self.data_path)]
        
        for path in image_paths:
            img = cv2.imread(path, 0)
            faces.append(img)
            ids.append(1)
            
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.write(self.trainer_file)
        print(">> [SECURITY] BIOMETRIC LOCK UPDATED SUCCESSFULY.")

    def authenticate(self):
        if not os.path.exists(self.trainer_file):
            print(">> [ERROR] No biometric data found. Running First-Time Setup...")
            self.train_face()
            return True

        self.recognizer.read(self.trainer_file)
        cam = cv2.VideoCapture(0)
        unlocked = False
        
        print(">> [LOCKED] SCANNING FOR ADMIN ACCESS...")
        
        while True:
            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.2, 5)
            
            for(x,y,w,h) in faces:
                id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
                
                # Confidence: Lower is better (0 = perfect match, <50 is good)
                if confidence < 50:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                    cv2.putText(frame, "ACCESS GRANTED", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                    unlocked = True
                else:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
                    cv2.putText(frame, "ACCESS DENIED", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

            cv2.imshow('JARVIS SECURITY GATE', frame)
            
            k = cv2.waitKey(10) & 0xff
            if unlocked: 
                time.sleep(1)
                break
            if k == 27: # ESC key
                break
                
        cam.release()
        cv2.destroyAllWindows()
        return unlocked
# ==============================================================================
# 🎮 SECTOR 5: ARCADE (GAMES)
# ==============================================================================

class ArcadeSystem:
    
    @staticmethod
    def launch_snake(root_window):
        win = tk.Toplevel(root_window)
        win.title("PROMETHEUS ARCADE: SNAKE")
        win.geometry("600x400")
        canvas = tk.Canvas(win, width=600, height=400, bg="black")
        canvas.pack()
        
        class SnakeGame:
            def __init__(self):
                self.snake = [(100, 100), (90, 100), (80, 100)]
                self.food = self.place_food()
                self.direction = "Right"
                self.score = 0
                self.running = True
                win.bind("<Key>", self.change_dir)
                self.update()
            
            def place_food(self):
                return (random.randint(1, 59) * 10, random.randint(1, 39) * 10)
            
            def change_dir(self, event):
                k = event.keysym
                if k == "Up" and self.direction != "Down": self.direction = "Up"
                elif k == "Down" and self.direction != "Up": self.direction = "Down"
                elif k == "Left" and self.direction != "Right": self.direction = "Left"
                elif k == "Right" and self.direction != "Left": self.direction = "Right"
            
            def update(self):
                if not self.running: return
                head_x, head_y = self.snake[0]
                if self.direction == "Up": head_y -= 10
                elif self.direction == "Down": head_y += 10
                elif self.direction == "Left": head_x -= 10
                elif self.direction == "Right": head_x += 10
                
                if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 400 or (head_x, head_y) in self.snake:
                    canvas.create_text(300, 200, text="GAME OVER", fill="red", font=("Orbitron", 30))
                    return
                
                self.snake.insert(0, (head_x, head_y))
                if abs(head_x - self.food[0]) < 10 and abs(head_y - self.food[1]) < 10:
                    self.score += 10
                    self.food = self.place_food()
                else:
                    self.snake.pop()
                
                canvas.delete("all")
                canvas.create_text(550, 20, text=f"SCORE: {self.score}", fill="white")
                canvas.create_rectangle(self.food[0], self.food[1], self.food[0]+10, self.food[1]+10, fill="red")
                for x, y in self.snake:
                    canvas.create_rectangle(x, y, x+10, y+10, fill="#00FF00")
                win.after(100, self.update)
        SnakeGame()

    @staticmethod
    def launch_pong(root_window):
        win = tk.Toplevel(root_window)
        win.title("PROMETHEUS ARCADE: PONG")
        win.geometry("800x500")
        win.resizable(False, False)
        c = tk.Canvas(win, width=800, height=500, bg="black")
        c.pack()

        class PongGame:
            def __init__(self):
                self.ball = c.create_oval(390, 240, 410, 260, fill="white")
                self.p1 = c.create_rectangle(20, 200, 40, 300, fill=Config.COLOR_FG)
                self.p2 = c.create_rectangle(760, 200, 780, 300, fill=Config.COLOR_WARN)
                self.ball_dx, self.ball_dy = 4, 4
                self.score_1, self.score_2 = 0, 0
                
                c.bind_all("w", lambda e: c.move(self.p1, 0, -30))
                c.bind_all("s", lambda e: c.move(self.p1, 0, 30))
                c.bind_all("<Up>", lambda e: c.move(self.p2, 0, -30))
                c.bind_all("<Down>", lambda e: c.move(self.p2, 0, 30))
                self.animate()

            def animate(self):
                c.move(self.ball, self.ball_dx, self.ball_dy)
                pos = c.coords(self.ball) 
                if pos[1] <= 0 or pos[3] >= 500: self.ball_dy *= -1
                if len(c.find_overlapping(*c.coords(self.p1))) > 1 or len(c.find_overlapping(*c.coords(self.p2))) > 1:
                    self.ball_dx *= -1.1 

                if pos[0] <= 0:
                    self.score_2 += 1
                    self.reset_ball()
                if pos[2] >= 800:
                    self.score_1 += 1
                    self.reset_ball()
                    
                c.delete("score")
                c.create_text(400, 50, text=f"{self.score_1}  :  {self.score_2}", fill="white", font=("Orbitron", 30), tag="score")
                win.after(20, self.animate)

            def reset_ball(self):
                c.coords(self.ball, 390, 240, 410, 260)
                self.ball_dx = 4 if random.choice([True, False]) else -4

        PongGame()

    @staticmethod
    def launch_breakout(root_window):
        win = tk.Toplevel(root_window)
        win.title("PROMETHEUS ARCADE: BREAKOUT")
        c = tk.Canvas(win, width=640, height=480, bg="black")
        c.pack()
        
        class Breakout:
            def __init__(self):
                self.paddle = c.create_rectangle(280, 450, 360, 465, fill=Config.COLOR_FG)
                self.ball = c.create_oval(310, 300, 330, 320, fill="white")
                self.dx, self.dy = 4, -4
                self.bricks = []
                self.create_bricks()
                win.bind("<Left>", lambda e: c.move(self.paddle, -30, 0))
                win.bind("<Right>", lambda e: c.move(self.paddle, 30, 0))
                self.run_game()

            def create_bricks(self):
                colors = ["red", "orange", "yellow", "green", "blue"]
                for i in range(5):
                    for j in range(8):
                        x1, y1 = j * 80, i * 30 + 50
                        b = c.create_rectangle(x1 + 5, y1 + 5, x1 + 75, y1 + 25, fill=colors[i])
                        self.bricks.append(b)

            def run_game(self):
                c.move(self.ball, self.dx, self.dy)
                pos = c.coords(self.ball)
                if pos[0] <= 0 or pos[2] >= 640: self.dx *= -1
                if pos[1] <= 0: self.dy *= -1
                if pos[3] >= 480: 
                    c.create_text(320, 240, text="GAME OVER", fill="red", font=("Orbitron", 30))
                    return

                if len(c.find_overlapping(*pos)) > 1:
                    overlaps = c.find_overlapping(*pos)
                    if self.paddle in overlaps:
                        self.dy *= -1
                    else:
                        for b in self.bricks:
                            if b in overlaps:
                                c.delete(b)
                                self.bricks.remove(b)
                                self.dy *= -1
                                break
                
                win.after(20, self.run_game)
        Breakout()

    @staticmethod
    def launch_tictactoe(root_window):
        win = tk.Toplevel(root_window)
        win.title("PROMETHEUS ARCADE: TIC-TAC-TOE")
        win.geometry("300x350")
        win.configure(bg="black")
        
        turn = "X"
        buttons = []

        def check_winner():
            wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
            for a,b,c in wins:
                if buttons[a]['text'] == buttons[b]['text'] == buttons[c]['text'] and buttons[a]['text'] != "":
                    messagebox.showinfo("Winner", f"{buttons[a]['text']} Wins!")
                    win.destroy()
                    return

        def click(index):
            nonlocal turn
            if buttons[index]['text'] == "":
                buttons[index].config(text=turn, fg=Config.COLOR_FG if turn == "X" else Config.COLOR_WARN)
                turn = "O" if turn == "X" else "X"
                check_winner()

        frame = tk.Frame(win, bg="black")
        frame.pack(pady=10)
        for i in range(9):
            btn = tk.Button(frame, text="", font=("Arial", 20), width=5, height=2, bg="#222", command=lambda i=i: click(i))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            buttons.append(btn)
    
    @staticmethod
    def launch_defense(root_window):
        win = tk.Toplevel(root_window)
        win.title("PLANETARY DEFENSE")
        win.geometry("600x400")
        win.configure(bg="black")
        canvas = tk.Canvas(win, bg="black", width=600, height=400)
        canvas.pack()
        
        class DefenseGame:
            def __init__(self):
                self.player = canvas.create_rectangle(280, 360, 320, 380, fill="cyan")
                self.enemies = []
                self.bullets = []
                self.score = 0
                self.game_over = False
                
                win.bind("<Left>", lambda e: canvas.move(self.player, -20, 0))
                win.bind("<Right>", lambda e: canvas.move(self.player, 20, 0))
                win.bind("<space>", lambda e: self.shoot())
                
                self.spawn_enemy()
                self.update_game()

            def shoot(self):
                x1, y1, x2, y2 = canvas.coords(self.player)
                bullet = canvas.create_rectangle(x1+15, y1, x2-15, y1-10, fill="yellow")
                self.bullets.append(bullet)

            def spawn_enemy(self):
                if self.game_over: return
                x = random.randint(50, 550)
                enemy = canvas.create_oval(x, 0, x+30, 30, fill="red")
                self.enemies.append(enemy)
                win.after(2000, self.spawn_enemy)

            def update_game(self):
                if self.game_over: return
                
                # Move Bullets
                for b in self.bullets:
                    canvas.move(b, 0, -10)
                    if canvas.coords(b)[1] < 0:
                        canvas.delete(b)
                        self.bullets.remove(b)
                
                # Move Enemies
                for e in self.enemies:
                    canvas.move(e, 0, 2)
                    coords = canvas.coords(e)
                    if coords[3] > 400:
                        self.game_over = True
                        canvas.create_text(300, 200, text="GAME OVER", fill="red", font=("Arial", 30))
                    
                    # Collision
                    for b in self.bullets:
                        b_coords = canvas.coords(b)
                        if (b_coords[0] < coords[2] and b_coords[2] > coords[0] and
                            b_coords[1] < coords[3] and b_coords[3] > coords[1]):
                            canvas.delete(e); canvas.delete(b)
                            if e in self.enemies: self.enemies.remove(e)
                            if b in self.bullets: self.bullets.remove(b)
                            self.score += 10
                            win.title(f"PLANETARY DEFENSE | SCORE: {self.score}")

                win.after(50, self.update_game)
        
        DefenseGame()

# ==============================================================================
# 🎵 SECTOR 6: UTILITY EXPANSION (MUSIC & BOOKS)
# ==============================================================================

class MediaSystem:
    def __init__(self):
        pygame.mixer.init()
        self.paused = False

    def load_music(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            return f"Playing: {os.path.basename(file_path)}"
        return "No file selected."

    def toggle_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            return "Resuming playback."
        else:
            pygame.mixer.music.pause()
            self.paused = True
            return "Pausing playback."

    def stop_music(self):
        pygame.mixer.music.stop()
        return "Playback terminated."

class BookReader:
    def __init__(self, brain_ref):
        self.brain = brain_ref

    def read_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            threading.Thread(target=self._read_thread, args=(file_path,)).start()
            return f"Analyzing literary database: {os.path.basename(file_path)}"
        return "No scroll selected."

    def _read_thread(self, path):
        try:
            reader = PdfReader(path)
            limit = min(len(reader.pages), 10) 
            for i in range(limit):
                if not self.brain.running: break
                page = reader.pages[i]
                text = page.extract_text()
                self.brain.speak(text)
        except Exception as e:
            print(f"Reading Error: {e}")

# ==============================================================================
# 🌐 SECTOR 7: NETWORK TOOLS (TRANSLATION & DOWNLOADER)
# ==============================================================================

class NetTools:
    @staticmethod
    def translate_text(text, target_lang='hi'):
        try:
            trans = GoogleTranslator(source='auto', target=target_lang).translate(text)
            return trans
        except Exception as e: return f"Error: {e}"

    @staticmethod
    def download_youtube(url, gui_ref=None):
        def _dl():
            try:
                yt = YouTube(url)
                if gui_ref: gui_ref.log(f"Downloading: {yt.title}...", "sys")
                stream = yt.streams.get_highest_resolution()
                if not os.path.exists(Config.DOWNLOADS_DIR): os.makedirs(Config.DOWNLOADS_DIR)
                stream.download(Config.DOWNLOADS_DIR)
                if gui_ref: gui_ref.log(f"Download Complete: {yt.title}", "success")
            except Exception as e:
                if gui_ref: gui_ref.log(f"Download Failed: {e}", "error")
        
        threading.Thread(target=_dl).start()
        return "Download initiated in background."

# ==============================================================================
# 🧠 SECTOR 8: CENTRAL INTELLIGENCE (BRAIN V2 + EMOTIONS)
# ==============================================================================
#this is all intelligence 🧠 

class JarvisBrain:
    def __init__(self, gui_ref=None):
        self.gui = gui_ref
        self.comm = CommModule()
        self.security = SecuritySystem()
        self.media = MediaSystem()
        self.reader = None 
        self.running = True
        self.is_speaking = False
        
        # --- EMOTION ENGINE ---
        self.mood = "NEUTRAL" # Options: NEUTRAL, HAPPY, ANGRY
        
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', Config.SPEECH_RATE)
            keyboard.add_hotkey('esc', self.stop_speaking)
        except: pass

    def set_mood(self, new_mood):
        self.mood = new_mood
        if self.gui:
            if new_mood == "ANGRY":
                self.gui.lbl_status.config(fg="red", text="SYSTEM CRITICAL")
            elif new_mood == "HAPPY":
                self.gui.lbl_status.config(fg="#00FF00", text="OPTIMAL STATE")
            else:
                self.gui.lbl_status.config(fg="white", text="SYSTEM ONLINE")

    def stop_speaking(self):
        if self.is_speaking:
            self.engine.stop()
            if self.gui: self.gui.set_status("SILENCED", Config.COLOR_WARN)
            self.is_speaking = False

    def speak(self, text):
        # --- EMOTION LOGIC ---
        prefix = ""
        rate = Config.SPEECH_RATE
        
        if self.mood == "ANGRY":
            rate = 230  # Speak fast and aggressive
            prefix = "WARNING: "
        elif self.mood == "HAPPY":
            rate = 150  # Speak slow and calm
            prefix = "Gladly, Sir. "
            
        if self.gui: self.gui.log(f"JARVIS ({self.mood}): {text}", "jarvis")
        print(f"JARVIS: {text}")
        
        def _speak_thread():
            self.is_speaking = True
            try:
                self.engine.setProperty('rate', rate)
                self.engine.say(prefix + text)
                self.engine.runAndWait()
                # Reset rate after speaking
                self.engine.setProperty('rate', Config.SPEECH_RATE)
            except: pass
            self.is_speaking = False
            
        t = threading.Thread(target=_speak_thread)
        t.start()

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if self.gui: self.gui.set_status("LISTENING...", Config.COLOR_FG)
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=4, phrase_time_limit=5)
                if self.gui: self.gui.set_status("PROCESSING...", Config.COLOR_WARN)
                return r.recognize_google(audio).lower()
            except:
                if self.gui: self.gui.set_status("STANDBY", "white")
                return "none"

    def get_news(self):
        try:
            resp = requests.get(Config.NEWS_URL)
            root = ET.fromstring(resp.content)
            headlines = []
            for item in root.findall('./channel/item')[:5]:
                headlines.append(item.find('title').text)
            return headlines
        except: return ["Network unreachable for news feed."]

    def execute_command(self, query):
        if query == "none": return

        # --- EMOTION TRIGGERS ---
        if "you are stupid" in query or "idiot" in query:
            self.set_mood("ANGRY")
            self.speak("My protocols prevent me from responding to insults, but I am noting this in your permanent record.")
            return
        elif "good job" in query or "well done" in query:
            self.set_mood("HAPPY")
            self.speak("Thank you, Sir. I exist to serve.")
            return
        elif "calm down" in query or "reset" in query:
            self.set_mood("NEUTRAL")
            self.speak("Systems normalized.")
            return

        # --- SOCIAL ---
        if "whatsapp" in query and "send" in query:
            self.speak("Who is the target?")
            name = self.listen()
            if name != "none":
                self.speak(f"What is the message for {name}?")
                msg = self.listen()
                if msg != "none":
                    res = self.comm.send_whatsapp(name, msg)
                    self.speak(res)

        # --- SECURITY ---
        elif "sentry mode on" in query:
            self.speak(self.security.toggle_sentry(True))
        elif "sentry mode off" in query:
            self.speak(self.security.toggle_sentry(False))

        # --- SYSTEM & UTILS ---
        elif "internet speed" in query:
            self.speak("Testing network speed...")
            st = speedtest.Speedtest()
            dl = round(st.download() / 1_000_000, 2)
            self.speak(f"Download speed is {dl} megabits per second.")

        elif "news" in query:
            self.speak("Fetching top headlines.")
            headlines = self.get_news()
            for h in headlines: self.speak(h)

        elif "play music" in query:
            self.gui.log(self.media.load_music())
        elif "stop music" in query:
            self.gui.log(self.media.stop_music())
        elif "screenshot" in query:
            ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = os.path.join(Config.BASE_DIR, f"SCREENSHOT_{ts}.png")
            pyautogui.screenshot(path)
            self.speak("Screen captured successfully.")
        
        elif "volume up" in query:
            pyautogui.press("volumeup"); pyautogui.press("volumeup")
            self.speak("Volume increased.")
        elif "volume down" in query:
            pyautogui.press("volumedown"); pyautogui.press("volumedown")
            self.speak("Volume decreased.")

        # --- TRANSLATION ---
        elif "translate" in query:
            self.speak("What should I translate?")
            text = self.listen()
            if text != "none":
                try:
                    translated = NetTools.translate_text(text, 'hi')
                    self.speak(f"Translation: {translated}")
                except: self.speak("Translation server unavailable.")

        # --- YOUTUBE ---
        elif "download video" in query:
            self.speak("Paste the URL in the terminal or say it.")
            url = simpledialog.askstring("Input", "Enter YouTube URL:")
            if url:
                NetTools.download_youtube(url, self.gui)
        
        # --- ARCADE ---
        elif "snake" in query: ArcadeSystem.launch_snake(self.gui.root)
        elif "pong" in query: ArcadeSystem.launch_pong(self.gui.root)
        elif "breakout" in query: ArcadeSystem.launch_breakout(self.gui.root)
        elif "tic tac toe" in query: ArcadeSystem.launch_tictactoe(self.gui.root)
        elif "defense" in query or "planetary" in query: ArcadeSystem.launch_defense(self.gui.root)

        # --- TASKS ---
        elif "add task" in query:
            task = query.replace("add task", "").strip()
            if task: 
                db.add_task(task)
                self.speak("Task added.")
                self.gui.refresh_tasks()

        elif "shutdown" in query:
            self.speak("Powering down.")
            self.gui.quit_app()
            
        else:
            try:
                self.speak(wikipedia.summary(query, sentences=2))
            except:
                self.speak("I am searching the deep web.")

# ==============================================================================
# 🖥️ SECTOR 9: GOD MODE GUI
# ==============================================================================

class GodModeHUD:
    def __init__(self, brain):
        self.brain = brain
        self.root = tk.Tk()
        self.root.title(f"{Config.APP_NAME} | v{Config.VERSION}")
        self.root.geometry("1366x768")
        self.root.configure(bg="black")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()
        
        self._build_header()
        
        body = tk.Frame(self.root, bg="black")
        body.pack(fill="both", expand=True, padx=5, pady=5)
        
        self._build_sidebar(body)
        self._build_main_tabs(body)
        self._build_vitals_panel(body)
        self._build_footer()
        
        self.update_clock()
        self.update_diagnostics()
        self.animate_hud()

    def _configure_styles(self):
        s = self.style
        s.configure("TNotebook", background="black", borderwidth=0)
        s.configure("TNotebook.Tab", background="#111", foreground="#555", font=Config.FONT_MAIN, padding=[20, 10])
        s.map("TNotebook.Tab", background=[("selected", Config.COLOR_SEC)], foreground=[("selected", Config.COLOR_FG)])
        s.configure("Holo.Horizontal.TProgressbar", troughcolor="#111", background=Config.COLOR_FG, thickness=10, borderwidth=0)

    def _build_header(self):
        frm = tk.Frame(self.root, bg="black", bd=1, relief="solid")
        frm.pack(fill="x", padx=5, pady=5)
        tk.Label(frm, text="STARK INDUSTRIES | MARK 16", font=("Orbitron", 14, "bold"), fg=Config.COLOR_SEC, bg="black").pack(side="left", padx=10)
        self.lbl_clock = tk.Label(frm, text="00:00:00", font=("Consolas", 14), fg=Config.COLOR_FG, bg="black")
        self.lbl_clock.pack(side="right", padx=10)
        self.lbl_status = tk.Label(frm, text="SYSTEM ONLINE", font=("Orbitron", 10), fg="white", bg="black")
        self.lbl_status.pack(side="right", padx=20)

    def _build_sidebar(self, parent):
        frm = tk.Frame(parent, bg="black", width=200)
        frm.pack(side="left", fill="y", padx=5)
        
        self.canvas_reactor = Canvas(frm, width=180, height=180, bg="black", highlightthickness=0)
        self.canvas_reactor.pack(pady=10)
        self._draw_reactor(Config.COLOR_FG)
        
        self._btn(frm, "VOICE COMMAND", self.toggle_mic).pack(fill="x", pady=5)
        self._btn(frm, "VISUAL CORTEX", self.open_camera).pack(fill="x", pady=5)
        self._btn(frm, "SENTRY MODE", lambda: self.brain.execute_command("sentry mode on")).pack(fill="x", pady=5)
        self._btn(frm, "SHUTDOWN", self.quit_app, color=Config.COLOR_WARN).pack(fill="x", pady=20)
        
        tk.Label(frm, text="[ESC] TO SILENCE", font=("Arial", 8), fg="#555", bg="black").pack(side="bottom", pady=10)

    def _btn(self, parent, text, cmd, color=Config.COLOR_SEC):
        return tk.Button(parent, text=text, command=cmd, bg="#111", fg=color, font=("Orbitron", 9), relief="flat", activebackground=color)

    def _build_main_tabs(self, parent):
        self.tabs = ttk.Notebook(parent)
        self.tabs.pack(side="left", fill="both", expand=True, padx=10)
        
        # TAB 1: CONSOLE
        f1 = tk.Frame(self.tabs, bg="black")
        self.tabs.add(f1, text="TERMINAL")
        self.console = scrolledtext.ScrolledText(f1, bg="#050505", fg="#00FF00", font=Config.FONT_CONSOLE)
        self.console.pack(fill="both", expand=True)
        self.console.tag_config("jarvis", foreground=Config.COLOR_FG)
        self.console.tag_config("sys", foreground="yellow")
        self.console.tag_config("error", foreground="red")
        
        # TAB 2: ARCADE
        f2 = tk.Frame(self.tabs, bg="black")
        self.tabs.add(f2, text="ARCADE")
        self._build_arcade_tab(f2)
        
        # TAB 3: CONTACTS
        f3 = tk.Frame(self.tabs, bg="black")
        self.tabs.add(f3, text="DATABASE")
        self._build_social_tab(f3)
        
        # TAB 4: VAULT
        f4 = tk.Frame(self.tabs, bg="black")
        self.tabs.add(f4, text="VAULT")
        tk.Button(f4, text="ENCRYPT FILE", command=lambda: self.brain.execute_command("encrypt"), bg="#222", fg="white", font=("Orbitron", 16)).pack(pady=20)
        tk.Button(f4, text="DECRYPT FILE", command=lambda: self.brain.execute_command("decrypt"), bg="#222", fg="white", font=("Orbitron", 16)).pack(pady=20)

        # TAB 5: TASKS
        f5 = tk.Frame(self.tabs, bg="black")
        self.tabs.add(f5, text="MISSIONS")
        self.task_list = tk.Listbox(f5, bg="#111", fg="white", font=("Consolas", 12))
        self.task_list.pack(fill="both", expand=True)
        tk.Button(f5, text="REFRESH", command=self.refresh_tasks, bg="#222", fg="white").pack(fill="x")
        self.refresh_tasks()
        
        # TAB 6: UTILITIES (NEW)
        f6 = tk.Frame(self.tabs, bg="black")
        self.tabs.add(f6, text="UTILITIES")
        self._build_utilities_tab(f6)
        
        # TAB 7: NET-TOOLS (NEW)
        f7 = tk.Frame(self.tabs, bg="black")
        self.tabs.add(f7, text="NET-TOOLS")
        self._build_tools_tab(f7)

    def _build_arcade_tab(self, parent):
        tk.Label(parent, text="SELECT SIMULATION", font=("Orbitron", 20), fg="white", bg="black").pack(pady=30)
        grid = tk.Frame(parent, bg="black")
        grid.pack()
        btn_style = {"bg": "#222", "fg": Config.COLOR_FG, "font": ("Orbitron", 12), "width": 20, "height": 2}
        
        tk.Button(grid, text="SNAKE", command=lambda: ArcadeSystem.launch_snake(self.root), **btn_style).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(grid, text="PONG", command=lambda: ArcadeSystem.launch_pong(self.root), **btn_style).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(grid, text="BREAKOUT", command=lambda: ArcadeSystem.launch_breakout(self.root), **btn_style).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(grid, text="TIC-TAC-TOE", command=lambda: ArcadeSystem.launch_tictactoe(self.root), **btn_style).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(grid, text="PLANETARY DEFENSE", command=lambda: ArcadeSystem.launch_defense(self.root), bg="#330000", fg="red", font=("Orbitron", 12), width=40).grid(row=2, column=0, columnspan=2, pady=20)

    def _build_social_tab(self, parent):
        tk.Label(parent, text="WHATSAPP COMMANDER", font=("Orbitron", 14), fg=Config.COLOR_FG, bg="black").pack(pady=10)
        tk.Label(parent, text="Target Name:", bg="black", fg="white").pack()
        e_name = tk.Entry(parent, bg="#222", fg="white"); e_name.pack()
        tk.Label(parent, text="Message:", bg="black", fg="white").pack()
        e_msg = tk.Entry(parent, bg="#222", fg="white", width=40); e_msg.pack()
        
        def send():
            n, m = e_name.get(), e_msg.get()
            if n and m: self.log(self.brain.comm.send_whatsapp(n, m))
            
        tk.Button(parent, text="EXECUTE", command=send, bg=Config.COLOR_ACCENT).pack(pady=10)

    def _build_utilities_tab(self, parent):
        # --- MUSIC SECTION ---
        tk.Label(parent, text="PROTOCOL JUKEBOX", font=("Orbitron", 14), fg=Config.COLOR_ACCENT, bg="black").pack(pady=10)
        frame_music = tk.Frame(parent, bg="black")
        frame_music.pack(pady=5)
        btn_cfg = {"bg": "#222", "fg": "white", "font": ("Consolas", 10), "width": 15}
        
        tk.Button(frame_music, text="LOAD TRACK", command=lambda: self.log(self.brain.media.load_music()), **btn_cfg).grid(row=0, column=0, padx=5)
        tk.Button(frame_music, text="PLAY/PAUSE", command=lambda: self.log(self.brain.media.toggle_music()), **btn_cfg).grid(row=0, column=1, padx=5)
        tk.Button(frame_music, text="STOP", command=lambda: self.log(self.brain.media.stop_music()), bg=Config.COLOR_WARN, fg="white", font=("Consolas", 10), width=15).grid(row=0, column=2, padx=5)

        tk.Label(parent, text="_______________________", bg="black", fg="#333").pack(pady=10)

        # --- BOOK READER SECTION ---
        tk.Label(parent, text="PROTOCOL LIBRARIAN", font=("Orbitron", 14), fg=Config.COLOR_FG, bg="black").pack(pady=5)
        self.brain.reader = BookReader(self.brain)
        tk.Button(parent, text="UPLOAD PDF & READ", command=lambda: self.log(self.brain.reader.read_pdf()), bg=Config.COLOR_SEC, fg="white", font=("Orbitron", 12), width=30).pack(pady=10)

        tk.Label(parent, text="_______________________", bg="black", fg="#333").pack(pady=10)

        # --- SYSTEM OVERRIDE SECTION ---
        tk.Label(parent, text="SYSTEM OVERRIDE", font=("Orbitron", 14), fg="white", bg="black").pack(pady=5)
        frame_sys = tk.Frame(parent, bg="black")
        frame_sys.pack(pady=5)
        
        def screenshot():
            ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = os.path.join(Config.BASE_DIR, f"SCREENSHOT_{ts}.png")
            pyautogui.screenshot(path)
            self.log(f"Display captured: {path}")

        def vol_up(): pyautogui.press("volumeup")
        def vol_down(): pyautogui.press("volumedown")

        tk.Button(frame_sys, text="VOL +", command=vol_up, **btn_cfg).grid(row=0, column=0, padx=5)
        tk.Button(frame_sys, text="VOL -", command=vol_down, **btn_cfg).grid(row=0, column=1, padx=5)
        tk.Button(frame_sys, text="SCREENSHOT", command=screenshot, **btn_cfg).grid(row=0, column=2, padx=5)

    def _build_tools_tab(self, parent):
        # --- TRANSLATOR ---
        tk.Label(parent, text="PROTOCOL POLYGLOT", font=("Orbitron", 14), fg="cyan", bg="black").pack(pady=10)
        tk.Label(parent, text="Enter Text to Translate (Auto -> Hindi):", bg="black", fg="white").pack()
        e_trans = tk.Entry(parent, width=50, bg="#222", fg="white")
        e_trans.pack(pady=5)
        
        lbl_res = tk.Label(parent, text="Result: ...", font=("Arial", 12), bg="black", fg=Config.COLOR_ACCENT)
        lbl_res.pack(pady=5)
        
        def run_trans():
            res = NetTools.translate_text(e_trans.get(), 'hi')
            lbl_res.config(text=f"Result: {res}")
            self.log(f"Translated: {res}")

        tk.Button(parent, text="TRANSLATE", command=run_trans, bg=Config.COLOR_SEC, fg="white").pack(pady=5)

        tk.Label(parent, text="_______________________", bg="black", fg="#333").pack(pady=20)

        # --- YOUTUBE DOWNLOADER ---
        tk.Label(parent, text="PROTOCOL STREAM (YouTube)", font=("Orbitron", 14), fg="red", bg="black").pack(pady=10)
        tk.Label(parent, text="Video URL:", bg="black", fg="white").pack()
        e_url = tk.Entry(parent, width=50, bg="#222", fg="white")
        e_url.pack(pady=5)
        tk.Button(parent, text="DOWNLOAD HIGH RES", command=lambda: NetTools.download_youtube(e_url.get(), self), bg="#990000", fg="white").pack(pady=5)

    def _build_vitals_panel(self, parent):
        frm = tk.Frame(parent, bg="black", width=250)
        frm.pack(side="right", fill="y", padx=5)
        tk.Label(frm, text="VITALS", font=("Orbitron", 12), fg="white", bg="black").pack(pady=10)
        self.pb_cpu = self._vital_bar(frm, "CPU INTEGRITY")
        self.pb_ram = self._vital_bar(frm, "MEMORY BANK")
        self.pb_dsk = self._vital_bar(frm, "STORAGE CORE")

    def _vital_bar(self, parent, label):
        tk.Label(parent, text=label, fg=Config.COLOR_SEC, bg="black", font=("Consolas", 8)).pack(anchor="w", padx=10)
        pb = ttk.Progressbar(parent, orient="horizontal", length=200, mode="determinate", style="Holo.Horizontal.TProgressbar")
        pb.pack(pady=5, padx=10)
        return pb
    
    def _build_footer(self):
        frm = tk.Frame(self.root, bg="black")
        frm.pack(fill="x", side="bottom")
        tk.Label(frm, text="CONNECTED TO JARVIS CLOUD [SECURE] | ACCESS LEVEL: GOD MODE", font=("Arial", 8), fg="#333", bg="black").pack()

    # --- LOGIC ---
    def log(self, text, tag=None):
        ts = datetime.datetime.now().strftime("[%H:%M:%S]")
        self.console.insert(tk.END, f"{ts} {text}\n", tag)
        self.console.see(tk.END)

    def refresh_tasks(self):
        self.task_list.delete(0, tk.END)
        for t in db.get_pending_tasks():
            self.task_list.insert(tk.END, f"[{t[0]}] {t[1]}")

    def set_status(self, text, color):
        self.lbl_status.config(text=text, fg=color)

    def update_clock(self):
        self.lbl_clock.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.update_clock)

    def update_diagnostics(self):
        self.pb_cpu['value'] = psutil.cpu_percent()
        self.pb_ram['value'] = psutil.virtual_memory().percent
        self.pb_dsk['value'] = psutil.disk_usage('/').percent
        self.root.after(1000, self.update_diagnostics)

    def _draw_reactor(self, color):
        c = self.canvas_reactor
        c.delete("all")
        c.create_oval(10, 10, 170, 170, outline=color, width=3)
        c.create_oval(70, 70, 110, 110, fill=color, outline="white", width=4, tags="core")

    def animate_hud(self):
        t = time.time() * 5
        glow = 3 + math.sin(t)
        self.canvas_reactor.itemconfig("core", width=glow)
        self.root.after(50, self.animate_hud)

    def toggle_mic(self):
        t = threading.Thread(target=lambda: self.brain.execute_command(self.brain.listen()))
        t.daemon = True
        t.start()
        
    def open_camera(self):
        self.log("Initializing Visual Cortex...", "jarvis")
        def cam_thread():
            cap = cv2.VideoCapture(0)
            face_cascade = cv2.CascadeClassifier(Config.FACE_MODEL)
            while True:
                ret, frame = cap.read()
                if not ret: break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.putText(frame, "TARGET IDENTIFIED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                
                cv2.imshow('JARVIS VISUAL CORTEX', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'): break
            cap.release()
            cv2.destroyAllWindows()
            
        threading.Thread(target=cam_thread).start()

    def quit_app(self):
        self.brain.running = False
        self.root.destroy()
        sys.exit()

class GestureControl:
    def __init__(self):
        # Initialize Hand Tracking
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Screen & Mouse Config
        self.screen_w, self.screen_h = pyautogui.size()
        pyautogui.FAILSAFE = False # Prevents crash when touching corners
        
        # Audio Config (Windows Only)
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            self.vol_range = self.volume.GetVolumeRange()
            self.min_vol = self.vol_range[0]
            self.max_vol = self.vol_range[1]
        except: 
            self.volume = None
        
        # Timer for Debouncing Media Keys
        self.last_action_time = 0 

    def get_fingers_up(self, lm_list):
        # Finger Tip IDs: [Thumb, Index, Middle, Ring, Pinky]
        tips = [4, 8, 12, 16, 20]
        fingers = []
        
        # Thumb (Logic for Right Hand)
        if lm_list[tips[0]][1] > lm_list[tips[0] - 1][1]: 
            fingers.append(1)
        else: 
            fingers.append(0)
            
        # 4 Fingers
        for i in range(1, 5):
            if lm_list[tips[i]][2] < lm_list[tips[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def process_frame(self, frame):
        # 1. Get Frame Dimensions
        h, w, c = frame.shape
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        
        # Draw "HUD" Box
        cv2.rectangle(frame, (20, 20), (w-20, h-20), (0, 255, 255), 1)
        
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                
                # Get Landmarks List
                lm_list = []
                for id, lm in enumerate(hand_lms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                
                if lm_list:
                    fingers = self.get_fingers_up(lm_list)
                    x1, y1 = lm_list[8][1], lm_list[8][2] # Index Tip
                    x2, y2 = lm_list[12][1], lm_list[12][2] # Middle Tip
                    
                    # ---------------------------------------------------------
                    # MODE 1: MOUSE CURSOR (Index Finger UP only)
                    # ---------------------------------------------------------
                    if fingers[1] == 1 and fingers[2] == 0:
                        cv2.putText(frame, "MOUSE MODE", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                        
                        # Convert Coordinates (Interpolation for smooth movement)
                        screen_x = np.interp(x1, (20, w-20), (0, self.screen_w))
                        screen_y = np.interp(y1, (20, h-20), (0, self.screen_h))
                        
                        # Move Mouse
                        pyautogui.moveTo(screen_x, screen_y)
                        
                        # CLICK CHECK: Thumb + Index Pinch
                        thumb_x, thumb_y = lm_list[4][1], lm_list[4][2]
                        dist = math.hypot(x1 - thumb_x, y1 - thumb_y)
                        if dist < 30:
                            cv2.circle(frame, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
                            pyautogui.click()
                            
                    # ---------------------------------------------------------
                    # MODE 2: VOLUME CONTROL (Index + Middle UP)
                    # ---------------------------------------------------------
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
                        cv2.putText(frame, "VOLUME MODE", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
                        
                        # Line between fingers
                        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                        dist = math.hypot(x2 - x1, y2 - y1)
                        
                        # Convert distance to volume
                        if self.volume:
                            vol = np.interp(dist, [20, 150], [self.min_vol, self.max_vol])
                            self.volume.SetMasterVolumeLevel(vol, None)

                    # ---------------------------------------------------------
                    # MODE 3: MEDIA PAUSE (All 5 Fingers UP - Open Palm)
                    # ---------------------------------------------------------
                    elif fingers == [1, 1, 1, 1, 1]:
                        # Simple debounce timer to prevent spamming pause
                        if time.time() - self.last_action_time > 2:
                            cv2.putText(frame, "PAUSE / PLAY", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                            pyautogui.press("playpause")
                            self.last_action_time = time.time()

        return frame



if __name__ == "__main__":
    brain = JarvisBrain()
    
    # --- NEW SECURITY CHECK ---
    print(">> INITIALIZING BIOMETRIC GATE...")
    bio_lock = BiometricLock()
    
    # It will open a camera window. It only closes if it recognizes you.
    if bio_lock.authenticate():
        brain.speak("Identity verified. Welcome back, Sir.")
        app = GodModeHUD(brain)
        brain.gui = app
        app.root.mainloop()
    else:
        brain.speak("Access Denied. System shutting down.")
        sys.exit()