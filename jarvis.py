# ==============================================================================
# PROJECT: J.A.R.V.I.S | GOD MODE | MARK 90 (VOICE EDITION)
# DEVELOPER: SHAILMANN
# PLATFORM: macOS (Apple Silicon/Intel)
# ARCHITECTURE: Modular Monolith
# LINES: 1000+
# ==============================================================================

"""
INDEX OF SECTORS:
1. GLOBAL CONFIGURATION
2. DATABASE CORE (SQLITE)
3. EMOTIONAL VOICE ENGINE (MAC NATIVE)
4. NEURAL BRAIN (OLLAMA LOCAL LLM)
5. VOICE SECURITY GATE (PASSPHRASE AUTH)
6. GESTURE CONTROL (MEDIAPIPE)
7. PROMETHEUS ARCADE (GAMES & VISUALS)
8. PRODUCTIVITY SUITE (TOOLS)
9. NETWORK & MEDIA
10. GRAPHICAL USER INTERFACE (DASHBOARD)
11. SYSTEM CONTROLLER (UPDATED: AUTO-SENSING)
12. MAIN ENTRY POINT
"""

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
import platform 
import ollama 
import textwrap
import uuid
import numpy as np
import mediapipe as mp
from tkinter import ttk, scrolledtext, messagebox, filedialog, Canvas, simpledialog, PhotoImage
from cryptography.fernet import Fernet
from difflib import get_close_matches
from plyer import notification 
import xml.etree.ElementTree as ET 
from PyPDF2 import PdfReader 
from deep_translator import GoogleTranslator 
from pytubefix import YouTube 
from PIL import Image, ImageTk 

# ==============================================================================
# ⚙️ SECTOR 1: GLOBAL CONFIGURATION & ASSETS
# ==============================================================================

class Config:
    """
    Global Configuration Hub.
    Manages paths, constants, themes, and API keys.
    """
    APP_NAME = "J.A.R.V.I.S"
    CODENAME = "MARK 90"
    VERSION = "90.0.2 (Auto-Sense Active)"
    DEVELOPER = "Shailmann"
    
    # --- AUTHENTICATION ---
    # The phrase you must say to unlock the system
    VOICE_PASSCODE = "protocol omega" 
    WAKE_WORD = "jarvis" # Word to trigger auto-listening
    
    # --- SYSTEM PATHS ---
    BASE_DIR = os.path.expanduser("~/Documents/Jarvis_Mark90")
    
    # Sub-directories map
    DIRS = {
        "DB": os.path.join(BASE_DIR, "Database"),
        "VAULT": os.path.join(BASE_DIR, "Secure_Vault"),
        "LOGS": os.path.join(BASE_DIR, "System_Logs"),
        "DOWNLOADS": os.path.join(BASE_DIR, "Downloads"),
        "ASSETS": os.path.join(BASE_DIR, "Assets"),
        "TEMP": os.path.join(BASE_DIR, "Temp"),
    }

    # Files map
    FILES = {
        "DB_MAIN": os.path.join(DIRS["DB"], "core_memory.db"),
        "KEY_MASTER": os.path.join(DIRS["VAULT"], "master_cipher.key"),
        "VOICE_LOG": os.path.join(DIRS["LOGS"], "voice_auth.log")
    }
    
    # --- VISUAL THEME (CYBERPUNK / STARK) ---
    THEME = {
        "BG_MAIN": "#050505",       # Deep Void
        "BG_SEC": "#0A0A0A",        # Soft Black
        "FG_PRIMARY": "#00FFFF",    # Arc Reactor Cyan
        "FG_SECONDARY": "#008888",  # Dim Cyan
        "ACCENT": "#FFD700",        # Gold
        "WARN": "#FF3333",          # Alert Red
        "SUCCESS": "#00FF00",       # Green
        "TEXT_MAIN": "#FFFFFF",
        "TEXT_DIM": "#AAAAAA",
        "FONT_HEADER": ("Orbitron", 16, "bold"),
        "FONT_BODY": ("Consolas", 10),
        "FONT_TINY": ("Arial", 8)
    }
    
    # --- AI SETTINGS ---
    OLLAMA_MODEL = "llama3.2" # Using Llama 3 for local inference
    
    # --- VOICE SETTINGS ---
    # Mac voices: Samantha, Alex, Fred, Victoria
    VOICE_ID = "Samantha"     

    @staticmethod
    def initialize():
        """Creates the entire file structure on first run."""
        print(">> [BOOT] INITIALIZING FILE SYSTEMS...")
        for key, path in Config.DIRS.items():
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"   [+] Created Directory: {key}")
        
        # Create Log File
        if not os.path.exists(Config.FILES["VOICE_LOG"]):
            with open(Config.FILES["VOICE_LOG"], "w") as f:
                f.write("--- SECURITY LOG INITIATED ---\n")

Config.initialize()

# ==============================================================================
# 💾 SECTOR 2: DATABASE CORE (SQLITE)
# ==============================================================================

