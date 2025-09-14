# #################################
# TALOS - Advanced Text File Analyzer
# Input: .txt file
# Export: CSV/Excel
# - Word List with Occurrences
# - Noun List and Occurrences
# - Proper Name List (Person)
# - Proper Name List (Location)
# - Lemmatized Text Analysis
# - Lexical-Syntactic Pattern Extraction
# ---------------------------------
# Enhanced Version with Language Detection
# Stanza Integration for Ancient Greek
# Christophe Roche - Advanced Version
# #################################

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from collections import Counter
import pandas as pd
import threading
import os
from pathlib import Path
import re
import time
import queue

class TextAnalyzer:
    def __init__(self):
        self.nlp = None
        self.stanza_nlp = None  # For Ancient Greek
        self.nlp_loading = False
        self.detected_language = "Unknown"
        self.selected_file = None
        self.file_content = None
        self.custom_pattern = None
        self.analysis_queue = queue.Queue()
        self.setup_gui()
        
    def detect_language(self, text):
        """Improved language detection with better English recognition"""
        try:
            # Try to use langdetect library if available
            from langdetect import detect, DetectorFactory, detect_langs
            DetectorFactory.seed = 0  # For consistent results
            
            # Take a sample of the text for faster detection
            sample = text[:3000] if len(text) > 3000 else text
            
            # Get probability distribution of languages
            try:
                lang_probs = detect_langs(sample)
                # If English has decent probability, prefer it
                for lang_prob in lang_probs:
                    if lang_prob.lang == 'en' and lang_prob.prob > 0.3:
                        return "English"
                
                # Otherwise use the top detection
                detected = detect(sample)
            except:
                detected = 'en'  # Default to English if detection fails
            
            # Map language codes to full names
            lang_map = {
                'en': 'English', 'fr': 'French', 'es': 'Spanish', 'de': 'German',
                'it': 'Italian', 'pt': 'Portuguese', 'nl': 'Dutch', 'ru': 'Russian',
                'zh-cn': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic',
                'el': 'Modern Greek'
            }
            
            detected_lang = lang_map.get(detected, "English")  # Default to English
            
            # Additional check for Ancient Greek vs Modern Greek
            if detected_lang == "Modern Greek":
                text_lower = text.lower()
                # Enhanced Ancient Greek detection
                ancient_greek_indicators = [
                    # Polytonic marks
                    'ἀ', 'ἁ', 'ἂ', 'ἃ', 'ἄ', 'ἅ', 'ἆ', 'ἇ', 'ἐ', 'ἑ', 'ἒ', 'ἓ', 'ἔ', 'ἕ',
                    'ἠ', 'ἡ', 'ἢ', 'ἣ', 'ἤ', 'ἥ', 'ἦ', 'ἧ', 'ἰ', 'ἱ', 'ἲ', 'ἳ', 'ἴ', 'ἵ',
                    'ὀ', 'ὁ', 'ὂ', 'ὃ', 'ὄ', 'ὅ', 'ὐ', 'ὑ', 'ὒ', 'ὓ', 'ὔ', 'ὕ', 'ὖ', 'ὗ',
                    'ὠ', 'ὡ', 'ὢ', 'ὣ', 'ὤ', 'ὥ', 'ὦ', 'ὧ', 'ὰ', 'ὲ', 'ὴ', 'ὶ', 'ὸ', 'ὺ', 'ὼ',
                    'ᾀ', 'ᾁ', 'ᾂ', 'ᾃ', 'ᾄ', 'ᾅ', 'ᾆ', 'ᾇ', 'ᾐ', 'ᾑ', 'ᾒ', 'ᾓ', 'ᾔ', 'ᾕ',
                    'ᾖ', 'ᾗ', 'ᾠ', 'ᾡ', 'ᾢ', 'ᾣ', 'ᾤ', 'ᾥ', 'ᾦ', 'ᾧ', 'ᾰ', 'ᾱ', 'ᾲ', 'ᾳ',
                    'ᾴ', 'ᾶ', 'ᾷ', 'ῂ', 'ῃ', 'ῄ', 'ῆ', 'ῇ', 'ῐ', 'ῑ', 'ῒ', 'ΐ', 'ῖ', 'ῗ',
                    'ῠ', 'ῡ', 'ῢ', 'ΰ', 'ῤ', 'ῥ', 'ῦ', 'ῧ', 'ῲ', 'ῳ', 'ῴ', 'ῶ', 'ῷ',
                    # Ancient Greek specific words
                    'καὶ', 'τὸ', 'τίν', 'τοῦ', 'ἐν', 'τῆς', 'εἰς', 'τῶν', 'τὰς', 'ὃ', 'ἡ', 'τόн',
                    'αὐτὸν', 'αὐτοῦ', 'ἐστι', 'γὰρ', 'δὲ', 'οὐ', 'μὴ', 'ἀλλὰ', 'ἄν', 'ἔστι', 'ὅτι',
                    'ὡς', 'μετὰ', 'πρὸς', 'διὰ', 'παρὰ', 'ἀπὸ', 'ἐπὶ', 'ὑπὸ', 'περὶ', 'σὺν', 'ἄνευ',
                    'ἕνεκα', 'χάριν', 'ἕως', 'μέχρι', 'πρίν', 'ἐάν', 'ἵνα', 'ὅπως', 'ὅταν', 'ἐπεὶ'
                ]
                
                # Modern Greek indicators
                modern_greek_indicators = [
                    'και', 'το', 'της', 'του', 'τα', 'με', 'σε', 'για', 'από', 'που', 'θа', 'είναι',
                    'έχει', 'έχουν', 'ήταν', 'αυτό', 'αυτή', 'αυτά', 'αυτός', 'αυτήν', 'αυτούς'
                ]
                
                # Check for polytonic marks first (strong Ancient Greek indicator)
                has_polytonic = any(mark in text for mark in ['ἀ', 'ἁ', 'ἂ', 'ἃ', 'ἄ', 'ἅ', 'ἆ', 'ἇ', 'ὁ', 'ὃ'])
                
                # Count matches for each language
                ancient_count = sum(1 for word in ancient_greek_indicators if f' {word} ' in f' {text_lower} ')
                modern_count = sum(1 for word in modern_greek_indicators if f' {word} ' in f' {text_lower} ')
                
                # Determine which Greek variant
                if has_polytonic or ancient_count > modern_count:
                    return "Ancient Greek"
                else:
                    return "Modern Greek"
            
            return detected_lang
            
        except ImportError:
            # Enhanced fallback: Better English detection
            text_lower = text.lower()
            words = text_lower.split()
            total_words = len(words)
            
            if total_words == 0:
                return "English"
            
            # Enhanced English indicators with higher weight
            english_words = ['the', 'and', 'is', 'are', 'was', 'were', 'have', 'has', 'will', 'would', 
                           'this', 'that', 'with', 'from', 'they', 'been', 'their', 'said', 'each', 'which',
                           'she', 'do', 'how', 'if', 'up', 'out', 'many', 'time', 'very', 'when', 'much',
                           'can', 'said', 'there', 'use', 'your', 'way', 'about', 'could', 'just']
            english_count = sum(1 for word in english_words if f' {word} ' in f' {text_lower} ')
            
            # French indicators
            french_words = ['le', 'la', 'les', 'de', 'du', 'des', 'et', 'est', 'sont', 'avec', 'dans', 'pour', 'sur', 'ce', 'qui', 'une', 'tout', 'nous', 'vous', 'ils']
            french_count = sum(1 for word in french_words if f' {word} ' in f' {text_lower} ')
            
            # Spanish indicators
            spanish_words = ['el', 'la', 'los', 'las', 'de', 'del', 'y', 'es', 'son', 'con', 'en', 'por', 'para', 'que', 'un', 'una', 'todo', 'pero', 'más', 'como']
            spanish_count = sum(1 for word in spanish_words if f' {word} ' in f' {text_lower} ')
            
            # German indicators
            german_words = ['der', 'die', 'das', 'und', 'ist', 'sind', 'mit', 'von', 'zu', 'haben', 'auf', 'für', 'ein', 'eine', 'nicht', 'sich', 'auch', 'werden', 'bei', 'noch']
            german_count = sum(1 for word in german_words if f' {word} ' in f' {text_lower} ')
            
            # Italian indicators
            italian_words = ['il', 'la', 'le', 'di', 'e', 'che', 'un', 'una', 'con', 'per', 'in', 'da', 'del', 'della', 'dei', 'delle', 'sono', 'è', 'hanno', 'sia']
            italian_count = sum(1 for word in italian_words if f' {word} ' in f' {text_lower} ')
            
            # Modern Greek indicators  
            modern_greek_words = ['το', 'η', 'και', 'του', 'της', 'στην', 'στον', 'με', 'για', 'από', 'όλα', 'αυτό', 'που', 'θα', 'είναι', 'έχει', 'μια', 'στα', 'ένα', 'όμως']
            modern_greek_count = sum(1 for word in modern_greek_words if f' {word} ' in f' {text_lower} ')
            
            # Ancient Greek indicators
            ancient_greek_words = ['καὶ', 'τὸ', 'τίν', 'τοῦ', 'ἐν', 'τῆς', 'εἰς', 'τῶν', 'τὰς', 'ὃ', 'ἡ', 'τόн',
                                 'αὐτὸν', 'αὐτοῦ', 'ἐστι', 'γὰρ', 'δὲ', 'οὐ', 'μὴ', 'ἀλλὰ', 'ἄν', 'ἔστι', 'ὅτι',
                                 'ὡς', 'μετὰ', 'πρὸς', 'διὰ', 'παρὰ', 'ἀπὸ', 'ἐπὶ', 'ὑπὸ', 'περὶ', 'σὺν', 'ἄνευ',
                                 'ἕνεκα', 'χάριν', 'ἕως', 'μέχρι', 'πρίν', 'ἐάν', 'ἵνα', 'ὅπως', 'ὅταν', 'ἐπεὶ']
            ancient_greek_count = sum(1 for word in ancient_greek_words if f' {word} ' in f' {text_lower} ')
            
            # Check for polytonic marks (strong Ancient Greek indicator)
            has_polytonic = any(mark in text for mark in ['ἀ', 'ἁ', 'ἂ', 'ἃ', 'ἄ', 'ἅ', 'ἆ', 'ἇ', 'ὁ', 'ὃ'])
            
            # Calculate percentages
            english_pct = (english_count / total_words) * 100
            french_pct = (french_count / total_words) * 100
            spanish_pct = (spanish_count / total_words) * 100
            german_pct = (german_count / total_words) * 100
            italian_pct = (italian_count / total_words) * 100
            modern_greek_pct = (modern_greek_count / total_words) * 100
            ancient_greek_pct = (ancient_greek_count / total_words) * 100
            
            # Ancient Greek has priority if detected
            if has_polytonic or ancient_greek_pct > 1.0:  # Even small percentage indicates Ancient Greek
                return "Ancient Greek"
            
            # English bias: if English percentage is decent, prefer it
            if english_pct >= 2.0 or english_count >= 5:
                return "English"
            
            max_pct = max(english_pct, french_pct, spanish_pct, german_pct, italian_pct, modern_greek_pct)
            
            if max_pct == 0:
                return "English"  # Default to English
            elif max_pct == modern_greek_pct:
                return "Modern Greek"
            elif max_pct == italian_pct:
                return "Italian"
            elif max_pct == french_pct:
                return "French"
            elif max_pct == spanish_pct:
                return "Spanish"
            elif max_pct == german_pct:
                return "German"
            else:
                return "English"
                
        except Exception:
            return "English"  # Always default to English
        
    def lazy_load_nlp(self, language="en"):
        """Lazy loading of NLP models with Stanza for Ancient Greek"""
        if self.nlp_loading:
            return False
            
        # If it's Ancient Greek and we haven't loaded Stanza yet
        if language == "Ancient Greek" and self.stanza_nlp is None:
            self.nlp_loading = True
            try:
                import stanza
                self.update_status("Loading Ancient Greek model (Stanza)...", self.colors['accent'])
                self.stanza_nlp = stanza.Pipeline("grc")
                self.nlp_loading = False
                self.update_status("Ancient Greek model loaded", self.colors['success'])
                return True
            except Exception as e:
                messagebox.showerror("Stanza Error", 
                    "Stanza model for Ancient Greek is not available.\n"
                    "Run: stanza.download('grc')\n"
                    f"Error: {str(e)}")
                self.nlp_loading = False
                return False
        
        # For all other languages, use spaCy
        if language != "Ancient Greek" and self.nlp is None:
            self.nlp_loading = True
            try:
                import spacy
                
                # Language model mapping
                model_map = {
                    "English": "en_core_web_sm",
                    "French": "fr_core_news_sm",
                    "Spanish": "es_core_news_sm",
                    "German": "de_core_news_sm",
                    "Italian": "it_core_news_sm",
                    "Portuguese": "pt_core_news_sm",
                    "Dutch": "nl_core_news_sm",
                    "Modern Greek": "el_core_news_sm"
                }
                
                model_name = model_map.get(language, "en_core_web_sm")
                
                try:
                    self.update_status(f"Loading {language} model (spaCy)...", self.colors['accent'])
                    self.nlp = spacy.load(model_name)
                    self.update_status(f"{language} model loaded", self.colors['success'])
                except OSError:
                    # Fallback to English if specific language model not available
                    self.update_status("Falling back to English model...", self.colors['accent'])
                    self.nlp = spacy.load("en_core_web_sm")
                    messagebox.showwarning("Model Warning", 
                        f"Language model for {language} not found. Using English model.\n"
                        f"For better results, install: python -m spacy download {model_name}")
                
                self.nlp_loading = False
                return True
            except Exception as e:
                messagebox.showerror("NLP Error", 
                    "spaCy model 'en_core_web_sm' is not installed.\n"
                    "Run: python -m spacy download en_core_web_sm\n"
                    f"Error: {str(e)}")
                self.nlp_loading = False
                return False
        
        # Return True if we already have the right model loaded
        return (language == "Ancient Greek" and self.stanza_nlp is not None) or \
               (language != "Ancient Greek" and self.nlp is not None)

    def get_nlp_doc(self, text, language):
        """Get processed document using appropriate NLP library"""
        if language == "Ancient Greek" and self.stanza_nlp is not None:
            # For Stanza, return the processed document directly
            return self.stanza_nlp(text)
        elif language != "Ancient Greek" and self.nlp is not None:
            # For spaCy, normal processing
            return self.nlp(text)
        else:
            return None

    def setup_gui(self):
        """Modern GUI setup with English interface"""
        self.window = tk.Tk()
        self.window.title("TALOS - Advanced Text File Analyzer")
        
        # Modern dark theme
        self.colors = {
            'bg_primary': '#1e1e2e',      # Primary dark background
            'bg_secondary': '#2a2a3e',     # Secondary background
            'accent': '#3b82f6',           # Modern blue
            'accent_hover': '#2563eb',     # Blue hover
            'text_primary': '#ffffff',     # Primary text
            'text_secondary': '#a1a1aa',   # Secondary text
            'success': '#22c55e',          # Success green
            'border': '#374151',           # Borders
            'warning': '#f59e0b',          # Warning orange
            'error': '#ef4444'             # Error red
        }
        
        self.setup_window_style()
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        
        # Window configuration
        self.center_window(850, 900)
        
    def setup_window_style(self):
        """Window style configuration"""
        self.window.configure(bg=self.colors['bg_primary'])
        
        # ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom style configuration
        self.style.configure('Modern.TButton',
                           background=self.colors['accent'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(20, 10))
        
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['accent_hover']),
                                ('pressed', '#1d4ed8')])
        
    def create_header(self):
        """Header creation with logo and title"""
        header_frame = tk.Frame(self.window, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Main title with modern style
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_frame.pack(expand=True)
        
        tk.Label(title_frame, 
                text="TALOS AI4SSH",
                font=('Segoe UI', 28, 'bold'),
                fg=self.colors['accent'],
                bg=self.colors['bg_primary']).pack()
                
        tk.Label(title_frame,
                text="Advanced Intelligent Text File Analyzer",
                font=('Segoe UI', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_primary']).pack()
        
    def create_main_content(self):
        """Main content creation"""
        main_frame = tk.Frame(self.window, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File selection section (FIRST)
        self.create_file_selection(main_frame)
        
        # Action buttons section
        self.create_action_buttons(main_frame)
        
        # Languages support info section
        self.create_language_info(main_frame)
        
        # Results area
        self.create_results_area(main_frame)
        
    def create_file_selection(self, parent):
        """File selection section - NOW FIRST"""
        file_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=1)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title and button in same row
        header_frame = tk.Frame(file_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(header_frame,
                text="📁 Step 1: Select Your Text File",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        # Select file button
        select_btn = tk.Button(header_frame,
                              text="📂 Browse File",
                              command=self.select_file,
                              bg=self.colors['accent'],
                              fg='white',
                              font=('Segoe UI', 10, 'bold'),
                              relief=tk.FLAT,
                              bd=0,
                              padx=15,
                              pady=8,
                              cursor='hand2')
        select_btn.pack(side=tk.RIGHT)
        
        # Hover effects for button
        select_btn.bind("<Enter>", lambda e: select_btn.config(bg=self.colors['accent_hover']))
        select_btn.bind("<Leave>", lambda e: select_btn.config(bg=self.colors['accent']))
        
        # File display area
        self.file_name_label = tk.Label(file_frame,
                                      text="❌ No file selected yet",
                                      font=('Segoe UI', 10),
                                      fg=self.colors['text_secondary'],
                                      bg=self.colors['bg_secondary'],
                                      wraplength=800,
                                      justify='left')
        self.file_name_label.pack(anchor='w', padx=15, pady=(0, 15))

    def create_action_buttons(self, parent):
        """Modern action buttons creation - NO FILE SELECTION"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=1)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Section title
        tk.Label(button_frame,
                text="📊 Step 2: Choose Your Analysis Type",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(pady=(15, 10))
        
        # Button container
        buttons_container = tk.Frame(button_frame, bg=self.colors['bg_secondary'])
        buttons_container.pack(pady=(0, 15))
        
        # Button configuration with text icons
        buttons_config = [
            ("📝 Word Analysis", lambda: self.handle_analysis(1), "Complete word frequency analysis"),
            ("🏷️ Noun Analysis", lambda: self.handle_analysis(2), "Common noun extraction"),
            ("👥 Person Names", lambda: self.handle_analysis(3), "Person name recognition"),
            ("🌍 Location Names", lambda: self.handle_analysis(4), "Location identification"),
            ("🔤 Lemmatization", lambda: self.handle_analysis(5), "Lemmatized word analysis"),
            ("🎯 Pattern Extraction", lambda: self.show_pattern_selector(), "Custom lexical-syntactic patterns")
        ]
        
        for i, (text, command, tooltip) in enumerate(buttons_config):
            btn = tk.Button(buttons_container,
                          text=text,
                          command=command,
                          bg=self.colors['accent'],
                          fg='white',
                          font=('Segoe UI', 10, 'bold'),
                          relief=tk.FLAT,
                          bd=0,
                          padx=15,
                          pady=10,
                          cursor='hand2')
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['accent_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['accent']))
            
            # Grid positioning 3x2
            row, col = i // 3, i % 3
            btn.grid(row=row, column=col, padx=6, pady=5, sticky='ew')
            
        # Column weight configuration
        for i in range(3):
            buttons_container.grid_columnconfigure(i, weight=1)
    
    def create_language_info(self, parent):
        """Language support information section"""
        lang_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=1)
        lang_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(lang_frame,
                text="🌍 Supported Languages",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor='w', padx=15, pady=(10, 5))
        
        # Language list with flags - more compact display
        languages = ["   🇺🇸 English", "🇬🇷 Modern Greek", "🏛️ Ancient Greek (models auto-installed when needed)"]
        
        # Create compact language display
        lang_text = "  • " + "   • ".join(languages)
        
        lang_display = tk.Label(lang_frame,
                               text=lang_text,
                               font=('Segoe UI', 9),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['bg_secondary'],
                               wraplength=850,
                               justify='left')
        lang_display.pack(anchor='w', padx=15, pady=(0, 5))
        
        # Installation note
        note_label = tk.Label(lang_frame,
                             text="💡 spaCy for modern languages, Stanza for Ancient Greek (models auto-installed when needed)",
                             font=('Segoe UI', 8),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg_secondary'],
                             wraplength=750)
        note_label.pack(anchor='w', padx=15, pady=(0, 10))
        
    def create_results_area(self, parent):
        """Results display area with modern style"""
        results_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=1)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results area header with progress bar
        header = tk.Frame(results_frame, bg=self.colors['bg_secondary'])
        header.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        # Title
        self.results_title = tk.Label(header,
                text="📊 Analysis Results",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary'])
        self.results_title.pack(side=tk.LEFT)
        
        # Progress bar for analysis
        self.results_progress = ttk.Progressbar(header, mode='determinate', length=200)
        self.results_progress.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Progress label
        self.progress_label = tk.Label(header,
                                     text="0%",
                                     font=('Segoe UI', 9),
                                     fg=self.colors['text_secondary'],
                                     bg=self.colors['bg_secondary'],
                                     width=5)
        self.progress_label.pack(side=tk.RIGHT)
        
        # Text area with modern style
        text_frame = tk.Frame(results_frame, bg=self.colors['border'], bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.text_area = ScrolledText(text_frame,
                                    wrap=tk.WORD,
                                    font=('Consolas', 11),
                                    bg='#ffffff',
                                    fg='#1f2937',
                                    selectbackground=self.colors['accent'],
                                    selectforeground='white',
                                    borderwidth=0,
                                    padx=15,
                                    pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        self.text_area.insert(tk.END, 
                             "🚀 Welcome to TALOS Advanced Text Analyzer!\n\n"
                             "📁 Step 1: Select a text file using the 'Browse File' button above\n"
                             "📊 Step 2: Choose an analysis type\n"
                             "💾 Step 3: Export results to Excel\n\n"
                             "💡 Tips:\n"
                             "• 'Person Names' and 'Location Names' use AI processing\n"
                             "• 'Lemmatization' provides base word forms\n"
                             "• 'Pattern Extraction' finds linguistic patterns like [adj][noun]\n"
                             "• Language is automatically detected for each file\n"
                             "• First AI analysis may take a few seconds to load\n"
                             "• Ancient Greek uses Stanza NLP, other languages use spaCy\n"
                             "• Supported formats: .txt files\n\n"
                             "📂 Select a file to get started!")
        
        # Make text area read-only initially
        self.text_area.config(state=tk.DISABLED)
    
    def create_status_bar(self):
        """Modern status bar"""
        self.status_frame = tk.Frame(self.window, bg=self.colors['bg_secondary'], height=30)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame,
                                   text="Ready - Please select a file",
                                   font=('Segoe UI', 9),
                                   fg=self.colors['text_secondary'],
                                   bg=self.colors['bg_secondary'])
        self.status_label.pack(side=tk.LEFT, padx=15, pady=6)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.status_frame, mode='indeterminate', length=100)
        self.progress.pack(side=tk.RIGHT, padx=15, pady=6)
        
    def update_status(self, message, color=None):
        """Update status bar"""
        if color is None:
            color = self.colors['text_secondary']
        self.status_label.config(text=message, fg=color)
        self.window.update()
        
    def update_results_progress(self, value, max_value=100):
        """Update the progress bar in the results area"""
        if value > max_value:
            value = max_value
            
        percentage = int((value / max_value) * 100)
        self.results_progress['value'] = percentage
        self.progress_label.config(text=f"{percentage}%")
        self.window.update()
        
    def reset_results_progress(self):
        """Reset the progress bar in the results area"""
        self.results_progress['value'] = 0
        self.progress_label.config(text="0%")
        
    def start_progress(self):
        """Start indeterminate progress bar"""
        self.progress.start(10)
        
    def stop_progress(self):
        """Stop progress bar"""
        self.progress.stop()
        
    def center_window(self, width, height):
        """Center window on screen"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
    def select_file(self):
        """File selection with validation and content loading"""
        file = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Select a text file"
        )
        
        if file:
            # File validation
            if not os.path.exists(file):
                messagebox.showerror("Error", "The selected file does not exist.")
                return False
                
            file_size = os.path.getsize(file)
            if file_size > 50 * 1024 * 1024:  # 50MB limit
                if not messagebox.askyesno("Large File", 
                                         f"File size is {file_size//1024//1024}MB. "
                                         "Processing may be slow. Continue?"):
                    return False
            
            # Load file content and detect language
            try:
                self.update_status("Loading file and detecting language...", self.colors['accent'])
                self.start_progress()
                
                with open(file, 'r', encoding='utf-8') as f:
                    self.file_content = f.read()
                    sample_text = self.file_content[:5000]  # First 5000 chars for detection
                    
                self.detected_language = self.detect_language(sample_text)
                self.selected_file = file
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {str(e)}")
                self.stop_progress()
                return False
            
            # Display selected file with language
            file_path = Path(file)
            language_flag = self.get_language_flag(self.detected_language)
            
            # File info display
            file_size_mb = file_size / (1024 * 1024)
            word_count = len(self.file_content.split())
            
            display_text = (
                f"✅ {file_path.name}\n"
                f"   📂 {file_path.parent}\n"
                f"   🌍 Language: {language_flag} {self.detected_language}\n"
                f"   📄 Size: {file_size_mb:.1f} MB | Words: {word_count:,}"
            )
            
            self.file_name_label.config(text=display_text, fg=self.colors['success'])
            self.update_status(f"File loaded: {file_path.name} ({self.detected_language})", self.colors['success'])
            self.stop_progress()
            
            # Display beginning of text in results area
            self.display_file_preview()
            
            return True
        return False
    
    def get_language_flag(self, language):
        """Get flag emoji for language"""
        flags = {
            'English': '🇺🇸', 'French': '🇫🇷', 'Spanish': '🇪🇸', 'German': '🇩🇪',
            'Italian': '🇮🇹', 'Portuguese': '🇵🇹', 'Dutch': '🇳🇱', 'Russian': '🇷🇺',
            'Chinese': '🇨🇳', 'Japanese': '🇯🇵', 'Korean': '🇰🇷', 'Arabic': '🇸🇦',
            'Modern Greek': '🇬🇷', 'Ancient Greek': '🏛️'
        }
        return flags.get(language, '🏳️')
        
    def handle_analysis(self, option):
        """Main handler for analyses - NO FILE SELECTION"""
        # Check if file is loaded
        if not self.selected_file or not self.file_content:
            messagebox.showwarning("No File Selected", 
                                 "⚠️ Please select a text file first using the 'Browse File' button!")
            return
            
        # Analysis configuration
        analysis_config = {
            1: ("words", "📝 Word Analysis", self.analyze_words),
            2: ("nouns", "🏷️ Noun Analysis", self.analyze_nouns),
            3: ("persons", "👥 Person Analysis", lambda: self.analyze_entities("PERSON")),
            4: ("locations", "🌍 Location Analysis", lambda: self.analyze_entities("GPE")),
            5: ("lemmas", "🔤 Lemmatization Analysis", self.analyze_lemmas),
            6: ("patterns", "🎯 Pattern Extraction", self.analyze_patterns)
        }
        
        if option not in analysis_config:
            return
            
        export_name, title, analyze_func = analysis_config[option]
        
        # Progress display
        self.update_status(f"Analysis in progress...", self.colors['accent'])
        self.start_progress()
        self.reset_results_progress()
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"{title}\n{'='*50}\n\n⏳ Processing...")
        self.text_area.config(state=tk.DISABLED)
        self.window.update()
        
        # Background analysis with timeout check
        def run_analysis():
            try:
                result = analyze_func()
                if result:
                    self.window.after(0, lambda: self.display_results(title, result, export_name))
                else:
                    self.window.after(0, lambda: self.update_status("Analysis completed (no results)", self.colors['warning']))
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("Error", f"Analysis error: {str(e)}"))
            finally:
                self.window.after(0, self.stop_progress)
                self.window.after(0, lambda: self.update_results_progress(100))
                
        # Start analysis thread with timeout monitor
        analysis_thread = threading.Thread(target=run_analysis, daemon=True)
        analysis_thread.start()
        
        # Monitor thread completion
        self.monitor_analysis_thread(analysis_thread, title)

    def monitor_analysis_thread(self, thread, title, timeout=300):
        """Monitor analysis thread with timeout"""
        start_time = time.time()
        
        def check_thread():
            if thread.is_alive():
                elapsed = time.time() - start_time
                if elapsed < timeout:
                    # Update progress based on elapsed time
                    progress = min(90, int((elapsed / timeout) * 90))  # Cap at 90% until completion
                    self.update_results_progress(progress)
                    
                    # Thread still running, check again in 500ms
                    self.window.after(500, check_thread)
                else:
                    # Thread timeout
                    self.window.after(0, lambda: self.update_status(f"{title} timed out after {timeout} seconds", self.colors['error']))
                    self.window.after(0, self.stop_progress)
            else:
                # Thread completed
                self.window.after(100, lambda: self.update_status(f"{title} completed", self.colors['success']))
        
        check_thread()

    def analyze_words(self):
        """Enhanced word analysis"""
        try:
            content = self.file_content.lower()
            # Enhanced cleaning
            words = re.findall(r'\b[a-zA-ZÀ-ÿα-ωΑ-Ωά-ώ]+\b', content)
            words = [word for word in words if len(word) > 2]  # Filter short words
            
            return Counter(words)
        except Exception as e:
            messagebox.showerror("Error", f"Word analysis error: {e}")
            return {}

    def analyze_patterns(self):
        """Default pattern extraction for backward compatibility"""
        if not self.lazy_load_nlp(self.detected_language):
            return {}
            
        try:
            doc = self.get_nlp_doc(self.file_content, self.detected_language)
            if doc is None:
                return {}
                
            patterns = []
            
            # Define common pattern templates (up to 5 positions)
            pattern_templates = [
                # 2-word patterns
                ["ADJ", "NOUN"],           # beautiful house
                ["NOUN", "NOUN"],          # computer science
                ["VERB", "NOUN"],          # read book
                
                # 3-word patterns
                ["ADJ", "ADJ", "NOUN"],    # big red car
                ["NOUN", "ADP", "NOUN"],   # book of poems
                ["DET", "ADJ", "NOUN"],    # the blue sky
                
                # 4-word patterns
                ["DET", 'ADJ', 'ADJ', 'NOUN'],      # the big red car
                ['NOUN', 'ADP', 'DET', 'NOUN'],     # book of the author
            ]
            
            # Extract patterns from text
            if self.detected_language == "Ancient Greek":
                # For Stanza, adapt token access logic
                tokens = [word for sent in doc.sentences for word in sent.words if word.text.isalpha()]
            else:
                # For spaCy, standard logic
                tokens = [token for token in doc if not token.is_space and token.is_alpha]
            
            total_tokens = len(tokens)
            
            for template_idx, template in enumerate(pattern_templates):
                pattern_length = len(template)
                
                for i in range(len(tokens) - pattern_length + 1):
                    token_sequence = tokens[i:i + pattern_length]
                    
                    if self.detected_language == "Ancient Greek":
                        # For Stanza
                        pos_sequence = [token.upos for token in token_sequence]
                        words = [token.text.lower() for token in token_sequence]
                    else:
                        # For spaCy
                        pos_sequence = [token.pos_ for token in token_sequence]
                        words = [token.text.lower() for token in token_sequence]
                    
                    if pos_sequence == template:
                        # Create pattern string
                        pos_pattern = "_".join(template)
                        word_pattern = " ".join(words)
                        
                        # Store as "POS_PATTERN: word pattern"
                        pattern_string = f"[{pos_pattern}]: {word_pattern}"
                        patterns.append(pattern_string)
                    
                    # Update progress periodically
                    if i % 100 == 0:
                        progress = ((template_idx * total_tokens) + i) / (len(pattern_templates) * total_tokens) * 100
                        self.window.after(0, lambda p=progress: self.update_results_progress(p))
            
            return Counter(patterns)
            
        except Exception as e:
            messagebox.showerror("Error", f"Pattern extraction error: {e}")
            return {}

    def analyze_nouns(self):
        """Noun analysis with lazy loading"""
        if not self.lazy_load_nlp(self.detected_language):
            return {}
            
        try:
            doc = self.get_nlp_doc(self.file_content, self.detected_language)
            if doc is None:
                return {}
            
            nouns = []
            
            if self.detected_language == "Ancient Greek":
                # For Stanza
                total_sents = len(doc.sentences)
                for sent_idx, sent in enumerate(doc.sentences):
                    for word in sent.words:
                        if word.upos == "NOUN" and len(word.text) > 2 and word.text.isalpha():
                            nouns.append(word.text.lower())
                    
                    # Update progress
                    progress = (sent_idx / total_sents) * 100
                    self.window.after(0, lambda p=progress: self.update_results_progress(p))
            else:
                # For spaCy
                nouns = [token.text.lower() for token in doc 
                        if token.pos_ == "NOUN" and len(token.text) > 2 and token.is_alpha]
            
            return Counter(nouns)
        except Exception as e:
            messagebox.showerror("Error", f"Noun analysis error: {e}")
            return {}

    def analyze_entities(self, entity_type):
        """Optimized named entity analysis with progress feedback"""
        if not self.lazy_load_nlp(self.detected_language):
            return {}
            
        try:
            doc = self.get_nlp_doc(self.file_content, self.detected_language)
            if doc is None:
                return {}
            
            entities = []
            processed_chars = 0
            total_chars = len(self.file_content)
            
            def update_progress():
                progress = min(100, int(processed_chars / total_chars * 100))
                self.text_area.config(state=tk.NORMAL)
                self.text_area.delete("end-2l", "end-1l")
                self.text_area.insert(tk.END, f"\n⏳ Processing... {progress}%")
                self.text_area.see(tk.END)
                self.text_area.config(state=tk.DISABLED)
                self.update_results_progress(progress)
                self.window.update()
            
            start_time = time.time()
            
            if self.detected_language == "Ancient Greek":
                # Ancient Greek processing with stanza
                total_sents = len(doc.sentences)
                for sent_idx, sent in enumerate(doc.sentences):
                    for word in sent.words:
                        if (word.text[0].isupper() and len(word.text) > 2 and 
                            word.upos in ["PROPN", "NOUN"]):
                            entities.append(word.text)
                            
                    processed_chars += len(sent.text)
                    
                    # Update progress
                    progress = (sent_idx / total_sents) * 100
                    self.window.after(0, lambda p=progress: self.update_results_progress(p))
            else:
                # Modern language processing with spaCy
                total_ents = len(doc.ents)
                for i, ent in enumerate(doc.ents):
                    if ent.label_ == entity_type:
                        entities.append(ent.text)
                    
                    processed_chars = ent.end_char
                    
                    # Update progress periodically
                    if i % 10 == 0:
                        progress = (i / total_ents) * 100
                        self.window.after(0, lambda p=progress: self.update_results_progress(p))
            
            # Final update to show completion
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete("end-2l", "end-1l")
            self.text_area.insert(tk.END, f"\n⏳ Processing... 100% ({(time.time()-start_time):.1f}s)")
            self.text_area.see(tk.END)
            self.text_area.config(state=tk.DISABLED)
            self.update_results_progress(100)
            self.window.update()
            
            return Counter(entities)
            
        except Exception as e:
            messagebox.showerror("Error", f"Entity analysis error: {e}")
            return {}

    def analyze_lemmas(self):
        """Lemmatization analysis"""
        if not self.lazy_load_nlp(self.detected_language):
            return {}
            
        try:
            doc = self.get_nlp_doc(self.file_content, self.detected_language)
            if doc is None:
                return {}
            
            lemmas = []
            
            if self.detected_language == "Ancient Greek":
                # For Stanza
                total_sents = len(doc.sentences)
                for sent_idx, sent in enumerate(doc.sentences):
                    for word in sent.words:
                        if (word.text.isalpha() and len(word.text) > 2 and 
                            word.lemma and word.lemma.lower() != word.text.lower()):
                            lemmas.append(word.lemma.lower())
                    
                    # Update progress
                    progress = (sent_idx / total_sents) * 100
                    self.window.after(0, lambda p=progress: self.update_results_progress(p))
            else:
                # For spaCy
                lemmas = [token.lemma_.lower() for token in doc 
                         if token.is_alpha and len(token.text) > 2 and not token.is_stop]
            
            return Counter(lemmas)
        except Exception as e:
            messagebox.showerror("Error", f"Lemmatization error: {e}")
            return {}

    def show_pattern_selector(self):
        """Show pattern selection dialog"""
        # Check if file is loaded first
        if not self.selected_file or not self.file_content:
            messagebox.showwarning("No File Selected", 
                                 "⚠️ Please select a text file first using the 'Browse File' button!")
            return
            
        pattern_window = tk.Toplevel(self.window)
        pattern_window.title("🎯 Custom Pattern Builder")
        pattern_window.geometry("500x700")
        pattern_window.configure(bg=self.colors['bg_primary'])
        pattern_window.grab_set()  # Make it modal
        
        # Center the window
        pattern_window.transient(self.window)
        
        # Title
        title_label = tk.Label(pattern_window, 
                              text="🎯 Build Your Custom Pattern",
                              font=('Segoe UI', 16, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_primary'])
        title_label.pack(pady=(20, 10))
        
        # Instructions
        instructions = tk.Label(pattern_window,
                               text="Select which positions to fill (1-5) and choose POS tags:",
                               font=('Segoe UI', 10),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['bg_primary'])
        instructions.pack(pady=(0, 20))
        
        # Main frame
        main_frame = tk.Frame(pattern_window, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Pattern builder frame
        builder_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'])
        builder_frame.pack(pady=20, padx=20)
        
        # Available POS tags
        pos_tags = [
            "ADJ",    # Adjective
            "NOUN",   # Noun
            "VERB",   # Verb
            "DET",    # Determiner (the, a, an)
            "ADP",    # Adposition (preposition)
            "ADV",    # Adverb
            "PRON",   # Pronoun
            "NUM",    # Number
            "CONJ",   # Conjunction
            "PART",   # Particle
            "*"       # Any POS (wildcard)
        ]
        
        # Pattern positions (5 positions)
        self.pattern_vars = []
        self.pattern_enabled = []
        
        tk.Label(builder_frame, 
                text="Pattern Positions:",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        for i in range(5):
            # Position frame
            pos_frame = tk.Frame(builder_frame, bg=self.colors['bg_secondary'])
            pos_frame.grid(row=i+1, column=0, columnspan=3, sticky='ew', pady=5, padx=10)
            
            # Enable checkbox
            enabled_var = tk.BooleanVar()
            self.pattern_enabled.append(enabled_var)
            
            checkbox = tk.Checkbutton(pos_frame, 
                                    text=f"Position {i+1}:",
                                    variable=enabled_var,
                                    font=('Segoe UI', 10, 'bold'),
                                    fg=self.colors['text_primary'],
                                    bg=self.colors['bg_secondary'],
                                    selectcolor=self.colors['bg_primary'])
            checkbox.pack(side=tk.LEFT, padx=(0, 10))
            
            # POS dropdown
            pos_var = tk.StringVar(value="ADJ")
            self.pattern_vars.append(pos_var)
            
            pos_combo = ttk.Combobox(pos_frame, 
                                   textvariable=pos_var,
                                   values=pos_tags,
                                   state='readonly',
                                   width=8,
                                   font=('Segoe UI', 9))
            pos_combo.pack(side=tk.LEFT, padx=(0, 10))
            
            # POS description
            descriptions = {
                "ADJ": "Adjective (big, beautiful)",
                "NOUN": "Noun (house, car)",
                "VERB": "Verb (run, eat)",
                "DET": "Determiner (the, a, an)",
                "ADP": "Preposition (of, in, on)",
                "ADV": "Adverb (quickly, very)",
                "PRON": "Pronoun (he, she, it)",
                "NUM": "Number (one, first)",
                "CONJ": "Conjunction (and, or)",
                "PART": "Particle (to, not)",
                "*": "Any word type"
            }
            
            desc_label = tk.Label(pos_frame,
                                 text=descriptions.get(pos_var.get(), ""),
                                 font=('Segoe UI', 8),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_secondary'])
            desc_label.pack(side=tk.LEFT)
            
            # Update description when POS changes
            def update_desc(event, label=desc_label, var=pos_var):
                label.config(text=descriptions.get(var.get(), ""))
            
            pos_combo.bind('<<ComboboxSelected>>', update_desc)
        
        # Example patterns section
        example_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'])
        example_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(example_frame,
                text="💡 Example Patterns:",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor='w')
        
        examples = [
            "ADJ + NOUN → 'beautiful house'",
            "DET + ADJ + NOUN → 'the red car'", 
            "NOUN + ADP + NOUN → 'cup of coffee'",
            "ADJ + ADJ + NOUN → 'big red balloon'",
            "VERB + DET + NOUN → 'read the book'"
        ]
        
        for example in examples:
            tk.Label(example_frame,
                    text=f"  • {example}",
                    font=('Segoe UI', 9),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['bg_secondary']).pack(anchor='w')
        
        # Buttons frame
        button_frame = tk.Frame(pattern_window, bg=self.colors['bg_primary'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        def extract_custom_pattern():
            # Get selected pattern
            selected_pattern = []
            for i, (enabled, pos_var) in enumerate(zip(self.pattern_enabled, self.pattern_vars)):
                if enabled.get():
                    selected_pattern.append(pos_var.get())
            
            if not selected_pattern:
                messagebox.showwarning("No Pattern", "Please select at least one position!")
                return
            
            if len(selected_pattern) > 5:
                messagebox.showwarning("Pattern Too Long", "Maximum 5 positions allowed!")
                return
            
            # Close dialog and start analysis
            pattern_window.destroy()
            self.custom_pattern = selected_pattern
            
            # Start analysis (no file selection needed)
            self.update_status("Extracting custom patterns...", self.colors['accent'])
            self.start_progress()
            self.reset_results_progress()
            self.text_area.config(state=tk.NORMAL)
            pattern_str = "_".join(selected_pattern)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"🎯 Custom Pattern Extraction [{pattern_str}]\n{'='*60}\n\n⏳ Processing...")
            self.text_area.config(state=tk.DISABLED)
            self.window.update()
            
            def run_custom_analysis():
                try:
                    result = self.analyze_custom_patterns(selected_pattern)
                    if result:
                        title = f"🎯 Custom Pattern [{pattern_str}]"
                        self.window.after(0, lambda: self.display_results(title, result, f"pattern_{pattern_str}"))
                    else:
                        self.window.after(0, lambda: self.update_status("No patterns found", self.colors['warning']))
                except Exception as e:
                    self.window.after(0, lambda: messagebox.showerror("Error", f"Pattern extraction error: {str(e)}"))
                finally:
                    self.window.after(0, self.stop_progress)
                    self.window.after(0, lambda: self.update_results_progress(100))
                    
            threading.Thread(target=run_custom_analysis, daemon=True).start()
        
        def cancel_dialog():
            pattern_window.destroy()
        
        # Extract button
        extract_btn = tk.Button(button_frame,
                               text="🎯 Extract Pattern",
                               command=extract_custom_pattern,
                               bg=self.colors['accent'],
                               fg='white',
                               font=('Segoe UI', 11, 'bold'),
                               relief=tk.FLAT,
                               bd=0,
                               padx=20,
                               pady=10)
        extract_btn.pack(side=tk.LEFT, padx=(50, 10))
        
        # Cancel button  
        cancel_btn = tk.Button(button_frame,
                              text="❌ Cancel",
                              command=cancel_dialog,
                              bg=self.colors['text_secondary'],
                              fg='white',
                              font=('Segoe UI', 11),
                              relief=tk.FLAT,
                              bd=0,
                              padx=20,
                              pady=10)
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 50))
        
    def analyze_custom_patterns(self, pattern_template):
        """Extract custom lexical-syntactic patterns"""
        if not self.lazy_load_nlp(self.detected_language):
            return {}
            
        try:
            doc = self.get_nlp_doc(self.file_content, self.detected_language)
            if doc is None:
                return {}
                
            patterns = []
            
            # Extract patterns from text
            if self.detected_language == "Ancient Greek":
                # For Stanza
                tokens = [word for sent in doc.sentences for word in sent.words if word.text.isalpha()]
            else:
                # For spaCy
                tokens = [token for token in doc if not token.is_space and token.is_alpha]
            
            pattern_length = len(pattern_template)
            total_tokens = len(tokens)
            
            for i in range(len(tokens) - pattern_length + 1):
                token_sequence = tokens[i:i + pattern_length]
                
                if self.detected_language == "Ancient Greek":
                    # For Stanza
                    pos_sequence = [token.upos for token in token_sequence]
                    words = [token.text.lower() for token in token_sequence]
                else:
                    # For spaCy
                    pos_sequence = [token.pos_ for token in token_sequence]
                    words = [token.text.lower() for token in token_sequence]
                
                # Check if pattern matches (with wildcard support)
                match = True
                for j, (expected, actual) in enumerate(zip(pattern_template, pos_sequence)):
                    if expected != "*" and expected != actual:
                        match = False
                        break
                
                if match:
                    # Create pattern string
                    pos_pattern = "_".join([p if p != "*" else actual_pos 
                                          for p, actual_pos in zip(pattern_template, pos_sequence)])
                    word_pattern = " ".join(words)
                    
                    # Store as "POS_PATTERN: word pattern"
                    pattern_string = f"[{pos_pattern}]: {word_pattern}"
                    patterns.append(pattern_string)
                
                # Update progress periodically
                if i % 100 == 0:
                    progress = (i / total_tokens) * 100
                    self.window.after(0, lambda p=progress: self.update_results_progress(p))
            
            return Counter(patterns)
            
        except Exception as e:
            messagebox.showerror("Error", f"Custom pattern extraction error: {e}")
            return {}
            
    def display_file_preview(self):
        """Display beginning of selected text file in results area"""
        if not self.file_content:
            return
            
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        
        # Header
        language_flag = self.get_language_flag(self.detected_language)
        file_name = Path(self.selected_file).name
        header = f"📄 File Preview: {file_name} {language_flag}\n{'='*60}\n\n"
        
        # Text preview (first 2000 characters)
        preview_text = self.file_content[:2000]
        if len(self.file_content) > 2000:
            preview_text += "\n\n... [Text continues, select an analysis to see full results]"
        
        # Word count info
        word_count = len(self.file_content.split())
        char_count = len(self.file_content)
        
        header += f"📊 Text Statistics:\n"
        header += f"   • Language detected: {self.detected_language}\n"
        if self.detected_language == "Ancient Greek":
            header += f"   • NLP Engine: Stanza (specialized for Ancient Greek)\n"
        else:
            header += f"   • NLP Engine: spaCy\n"
        header += f"   • Total characters: {char_count:,}\n"
        header += f"   • Total words: {word_count:,}\n"
        header += f"   • Preview (first 2000 chars):\n\n"
        header += f"{'-'*60}\n\n"
        
        self.text_area.insert(tk.END, header + preview_text)
        self.text_area.config(state=tk.DISABLED)
            
    def display_results(self, title, result, export_name):
        """Modern results display"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        
        total = sum(result.values())
        unique = len(result)
        
        # Results header
        language_flag = self.get_language_flag(self.detected_language)
        header = f"{title} {language_flag}\n{'='*60}\n\n"
        header += f"📈 Statistics:\n"
        header += f"   • Total occurrences: {total:,}\n"
        header += f"   • Unique elements: {unique:,}\n"
        header += f"   • Source file: {Path(self.selected_file).name}\n"
        header += f"   • Detected language: {self.detected_language}\n"
        if self.detected_language == "Ancient Greek":
            header += f"   • NLP Engine: Stanza\n"
        else:
            header += f"   • NLP Engine: spaCy\n"
        header += "\n"
        
        self.text_area.insert(tk.END, header)
        
        if result:
            # Results table
            self.text_area.insert(tk.END, f"{'Element':<50} {'Occurrences':>12}\n")
            self.text_area.insert(tk.END, f"{'-'*50} {'-'*12}\n")
            
            # Sort by frequency (descending)
            for item, count in sorted(result.items(), key=lambda x: x[1], reverse=True):
                display_item = (item[:47] + '...') if len(item) > 47 else item
                self.text_area.insert(tk.END, f"{display_item:<50} {count:>12}\n")
                
            # Export offer with format choice
            export_window = tk.Toplevel(self.window)
            export_window.title("💾 Export Results")
            export_window.geometry("400x250")
            export_window.configure(bg=self.colors['bg_primary'])
            export_window.grab_set()
            export_window.transient(self.window)
            
            # Center the export window
            export_window.geometry("+{}+{}".format(
                self.window.winfo_rootx() + 250,
                self.window.winfo_rooty() + 150
            ))
            
            # Title
            tk.Label(export_window,
                    text="💾 Export Analysis Results",
                    font=('Segoe UI', 14, 'bold'),
                    fg=self.colors['accent'],
                    bg=self.colors['bg_primary']).pack(pady=(20, 15))
            
            # Info
            info_text = f"📊 {unique} unique elements to export\n🌍 Language: {self.detected_language}"
            tk.Label(export_window,
                    text=info_text,
                    font=('Segoe UI', 10),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['bg_primary']).pack(pady=(0, 20))
            
            # Format selection
            tk.Label(export_window,
                    text="Choose export format:",
                    font=('Segoe UI', 11, 'bold'),
                    fg=self.colors['text_primary'],
                    bg=self.colors['bg_primary']).pack()
            
            button_frame = tk.Frame(export_window, bg=self.colors['bg_primary'])
            button_frame.pack(pady=20)
            
            def export_excel():
                export_window.destroy()
                self.save_to_file(result, export_name, title, 'excel')
            
            def export_csv():
                export_window.destroy()
                self.save_to_file(result, export_name, title, 'csv')
            
            def cancel_export():
                export_window.destroy()
            
            # Excel button
            excel_btn = tk.Button(button_frame,
                                text="📊 Excel (.xlsx)",
                                command=export_excel,
                                bg=self.colors['accent'],
                                fg='white',
                                font=('Segoe UI', 10, 'bold'),
                                relief=tk.FLAT,
                                padx=20, pady=10)
            excel_btn.pack(side=tk.LEFT, padx=10)
            
            # CSV button
            csv_btn = tk.Button(button_frame,
                              text="📄 CSV (.csv)",
                              command=export_csv,
                              bg=self.colors['success'],
                              fg='white',
                              font=('Segoe UI', 10, 'bold'),
                              relief=tk.FLAT,
                              padx=20, pady=10)
            csv_btn.pack(side=tk.LEFT, padx=10)
            
            # Cancel button
            cancel_btn = tk.Button(export_window,
                                 text="❌ Cancel",
                                 command=cancel_export,
                                 bg=self.colors['text_secondary'],
                                 fg='white',
                                 font=('Segoe UI', 9),
                                 relief=tk.FLAT,
                                 padx=15, pady=8)
            cancel_btn.pack(pady=(10, 20))
        else:
            self.text_area.insert(tk.END, "❌ No results found.")
            
        self.text_area.config(state=tk.DISABLED)
        self.update_status(f"Analysis complete - {unique} elements found", self.colors['success'])
        
    def save_to_file(self, data, default_name, title, format_type):
        """Enhanced export with format choice and pattern-specific handling"""
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M')
        
        # Determine file extension and filter
        if format_type == 'excel':
            extension = ".xlsx"
            filetypes = [("Excel files", "*.xlsx")]
        else:
            extension = ".csv" 
            filetypes = [("CSV files", "*.csv")]
            
        filename = f"talos_{default_name}_{timestamp}{extension}"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=extension,
            initialfile=filename,
            filetypes=filetypes,
            title=f"Save Analysis Results ({format_type.upper()})"
        )
        
        if file_path:
            try:
                self.update_status(f"Saving {format_type.upper()} file...", self.colors['accent'])
                self.start_progress()
                
                # Check if this is pattern data (contains brackets and colons)
                is_pattern_data = any('[' in str(key) and ']:' in str(key) for key in data.keys())
                
                if is_pattern_data:
                    # Special handling for lexical-syntactic patterns
                    df = self.create_pattern_dataframe(data)
                else:
                    # Standard handling for other analyses
                    df = pd.DataFrame(list(data.items()), columns=["Element", "Occurrences"])
                    df = df.sort_values("Occurrences", ascending=False)
                
                # Add statistics
                stats_df = pd.DataFrame({
                    'Statistic': ['Total Occurrences', 'Unique Elements', 'Average per Element', 'Language Detected', 'NLP Engine'],
                    'Value': [df['Occurrences'].sum() if 'Occurrences' in df.columns else sum(data.values()), 
                             len(df), 
                             df['Occurrences'].mean() if 'Occurrences' in df.columns else sum(data.values())/len(data), 
                             self.detected_language,
                             'Stanza' if self.detected_language == 'Ancient Greek' else 'spaCy']
                })
                
                if format_type == 'excel':
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Results', index=False)
                        stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                else:
                    df.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                self.stop_progress()
                messagebox.showinfo("✅ Success", 
                                  f"Analysis saved successfully!\n\n📄 {Path(file_path).name}")
                self.update_status(f"Exported: {Path(file_path).name}", self.colors['success'])
                
            except Exception as e:
                self.stop_progress()
                messagebox.showerror("❌ Error", f"Save error:\n{str(e)}")
                
    def create_pattern_dataframe(self, pattern_data):
        """Create specialized DataFrame for lexical-syntactic patterns"""
        rows = []
        
        for pattern_string, count in pattern_data.items():
            try:
                # Parse pattern string: "[ADJ_NOUN]: beautiful house"
                if ']:' in pattern_string:
                    pos_part, word_part = pattern_string.split(']:')
                    pos_pattern = pos_part.strip('[')
                    word_pattern = word_part.strip()
                    
                    # Split POS pattern and words
                    pos_tags = pos_pattern.split('_')
                    words = word_pattern.split()
                    
                    # Create row with POS-named columns
                    row = {'Pattern': pos_pattern, 'Full_Example': word_pattern, 'Occurrences': count}
                    
                    # Add columns named by POS type (e.g., ADJ, NOUN, VERB, etc.)
                    for i, pos_tag in enumerate(pos_tags):
                        if i < len(words):
                            # Handle duplicate POS tags by adding suffix
                            col_name = pos_tag
                            counter = 1
                            while col_name in row:
                                counter += 1
                                col_name = f"{pos_tag}_{counter}"
                            
                            row[col_name] = words[i]
                    
                    rows.append(row)
                else:
                    # Fallback for malformed patterns
                    rows.append({
                        'Pattern': pattern_string,
                        'Full_Example': '',
                        'Occurrences': count
                    })
            except Exception:
                # Fallback for any parsing errors
                rows.append({
                    'Pattern': str(pattern_string),
                    'Full_Example': '',
                    'Occurrences': count
                })
        
        df = pd.DataFrame(rows)
        df = df.sort_values('Occurrences', ascending=False)
        
        return df
    
    def run(self):
        """Launch the application"""
        try:
            # Window icon (optional)
            # self.window.iconbitmap()  # Use .ico file if available
            pass
        except:
            pass
            
        self.window.mainloop()

# Main entry point
if __name__ == "__main__":
    try:
        app = TextAnalyzer()
        app.run()
    except Exception as e:
        import traceback
        print(f"Application launch error: {e}")
        print("Error details:")
        traceback.print_exc()
        input("Press Enter to close...")