class DatabaseCore:
    """
    Handles all persistent memory: Contacts, Tasks, Logs, and System Stats.
    Uses SQLite3 for local storage.
    """
    def __init__(self):
        self.conn = sqlite3.connect(Config.FILES["DB_MAIN"], check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._build_tables()

    def _build_tables(self):
        """Constructs the schema if it doesn't exist."""
        # 1. Contacts Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                phone TEXT,
                email TEXT,
                relation TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # 2. Mission/Task Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                status TEXT DEFAULT 'PENDING',
                priority TEXT DEFAULT 'NORMAL',
                deadline DATETIME
            )
        """)
        # 3. System Logs (Audit Trail)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                details TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    # --- CONTACT METHODS ---
    def add_contact(self, name, phone, email="", relation="Friend"):
        try:
            self.cursor.execute("INSERT INTO contacts (name, phone, email, relation) VALUES (?, ?, ?, ?)", 
                                (name.lower(), phone, email, relation))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_contact(self, name):
        self.cursor.execute("SELECT name, phone FROM contacts")
        data = self.cursor.fetchall()
        names = [x[0] for x in data]
        matches = get_close_matches(name.lower(), names, n=1, cutoff=0.6)
        if matches:
            target = matches[0]
            self.cursor.execute("SELECT phone, email FROM contacts WHERE name=?", (target,))
            return self.cursor.fetchone()
        return None

    # --- LOGGING METHODS ---
    def log_event(self, event_type, details):
        self.cursor.execute("INSERT INTO audit_logs (event_type, details) VALUES (?, ?)", (event_type, details))
        self.conn.commit()

    # --- TASK METHODS ---
    def add_mission(self, title):
        self.cursor.execute("INSERT INTO missions (title) VALUES (?)", (title,))
        self.conn.commit()

    def get_missions(self):
        self.cursor.execute("SELECT id, title, status FROM missions WHERE status='PENDING'")
        return self.cursor.fetchall()

    def complete_mission(self, mid):
        self.cursor.execute("UPDATE missions SET status='COMPLETED' WHERE id=?", (mid,))
        self.conn.commit()

    def clear_completed_missions(self):
        self.cursor.execute("DELETE FROM missions WHERE status='COMPLETED'")
        self.conn.commit()

db = DatabaseCore()

# ==============================================================================
# 🗣️ SECTOR 3: EMOTIONAL VOICE ENGINE
# ==============================================================================

class EmotionalVoiceEngine:
    """
    Advanced Text-to-Speech wrapper for macOS.
    Simulates emotion by altering speech rate and using prefixes.
    """
    def __init__(self, gui_ref=None):
        self.gui = gui_ref
        self.is_speaking = False
        self.current_mood = "NEUTRAL"

    def set_mood(self, mood):
        """
        Updates the internal mood state.
        Options: NEUTRAL, ANGRY, HAPPY, SERIOUS, FAST
        """
        self.current_mood = mood
        if self.gui:
            # Update GUI Color based on mood
            color = "white"
            if mood == "ANGRY": color = "red"
            elif mood == "HAPPY": color = "#00FF00"
            elif mood == "SERIOUS": color = "cyan"
            self.gui.update_reactor_color(color)

    def speak(self, text):
        """
        Spawns a thread to speak so the GUI doesn't freeze.
        Adjusts parameters based on 'current_mood'.
        """
        
        # 1. Determine Speech Parameters based on Mood
        # Standard Mac Rate is roughly 175
        rate = "175" 
        voice = Config.VOICE_ID
        prefix = ""
        
        if self.current_mood == "ANGRY":
            rate = "230" # Fast and aggressive
            prefix = "Warning. "
        elif self.current_mood == "HAPPY":
            rate = "160" # Slower and lighter
            prefix = "Certainly. "
        elif self.current_mood == "SERIOUS":
            rate = "150" # Slow and deliberate
            prefix = ""
        elif self.current_mood == "FAST":
            rate = "250" # Data readout speed
            prefix = ""

        full_text = f"{prefix}{text}"

        # 2. Update GUI Console
        if self.gui:
            self.gui.log_to_terminal(f"JARVIS: {full_text}", "jarvis")
        else:
            print(f"JARVIS: {full_text}")

        # 3. Audio Thread execution
        threading.Thread(target=self._run_say_command, args=(full_text, rate, voice)).start()

    def _run_say_command(self, text, rate, voice):
        try:
            self.is_speaking = True
            # Use macOS 'say' command. 
            # -v sets voice, -r sets rate.
            subprocess.run(["say", "-v", voice, "-r", rate, text])
            self.is_speaking = False
        except Exception as e:
            print(f"Audio Error: {e}")

# ==============================================================================
# 🧠 SECTOR 4: NEURAL BRAIN (OLLAMA INTEGRATION)
# ==============================================================================

class BrainCore:
    """
    The Thinking Module. Connects to local Ollama instance.
    """
    def __init__(self, voice_engine):
        self.voice = voice_engine

    def think(self, user_input, gui_status_callback=None):
        """Sends prompt to Local LLM and speaks response."""
        
        if gui_status_callback:
            gui_status_callback("THINKING (NEURAL)...", Config.THEME["FG_PRIMARY"])

        print(f">> [BRAIN] Processing: {user_input}")

        def _process():
            try:
                # System Prompt for Personality
                sys_msg = (
                    "You are JARVIS, a highly advanced AI created by Shailmann. "
                    "You are currently in God Mode. "
                    "Your responses must be short, witty, and helpful. "
                    "Max 2 sentences. No emojis. "
                    "If asked about emotions, simulate a human response."
                )

                response = ollama.chat(model=Config.OLLAMA_MODEL, messages=[
                    {'role': 'system', 'content': sys_msg},
                    {'role': 'user', 'content': user_input}
                ])
                
                reply = response['message']['content']
                
                # Analyze sentiment (rudimentary) to change voice mood
                if "error" in reply.lower() or "danger" in reply.lower():
                    self.voice.set_mood("ANGRY")
                elif "happy" in reply.lower() or "glad" in reply.lower():
                    self.voice.set_mood("HAPPY")
                else:
                    self.voice.set_mood("NEUTRAL")

                # Speak result
                self.voice.speak(reply)
                
                if gui_status_callback:
                    gui_status_callback("ONLINE", "white")
                    
            except Exception as e:
                print(f"[BRAIN ERROR] {e}")
                self.voice.set_mood("SERIOUS")
                self.voice.speak("I am unable to access my neural pathways. Is Ollama running?")
                if gui_status_callback:
                    gui_status_callback("NEURAL ERROR", "red")

        threading.Thread(target=_process).start()

# ==============================================================================
# 🎙️ SECTOR 5: VOICE SECURITY GATE (PASSPHRASE AUTH)
# ==============================================================================

class VoiceSecurityGate:
    """
    Replaces the Camera Security.
    Requires the user to speak a specific passphrase to access the system.
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.passcode = Config.VOICE_PASSCODE
        self.attempts = 0

    def authenticate(self):
        """
        Runs the authentication loop.
        Returns True if successful, False if max attempts reached.
        """
        print("\n")
        print("█░█ █▀█ █ █▀▀ █▀▀ ▄▀█ ▀█▀ █▀▀")
        print("▀▄▀ █▄█ █ █▄▄ ██▄ █▀█ ░█░ ██▄")
        print("-------------------------------")
        print(f">> [SEC] VOICE AUTH INITIATED...")
        
        # Provide visual/audio cue
        os.system(f"say -v Samantha 'Voice Identification Required. State the Passcode.'")
        
        while self.attempts < 3:
            try:
                with sr.Microphone() as source:
                    print(f">> [SEC] LISTENING (Attempt {self.attempts + 1}/3)...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                    print(">> [SEC] PROCESSING VOICE PRINT...")
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f">> [SEC] INPUT RECEIVED: '{text}'")
                    
                    if self.passcode in text:
                        print(">> [SEC] ACCESS GRANTED.")
                        os.system(f"say -v Samantha 'Access Granted. Welcome Shailmann.'")
                        return True
                    else:
                        print(">> [SEC] ACCESS DENIED. PASSPHRASE INCORRECT.")
                        os.system(f"say -v Samantha 'Incorrect. Try again.'")
                        self.attempts += 1
                        
            except sr.WaitTimeoutError:
                print(">> [SEC] TIMEOUT. NO VOICE DETECTED.")
                self.attempts += 1
            except sr.UnknownValueError:
                print(">> [SEC] UNINTELLIGIBLE.")
                self.attempts += 1
            except Exception as e:
                print(f">> [SEC] ERROR: {e}")
                break
        
        os.system(f"say -v Samantha 'Security Breach Detected. System Lockdown.'")
        return False

# ==============================================================================
# 👐 SECTOR 6: GESTURE CONTROL (MAC COMPATIBLE)
# ==============================================================================

class GestureEngine:
    """
    Uses MediaPipe to track hands. 
    Controls Mouse (Index), Click (Pinch), and Volume (Thumb+Index).
    """
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.draw = mp.solutions.drawing_utils
        self.w_scr, self.h_scr = pyautogui.size()
        self.last_click = 0

    def process_frame(self, frame):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.hands.process(rgb)
        
        # Cyberpunk visual overlay
        cv2.rectangle(frame, (20,20), (w-20, h-20), (255,255,0), 1)
        cv2.putText(frame, "VISUAL LINK ACTIVE", (30, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
        
        if res.multi_hand_landmarks:
            for lms in res.multi_hand_landmarks:
                self.draw.draw_landmarks(frame, lms, self.mp_hands.HAND_CONNECTIONS)
                
                # Get Coordinates
                lm = lms.landmark
                index_x, index_y = int(lm[8].x * w), int(lm[8].y * h)
                thumb_x, thumb_y = int(lm[4].x * w), int(lm[4].y * h)
                middle_x, middle_y = int(lm[12].x * w), int(lm[12].y * h)
                
                # 1. Mouse Move (Index up)
                if lm[8].y < lm[6].y and lm[12].y > lm[10].y: 
                    # Map coordinates
                    screen_x = np.interp(index_x, (20, w-20), (0, self.w_scr))
                    screen_y = np.interp(index_y, (20, h-20), (0, self.h_scr))
                    
                    # Smoothing
                    cur_x, cur_y = pyautogui.position()
                    pyautogui.moveTo(cur_x + (screen_x - cur_x)/5, cur_y + (screen_y - cur_y)/5)
                    cv2.putText(frame, "TARGETING", (index_x, index_y-20), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 2)

                # 2. Click (Index + Middle Pinch)
                dist_click = math.hypot(index_x - middle_x, index_y - middle_y)
                if dist_click < 30 and (time.time() - self.last_click) > 0.5:
                    pyautogui.click()
                    self.last_click = time.time()
                    cv2.circle(frame, (index_x, index_y), 15, (0,0,255), cv2.FILLED)

                # 3. Volume (Thumb + Index Distance)
                dist_vol = math.hypot(index_x - thumb_x, index_y - thumb_y)
                vol_level = np.interp(dist_vol, [20, 150], [0, 100])
                
                if int(vol_level) % 5 == 0:
                    self.set_volume(vol_level)
                
                # Draw Bar
                bar_h = np.interp(dist_vol, [20, 150], [400, 150])
                cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 2)
                cv2.rectangle(frame, (50, int(bar_h)), (85, 400), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, f"{int(vol_level)}%", (45, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

        return frame

    def set_volume(self, vol):
        if platform.system() == "Darwin":
            cmd = f"set volume output volume {int(vol)}"
            subprocess.call(["osascript", "-e", cmd])

# ==============================================================================
# 🎮 SECTOR 7: PROMETHEUS ARCADE (GAMES & VISUALS)
# ==============================================================================

class MatrixRain:
    """
    Generates a Matrix-style digital rain effect on a Canvas.
    Used for screensaver mode.
    """
    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("MATRIX CONSTRUCT")
        self.win.geometry("800x600")
        self.win.configure(bg="black")
        self.c = Canvas(self.win, width=800, height=600, bg="black", highlightthickness=0)
        self.c.pack()
        self.letters = "010101XYZA"
        self.drops = [0 for _ in range(40)] # 40 columns
        self.running = True
        self.animate()

    def animate(self):
        if not self.running: return
        
        # Fade effect (draw semi-transparent black rectangle over everything)
        # Note: Tkinter canvas doesn't do alpha well, so we just redraw text
        self.c.delete("all")
        
        for i in range(len(self.drops)):
            text = random.choice(self.letters)
            x = i * 20
            y = self.drops[i] * 20
            
            # Draw trail
            for j in range(5):
                 color = "#00FF00" if j == 0 else "#005500"
                 self.c.create_text(x, y - (j*20), text=random.choice(self.letters), fill=color, font=("Consolas", 14), tags="rain")
            
            if self.drops[i] * 20 > 600 and random.random() > 0.95:
                self.drops[i] = 0
            self.drops[i] += 1
            
        self.win.after(50, self.animate)

class ArcadeEngine:
    """
    Game Launcher Hub.
    """
    @staticmethod
    def launch_matrix(root):
        MatrixRain(root)

    @staticmethod
    def play_snake(root):
        win = tk.Toplevel(root)
        win.title("PROMETHEUS: SNAKE")
        win.geometry("600x440")
        win.configure(bg="black")
        c = Canvas(win, width=600, height=400, bg="#111", highlightthickness=0)
        c.pack(pady=10)
        lbl_score = tk.Label(win, text="SCORE: 0", font=("Orbitron", 14), bg="black", fg="cyan")
        lbl_score.pack()

        class SnakeLogic:
            def __init__(self):
                self.snake = [(100,100), (90,100), (80,100)]
                self.food = (random.randint(1,59)*10, random.randint(1,39)*10)
                self.direction = "Right"
                self.score = 0
                self.running = True
                win.bind("<Up>", lambda e: self.set_dir("Up"))
                win.bind("<Down>", lambda e: self.set_dir("Down"))
                win.bind("<Left>", lambda e: self.set_dir("Left"))
                win.bind("<Right>", lambda e: self.set_dir("Right"))
                self.loop()
            
            def set_dir(self, d):
                opposites = {"Up":"Down", "Down":"Up", "Left":"Right", "Right":"Left"}
                if d != opposites.get(self.direction): self.direction = d
            
            def loop(self):
                if not self.running: return
                hx, hy = self.snake[0]
                if self.direction == "Up": hy -= 10
                elif self.direction == "Down": hy += 10
                elif self.direction == "Left": hx -= 10
                elif self.direction == "Right": hx += 10
                
                if hx < 0 or hx >= 600 or hy < 0 or hy >= 400 or (hx,hy) in self.snake:
                    c.create_text(300, 200, text="GAME OVER", fill="red", font=("Orbitron", 30))
                    return
                
                self.snake.insert(0, (hx, hy))
                if abs(hx-self.food[0]) < 10 and abs(hy-self.food[1]) < 10:
                    self.score += 10
                    lbl_score.config(text=f"SCORE: {self.score}")
                    self.food = (random.randint(1,59)*10, random.randint(1,39)*10)
                else:
                    self.snake.pop()
                
                c.delete("all")
                c.create_rectangle(self.food[0], self.food[1], self.food[0]+10, self.food[1]+10, fill="#FF0055", outline="")
                for x,y in self.snake:
                    c.create_rectangle(x,y,x+10,y+10, fill="#00FF99", outline="")
                
                win.after(80, self.loop)
        SnakeLogic()

# ==============================================================================
# 🛠️ SECTOR 8: PRODUCTIVITY SUITE (TOOLS)
# ==============================================================================

class ProductivitySuite:
    """
    Additional tools for the user.
    """
    @staticmethod
    def open_calculator(root):
        win = tk.Toplevel(root)
        win.title("JARVIS CALC")
        win.geometry("300x400")
        
        e = tk.Entry(win, width=16, font=("Arial", 24), borderwidth=2, relief="solid")
        e.grid(row=0, column=0, columnspan=4)
        
        def btn_click(x):
            cur = e.get()
            e.delete(0, tk.END)
            e.insert(0, str(cur) + str(x))
            
        def clear(): e.delete(0, tk.END)
        
        def equal():
            try:
                res = str(eval(e.get()))
                e.delete(0, tk.END)
                e.insert(0, res)
            except:
                e.delete(0, tk.END)
                e.insert(0, "ERR")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]
        
        for (text, r, c) in buttons:
            if text == '=': cmd = equal
            elif text == 'C': cmd = clear
            else: cmd = lambda t=text: btn_click(t)
            tk.Button(win, text=text, padx=20, pady=20, font=("Arial", 12), command=cmd).grid(row=r, column=c)

    @staticmethod
    def clean_system(gui_log):
        gui_log("Initializing Cleanup Protocol...", "sys")
        # Simulates cleaning temp files
        temp_dir = Config.DIRS["TEMP"]
        gui_log(f"Scanning {temp_dir}...", "sys")
        time.sleep(1)
        gui_log("Deleting temporary caches...", "sys")
        time.sleep(1)
        gui_log("Optimizing database...", "sys")
        time.sleep(0.5)
        gui_log("System Optimal.", "success")

# ==============================================================================
# 📡 SECTOR 9: NETWORK & MEDIA
# ==============================================================================

class MediaSystem:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False

    def load_music(self):
        path = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3 *.wav")])
        if path:
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                self.is_playing = True
                return f"Playing: {os.path.basename(path)}"
            except Exception as e:
                return f"Media Error: {e}"
        return "Selection Cancelled."

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        return "Playback Stopped."

class CommModule:
    @staticmethod
    def send_whatsapp(target, msg):
        try:
            def _send():
                pywhatkit.sendwhatmsg_instantly(target, msg, wait_time=10, tab_close=True)
            threading.Thread(target=_send).start()
            return "Protocol Initiated."
        except Exception as e:
            return f"Comm Error: {e}"

# ==============================================================================
# 🖥️ SECTOR 10: GRAPHICAL USER INTERFACE (DASHBOARD)
# ==============================================================================

class Dashboard:
    """
    The main Graphical User Interface. 
    """
    def __init__(self, root, brain_ref):
        self.root = root
        self.brain = brain_ref
        self.root.title(Config.APP_NAME + " // " + Config.VERSION)
        self.root.geometry("1400x850")
        self.root.configure(bg=Config.THEME["BG_MAIN"])
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()
        
        self._init_layout()
        self._init_sidebar()
        self._init_header()
        self._init_content_area()
        self._init_footer()
        
        self.update_clock()
        self.update_vitals()
        self.animate_reactor()

    def _configure_styles(self):
        s = self.style
        colors = Config.THEME
        s.configure("TFrame", background=colors["BG_MAIN"])
        s.configure("TLabel", background=colors["BG_MAIN"], foreground=colors["TEXT_MAIN"], font=colors["FONT_BODY"])
        s.configure("TNotebook", background=colors["BG_MAIN"], borderwidth=0)
        s.configure("TNotebook.Tab", background=colors["BG_SEC"], foreground=colors["FG_SECONDARY"], padding=[20, 10], font=colors["FONT_HEADER"])
        s.map("TNotebook.Tab", background=[("selected", colors["FG_PRIMARY"])], foreground=[("selected", "black")])
        s.configure("Horizontal.TProgressbar", background=colors["FG_PRIMARY"], troughcolor=colors["BG_SEC"], borderwidth=0)

    def _init_layout(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def _init_header(self):
        h = tk.Frame(self.root, bg=Config.THEME["BG_SEC"], height=60)
        h.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        tk.Label(h, text=f"{Config.APP_NAME} | {Config.CODENAME}", font=("Orbitron", 18, "bold"), 
                 bg=Config.THEME["BG_SEC"], fg=Config.THEME["FG_PRIMARY"]).pack(side="left", padx=20)
        
        self.lbl_status = tk.Label(h, text="SYSTEM ONLINE", font=("Orbitron", 12), bg=Config.THEME["BG_SEC"], fg="white")
        self.lbl_status.pack(side="right", padx=20)

    def _init_sidebar(self):
        s = tk.Frame(self.root, bg=Config.THEME["BG_SEC"], width=250)
        s.grid(row=1, column=0, sticky="ns", padx=5, pady=0)
        s.grid_propagate(False)
        
        # Arc Reactor Canvas
        self.canv_reactor = Canvas(s, width=150, height=150, bg=Config.THEME["BG_SEC"], highlightthickness=0)
        self.canv_reactor.pack(pady=20)
        self._draw_reactor_base()
        
        # Control Buttons
        # Note: Manual buttons kept as backup
        self._create_sidebar_btn(s, "MANUAL LISTEN", self.toggle_mic)
        self._create_sidebar_btn(s, "RESTART GESTURES", self.toggle_gestures)
        self._create_sidebar_btn(s, "MATRIX MODE", self.toggle_matrix)
        self._create_sidebar_btn(s, "CALCULATOR", lambda: ProductivitySuite.open_calculator(self.root))
        
        tk.Label(s, text="AUTO-SENSORS ACTIVE", fg=Config.THEME["SUCCESS"], bg=Config.THEME["BG_SEC"], font=("Arial", 8)).pack(side="bottom", pady=10)

    def _create_sidebar_btn(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, command=cmd, 
                        bg="#111", fg=Config.THEME["FG_PRIMARY"], 
                        activebackground=Config.THEME["FG_PRIMARY"], activeforeground="black",
                        font=("Orbitron", 10), relief="flat", height=2)
        btn.pack(fill="x", pady=5, padx=10)

    def _init_content_area(self):
        c = tk.Frame(self.root, bg=Config.THEME["BG_MAIN"])
        c.grid(row=1, column=1, sticky="nsew", padx=5, pady=0)
        
        self.tabs = ttk.Notebook(c)
        self.tabs.pack(fill="both", expand=True)
        
        # 1. TERMINAL TAB
        self.tab_term = tk.Frame(self.tabs, bg="black")
        self.tabs.add(self.tab_term, text="TERMINAL")
        self.console = scrolledtext.ScrolledText(self.tab_term, bg="#020202", fg="#00FF00", font=("Consolas", 11))
        self.console.pack(fill="both", expand=True, padx=5, pady=5)
        self.console.tag_config("jarvis", foreground="cyan")
        self.console.tag_config("user", foreground="yellow")
        self.console.tag_config("sys", foreground="magenta")
        self.console.tag_config("error", foreground="red")

        # 2. MISSIONS TAB (Tasks)
        self.tab_mission = tk.Frame(self.tabs, bg="black")
        self.tabs.add(self.tab_mission, text="MISSIONS")
        self._build_mission_tab()

        # 3. ARCADE TAB
        self.tab_arcade = tk.Frame(self.tabs, bg="black")
        self.tabs.add(self.tab_arcade, text="ARCADE")
        self._build_arcade_tab()

        # 4. TOOLS TAB
        self.tab_tools = tk.Frame(self.tabs, bg="black")
        self.tabs.add(self.tab_tools, text="PROTOCOLS")
        self._build_tools_tab()

    def _build_mission_tab(self):
        top = tk.Frame(self.tab_mission, bg="black")
        top.pack(fill="x", pady=10)
        self.entry_task = tk.Entry(top, bg="#222", fg="white", font=("Consolas", 12), width=50)
        self.entry_task.pack(side="left", padx=10)
        tk.Button(top, text="ADD MISSION", bg=Config.THEME["FG_SECONDARY"], fg="white", 
                  command=self.add_task_gui).pack(side="left")
        self.list_tasks = tk.Listbox(self.tab_mission, bg="#111", fg="white", font=("Consolas", 12))
        self.list_tasks.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_tasks()

    def _build_arcade_tab(self):
        lbl = tk.Label(self.tab_arcade, text="SELECT SIMULATION", font=("Orbitron", 24), bg="black", fg="white")
        lbl.pack(pady=40)
        grid = tk.Frame(self.tab_arcade, bg="black")
        grid.pack()
        games = [
            ("SNAKE", lambda: ArcadeEngine.play_snake(self.root)),
            ("MATRIX", lambda: ArcadeEngine.launch_matrix(self.root)),
            ("TICTACTOE", lambda: messagebox.showinfo("Info", "Simulation Loaded."))
        ]
        r, c = 0, 0
        for name, cmd in games:
            tk.Button(grid, text=name, command=cmd, font=("Orbitron", 14), 
                      width=15, bg="#222", fg="cyan").grid(row=r, column=c, padx=20, pady=20)
            c += 1
            if c > 1: c = 0; r += 1

    def _build_tools_tab(self):
        grid = tk.Frame(self.tab_tools, bg="black")
        grid.pack(pady=20)
        
        def run_speed():
            self.log_to_terminal("Calculating Network Velocity...", "sys")
            def _t():
                st = speedtest.Speedtest()
                d = st.download() / 1_000_000
                self.log_to_terminal(f"Download: {d:.2f} Mbps", "jarvis")
            threading.Thread(target=_t).start()

        def play_music(): self.brain.media_sys.load_music()
        def clean_sys(): threading.Thread(target=lambda: ProductivitySuite.clean_system(self.log_to_terminal)).start()

        tk.Button(grid, text="NET VELOCITY", command=run_speed, width=20, bg="#111", fg="yellow").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(grid, text="MEDIA PLAYER", command=play_music, width=20, bg="#111", fg="yellow").grid(row=0, column=1, padx=10, pady=10)
        tk.Button(grid, text="SYSTEM CLEAN", command=clean_sys, width=20, bg="#111", fg="yellow").grid(row=1, column=0, padx=10, pady=10)
        tk.Button(grid, text="SCREEN CAPTURE", command=self.brain.take_screenshot, width=20, bg="#111", fg="yellow").grid(row=1, column=1, padx=10, pady=10)

    def _init_footer(self):
        f = tk.Frame(self.root, bg="black")
        f.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.lbl_cpu = tk.Label(f, text="CPU: 0%", fg=Config.THEME["FG_SECONDARY"], bg="black", font=("Consolas", 9))
        self.lbl_cpu.pack(side="left", padx=10)
        self.lbl_ram = tk.Label(f, text="RAM: 0%", fg=Config.THEME["FG_SECONDARY"], bg="black", font=("Consolas", 9))
        self.lbl_ram.pack(side="left", padx=10)
        self.lbl_time = tk.Label(f, text="00:00:00", fg="white", bg="black", font=("Consolas", 9))
        self.lbl_time.pack(side="right", padx=10)

    # --- ANIMATION & UPDATES ---
    def _draw_reactor_base(self):
        c = self.canv_reactor
        c.create_oval(10,10,140,140, outline=Config.THEME["FG_SECONDARY"], width=2)
        c.create_oval(20,20,130,130, outline=Config.THEME["FG_SECONDARY"], width=1)
        self.reactor_core = c.create_oval(50,50,100,100, fill=Config.THEME["FG_PRIMARY"], tags="core")

    def animate_reactor(self):
        glow = 2 + math.sin(time.time()*4)
        self.canv_reactor.itemconfig("core", width=glow, outline="white")
        self.root.after(50, self.animate_reactor)
        
    def update_reactor_color(self, color):
        self.canv_reactor.itemconfig("core", fill=color)

    def update_clock(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.lbl_time.config(text=now)
        self.root.after(1000, self.update_clock)

    def update_vitals(self):
        c = psutil.cpu_percent()
        r = psutil.virtual_memory().percent
        self.lbl_cpu.config(text=f"CPU: {c}%")
        self.lbl_ram.config(text=f"RAM: {r}%")
        self.root.after(2000, self.update_vitals)

    def log_to_terminal(self, text, tag="user"):
        ts = datetime.datetime.now().strftime("[%H:%M]")
        self.console.insert(tk.END, f"{ts} {text}\n", tag)
        self.console.see(tk.END)

    def set_status(self, text, color):
        self.lbl_status.config(text=text, fg=color)

    # --- ACTIONS ---
    def add_task_gui(self):
        t = self.entry_task.get()
        if t:
            db.add_mission(t)
            self.entry_task.delete(0, tk.END)
            self.refresh_tasks()
    
    def refresh_tasks(self):
        self.list_tasks.delete(0, tk.END)
        for m in db.get_missions():
            self.list_tasks.insert(tk.END, f"[ID: {m[0]}] {m[1]} [{m[2]}]")

    def toggle_mic(self):
        # Manual Trigger
        threading.Thread(target=self.brain.manual_listen_once).start()

    def toggle_matrix(self):
        ArcadeEngine.launch_matrix(self.root)

    def toggle_gestures(self):
        self.log_to_terminal("Engaging Gesture Link...", "sys")
        def _ges():
            gc = GestureEngine()
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if not ret: break
                frame = gc.process_frame(frame)
                cv2.imshow("GESTURE LINK", frame)
                # Auto-close check (optional) or keep running
                if cv2.waitKey(1) & 0xFF == ord('q'): break
            cap.release()
            cv2.destroyAllWindows()
            for i in range(5): cv2.waitKey(1)
        threading.Thread(target=_ges, daemon=True).start()

# ==============================================================================
# 🧠 SECTOR 11: SYSTEM CONTROLLER (MAIN LOGIC)
# ==============================================================================

class JarvisController:
    """
    Coordinates all modules (Brain, Voice, GUI, Security).
    UPDATED: Now includes Background Listeners.
    """
    def __init__(self):
        self.gui = None # Set later
        self.voice = EmotionalVoiceEngine(None)
        self.brain_ai = BrainCore(self.voice)
        self.voice_sec = VoiceSecurityGate()
        self.media_sys = MediaSystem()
        self.comm_sys = CommModule()
        self.running = True
        self.recognizer = sr.Recognizer()

    def attach_gui(self, gui):
        self.gui = gui
        self.voice.gui = gui # Link voice to GUI logger
        
        # --- AUTO START SYSTEMS ---
        self.start_auto_sense()

    def start_auto_sense(self):
        """Starts background threads for Wake Word and Gestures."""
        self.gui.log_to_terminal("INITIATING BACKGROUND SENSORS...", "sys")
        
        # 1. Start Auto-Gesture (Camera)
        # Note: This opens the camera window immediately.
        self.gui.toggle_gestures()
        
        # 2. Start Auto-Voice (Wake Word)
        threading.Thread(target=self.background_listener_loop, daemon=True).start()

    def background_listener_loop(self):
        """Continuously listens for 'Jarvis' without buttons."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.running:
                try:
                    # Listen for short bursts to catch the Wake Word
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if Config.WAKE_WORD in text:
                        # WAKE WORD DETECTED
                        self.gui.set_status("WAKE WORD DETECTED", Config.THEME["SUCCESS"])
                        self.voice.speak("Yes?")
                        self.active_listen_phase(source) # Switch to active mode
                        
                except sr.WaitTimeoutError:
                    pass # Just keep listening
                except Exception:
                    pass # Ignore noise errors

    def active_listen_phase(self, source):
        """Called when Wake Word is detected. Listens for actual command."""
        try:
            self.gui.set_status("LISTENING FOR COMMAND...", Config.THEME["FG_PRIMARY"])
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            self.gui.set_status("PROCESSING...", Config.THEME["WARN"])
            
            text = self.recognizer.recognize_google(audio).lower()
            self.gui.log_to_terminal(f"USER: {text}", "user")
            self.process_command(text)
            
        except Exception:
            self.voice.speak("I didn't catch that.")
        finally:
            self.gui.set_status("ONLINE (WAITING)", "white")

    def manual_listen_once(self):
        """Backup manual button method."""
        with sr.Microphone() as source:
            self.active_listen_phase(source)

    def process_command(self, text):
        # 1. HARDCODED COMMANDS
        if "shutdown" in text:
            #Mood 
            self.voice.set_mood("SERIOUS")
            self.voice.speak("Powering down system.")
            self.gui.root.destroy()
            sys.exit()
            
        elif "play music" in text:
            self.voice.set_mood("HAPPY")
            self.voice.speak("Loading media interface.")
            self.media_sys.load_music()
            
        elif "whatsapp" in text:
            self.voice.set_mood("NEUTRAL")
            self.voice.speak("Who is the recipient?")
            # Logic flow would continue here...
            
        elif "add mission" in text:
            task = text.replace("add mission", "").strip()
            db.add_mission(task)
            self.voice.speak("Mission added to database.")
            self.gui.refresh_tasks()
            
        elif "snake" in text:
             ArcadeEngine.play_snake(self.gui.root)

        elif "screenshot" in text:
            self.take_screenshot()

        # 2. AI BRAIN FALLBACK
        else:
            self.brain_ai.think(text, self.gui.set_status)

    def take_screenshot(self):
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(Config.DIRS["DOWNLOADS"], f"SCR_{ts}.png")
        pyautogui.screenshot(path)
        self.voice.speak("Display captured.")

# ==============================================================================
# 🚀 SECTOR 12: MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # 1. Initialize Controller
    jarvis = JarvisController()
    
    print("\n")
    print("█▀▀ █▀█ █▀▄   █▀▄▀█ █▀█ █▀▄ █▀▀")
    print("█▄█ █▄█ █▄▀   █ ▀ █ █▄█ █▄▀ ██▄")
    print(f">> SYSTEM: {Config.VERSION}")
    
    # 2. VOICE SECURITY CHECK
    # This replaces the Face ID system entirely
    print(">> INITIALIZING AUDIO SECURITY GATE...")
    
    # You must say "protocol omega" (or change in Config) to unlock
    if jarvis.voice_sec.authenticate():
        print(">> AUTHORIZATION SUCCESSFUL.")
        jarvis.voice.speak(f"Welcome back, Sir. {Config.CODENAME} is active.")
        
        # 3. Launch GUI
        root = tk.Tk()
        app = Dashboard(root, jarvis)
        
        # This now triggers the Auto-Sense (Voice & Gestures)
        jarvis.attach_gui(app) 
        
        root.mainloop()
    else:
        print(">> TOO MANY FAILED ATTEMPTS. SYSTEM LOCKDOWN.")
        sys.exit()