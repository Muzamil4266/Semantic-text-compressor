#!/usr/bin/env python3
"""
SEMANTIC TEXT COMPRESSOR
AI-Powered Semantic Understanding & Automatic Compression
Built with CustomTkinter + FLAN-T5 Model

Usage:
    python semantic_text_compressor.py

First run downloads FLAN-T5-Small (~300MB) - be patient!
"""

import sys
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import site

sys.path.insert(0, site.getusersitepackages())

try:
    import customtkinter as ctk
except ImportError:
    print("[!] customtkinter not installed. Run: pip install customtkinter")
    sys.exit(1)

try:
    from transformers import T5Tokenizer, T5ForConditionalGeneration
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[!] transformers not installed. Run: pip install transformers torch")

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# ============================================================
# CONFIGURATION
# ============================================================
RATIO = 10
APP_NAME = "Semantic Text Compressor"
APP_VERSION = "1.0.0"
MODEL_NAME = "google/flan-t5-small"

# ============================================================
# THEME SETUP
# ============================================================
ctk.set_appearance_mode("dark")

BG_COLOR = "#0f1117"
CARD_BG = "#1a1d26"
CARD_BORDER = "#2a2d3a"
ACCENT_PURPLE = "#7c3aed"
ACCENT_BLUE = "#2563eb"
ACCENT_GREEN = "#10b981"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#9ca3af"
TEXT_MUTED = "#6b7280"

# ============================================================
# TEXT EXTRACTION (PDF, TXT, DOCX)
# ============================================================

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.txt':
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    elif ext == '.pdf':
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
        text = ""
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text
    elif ext == '.docx':
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx not installed. Run: pip install python-docx")
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use .txt, .pdf, or .docx")


def count_words(text):
    return len(re.findall(r'\b\w+\b', text))


def count_chars(text):
    return len(text)


def clean_text(text):
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    text = re.sub(r'[^\w\s.,;:!?\-\'"()\[\]{}]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ============================================================
# CHUNKING FOR LONG TEXTS
# ============================================================

def split_into_chunks(text, max_chunk_words=500):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_words = 0

    for sent in sentences:
        sent_words = len(sent.split())
        if current_words + sent_words > max_chunk_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sent]
            current_words = sent_words
        else:
            current_chunk.append(sent)
            current_words += sent_words

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# ============================================================
# AI SUMMARIZATION ENGINE (FLAN-T5)
# ============================================================

class FLAN5Summarizer:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.model_loaded = False

    def load_model(self, status_callback=None):
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers library not installed. Run: pip install transformers torch")

        if status_callback:
            status_callback("Loading FLAN-T5 AI model...")

        self.tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
        self.model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
        self.model_loaded = True

        if status_callback:
            status_callback("AI model ready!")

    def summarize_text(self, text, target_words):
        if not self.model_loaded:
            self.load_model()

        prompt = f"summarize: {text}"

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )

        # FIX: Convert target words to estimated tokens (FLAN-T5 uses tokens, not words)
        # Roughly 1 word ≈ 1.3-1.5 tokens for English text
        estimated_tokens = int(target_words * 1.5)

        max_new_tokens = estimated_tokens + 30
        min_new_tokens = max(estimated_tokens - 30, 20)

        # FIX: Use max_new_tokens/min_new_tokens instead of max_length/min_length
        # max_length counts input + output, max_new_tokens counts only generated output
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_new_tokens=max_new_tokens,
            min_new_tokens=min_new_tokens,
            num_beams=4,
            early_stopping=False,  # FIXED: No early stopping - must reach target length
            no_repeat_ngram_size=3
        )

        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    def summarize_long_text(self, text, target_words, status_callback=None, log_callback=None):
        if not self.model_loaded:
            if status_callback:
                status_callback("Loading AI model...")
            self.load_model(status_callback)

        chunks = split_into_chunks(text, max_chunk_words=500)
        total_chunks = len(chunks)

        if log_callback:
            log_callback(f"[INFO] Text split into {total_chunks} chunks for processing.")

        if status_callback:
            status_callback(f"Processing {total_chunks} chunks...")

        chunk_summaries = []
        start_time = time.time()

        for i, chunk in enumerate(chunks):
            chunk_start = time.time()

            if status_callback:
                status_callback(f"Processing chunk {i+1}/{total_chunks}...")
            if log_callback:
                log_callback(f"[>] Processing chunk {i+1}/{total_chunks} with AI...")

            chunk_words = len(chunk.split())
            chunk_target = max(chunk_words // RATIO, 30)

            # Log the target for debugging
            if log_callback:
                log_callback(f"[>] Chunk {i+1} target: {chunk_target} words (from {chunk_words} words)")

            summary = self.summarize_text(chunk, chunk_target)
            chunk_summaries.append(summary)

            chunk_time = time.time() - chunk_start
            summary_words = len(summary.split())

            if log_callback:
                log_callback(f"[>] Chunk {i+1} done. Extracted {summary_words} words. ({chunk_time:.1f}s)")

            # Progress update
            progress = (i + 1) / total_chunks * 0.7  # 70% for chunking
            if status_callback:
                status_callback(f"Chunk {i+1}/{total_chunks} complete")

        combined = " ".join(chunk_summaries)
        combined_words = len(combined.split())

        if log_callback:
            log_callback(f"[>] Stage 2: All chunks summarized. Combined: {combined_words} words.")

        if combined_words > target_words * 1.5 and total_chunks > 1:
            if status_callback:
                status_callback("Final polish...")
            if log_callback:
                log_callback("[>] Stage 3: Multi-pass compression needed.")

            final_target = max(target_words, 50)

            if combined_words > 500:
                sub_chunks = split_into_chunks(combined, max_chunk_words=400)
                sub_summaries = []
                for j, sub_chunk in enumerate(sub_chunks):
                    if log_callback:
                        log_callback(f"[>] Final polish {j+1}/{len(sub_chunks)}...")
                    sub_target = max(final_target // len(sub_chunks), 20)
                    sub_summary = self.summarize_text(sub_chunk, sub_target)
                    sub_summaries.append(sub_summary)
                final_summary = " ".join(sub_summaries)
            else:
                final_summary = self.summarize_text(combined, final_target)

            if log_callback:
                log_callback("[>] Finalizing output...")
        else:
            if log_callback:
                log_callback("[>] Stage 3: Single-pass compression sufficient.")
            final_summary = combined

        final_words = len(final_summary.split())
        if final_words > target_words:
            words = final_summary.split()
            final_summary = " ".join(words[:target_words])
            last_period = final_summary.rfind('.')
            if last_period > len(final_summary) * 0.8:
                final_summary = final_summary[:last_period + 1]

        total_time = time.time() - start_time
        if log_callback:
            log_callback(f"[OK] Compression complete! {count_words(text)} -> {final_words} words in {total_time:.1f}s")

        return final_summary


# ============================================================
# MAIN APPLICATION
# ============================================================

class SemanticTextCompressor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("850x950")
        self.minsize(800, 700)
        self.configure(fg_color=BG_COLOR)

        self.current_text = ""
        self.output_text = ""
        self.engine = FLAN5Summarizer()
        self.log_start_time = None

        self._build_ui()

    def _build_ui(self):
        # Main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=BG_COLOR,
            scrollbar_button_color=ACCENT_PURPLE,
            scrollbar_button_hover_color=ACCENT_BLUE
        )
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # ========== HEADER ==========
        header = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        header.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header,
            text="SEMANTIC TEXT COMPRESSOR",
            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        title_label.pack(anchor="center")

        subtitle = ctk.CTkLabel(
            header,
            text="AI-Powered  •  Semantic Understanding  •  Automatic Compression",
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(anchor="center", pady=(2, 10))

        # Tagline pill
        tagline = ctk.CTkFrame(header, fg_color=CARD_BG, corner_radius=20, border_width=1, border_color=ACCENT_PURPLE)
        tagline.pack(anchor="center", pady=(0, 10))

        tagline_label = ctk.CTkLabel(
            tagline,
            text="✨  Compress more. Understand everything.",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=ACCENT_PURPLE
        )
        tagline_label.pack(padx=20, pady=8)

        # ========== SECTION 1: INPUT TEXT ==========
        input_section = self._create_section(self.main_frame, "1. INPUT TEXT", "📄")
        input_section.grid(row=1, column=0, sticky="ew", padx=30, pady=10)

        input_header = ctk.CTkFrame(input_section, fg_color=CARD_BG)
        input_header.pack(fill="x", padx=20, pady=(15, 5))

        input_title = ctk.CTkLabel(
            input_header,
            text="Paste your text or load a file to compress",
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color=TEXT_SECONDARY
        )
        input_title.pack(side="left")

        # Load File button
        load_btn = ctk.CTkButton(
            input_header,
            text="📁 Load File",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            width=120,
            height=32,
            corner_radius=8,
            fg_color=CARD_BG,
            border_width=1,
            border_color=ACCENT_PURPLE,
            text_color=TEXT_PRIMARY,
            hover_color="#2a1d4a",
            command=self._load_file
        )
        load_btn.pack(side="right")

        # Input text area
        self.input_textbox = ctk.CTkTextbox(
            input_section,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="word",
            corner_radius=10,
            fg_color="#0d0f14",
            border_width=1,
            border_color=CARD_BORDER,
            height=150
        )
        self.input_textbox.pack(fill="x", padx=20, pady=10)
        self.input_textbox.insert("0.0", "Paste your text here...")
        self.input_textbox.bind("<KeyRelease>", self._update_input_stats)

        # Input stats
        input_stats = ctk.CTkFrame(input_section, fg_color=CARD_BG)
        input_stats.pack(fill="x", padx=20, pady=(0, 15))

        self.input_word_label = ctk.CTkLabel(
            input_stats,
            text="📄 0 words",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=TEXT_SECONDARY
        )
        self.input_word_label.pack(side="left")

        self.input_char_label = ctk.CTkLabel(
            input_stats,
            text="|  0 characters",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=TEXT_MUTED
        )
        self.input_char_label.pack(side="left", padx=(10, 0))

        self.ready_label = ctk.CTkLabel(
            input_stats,
            text="Ready to compress ✓",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=ACCENT_GREEN
        )
        self.ready_label.pack(side="right")

        # ========== SECTION 2: AUTOMATIC COMPRESSION ==========
        compression_section = self._create_section(self.main_frame, "2. AUTOMATIC COMPRESSION", "📊")
        compression_section.grid(row=2, column=0, sticky="ew", padx=30, pady=10)

        compression_desc = ctk.CTkLabel(
            compression_section,
            text="We automatically calculate the perfect compression based on your text length",
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color=TEXT_SECONDARY
        )
        compression_desc.pack(anchor="w", padx=20, pady=(10, 15))

        # Stats cards row
        stats_row = ctk.CTkFrame(compression_section, fg_color=CARD_BG)
        stats_row.pack(fill="x", padx=20, pady=(0, 15))

        # Your Text card
        your_text_card = self._create_stat_card(stats_row, "Your Text", "0", "words", "📄")
        your_text_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Arrow
        arrow_label = ctk.CTkLabel(
            stats_row,
            text="→",
            font=ctk.CTkFont(family="Helvetica", size=24),
            text_color=ACCENT_PURPLE
        )
        arrow_label.pack(side="left", padx=5)

        # AI card
        ai_card = self._create_ai_card(stats_row)
        ai_card.pack(side="left", padx=5)

        # Arrow
        arrow_label2 = ctk.CTkLabel(
            stats_row,
            text="→",
            font=ctk.CTkFont(family="Helvetica", size=24),
            text_color=ACCENT_PURPLE
        )
        arrow_label2.pack(side="left", padx=5)

        # Compressed Output card
        output_card = self._create_stat_card(stats_row, "Compressed Output", "0", "words", "📄")
        output_card.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Feature badges row
        badges_row = ctk.CTkFrame(compression_section, fg_color=CARD_BG)
        badges_row.pack(fill="x", padx=20, pady=(0, 15))

        self._create_badge(badges_row, "🧠", "Smart Algorithm", "Understands meaning,\nnot just words").pack(side="left", fill="both", expand=True, padx=(0, 5))
        self._create_badge(badges_row, "🔍", "Semantic Analysis", "Captures essence\nand key points").pack(side="left", fill="both", expand=True, padx=5)
        self._create_badge(badges_row, "⚡", "Auto Compression", "10 words → 1 word\n(Automatically)", accent=True).pack(side="left", fill="both", expand=True, padx=5)
        self._create_badge(badges_row, "🔀", "Multi-Stage", "Chunking + Hierarchical\nSummarization").pack(side="left", fill="both", expand=True, padx=(5, 0))

        # ========== SECTION 3: COMPRESS & SAVE ==========
        action_section = self._create_section(self.main_frame, "3. COMPRESS & SAVE", "🚀")
        action_section.grid(row=3, column=0, sticky="ew", padx=30, pady=10)

        action_desc = ctk.CTkLabel(
            action_section,
            text="Compress your text and save the result",
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color=TEXT_SECONDARY
        )
        action_desc.pack(anchor="w", padx=20, pady=(10, 15))

        # Compress button
        self.compress_btn = ctk.CTkButton(
            action_section,
            text="🚀 COMPRESS NOW",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            height=50,
            corner_radius=12,
            fg_color=ACCENT_PURPLE,
            hover_color="#6d28d9",
            command=self._compress
        )
        self.compress_btn.pack(fill="x", padx=20, pady=(0, 10))

        btn_subtitle = ctk.CTkLabel(
            action_section,
            text="⚡ Fast  •  Accurate  •  AI-Powered",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=TEXT_MUTED
        )
        btn_subtitle.pack(anchor="center", pady=(0, 15))

        # ========== SECTION 3.5: LIVE LOGS & PROGRESS ==========
        logs_section = self._create_section(self.main_frame, "LIVE LOGS & PROGRESS", "📋")
        logs_section.grid(row=4, column=0, sticky="ew", padx=30, pady=10)

        # Progress bar
        progress_frame = ctk.CTkFrame(logs_section, fg_color=CARD_BG)
        progress_frame.pack(fill="x", padx=20, pady=(10, 5))

        self.progress_pct_label = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=ACCENT_PURPLE
        )
        self.progress_pct_label.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=8,
            corner_radius=4,
            fg_color="#0d0f14",
            progress_color=ACCENT_PURPLE,
            border_width=0
        )
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=(10, 10))
        self.progress_bar.set(0)

        self.eta_label = ctk.CTkLabel(
            progress_frame,
            text="Ready",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=TEXT_MUTED
        )
        self.eta_label.pack(side="right")

        # Logs text area
        self.logs_textbox = ctk.CTkTextbox(
            logs_section,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word",
            corner_radius=10,
            fg_color="#0d0f14",
            border_width=1,
            border_color=CARD_BORDER,
            height=120
        )
        self.logs_textbox.pack(fill="x", padx=20, pady=10)
        self.logs_textbox.insert("0.0", "Logs will appear here during compression...")
        self.logs_textbox.configure(state="disabled")

        # ========== SECTION 4: OUTPUT ==========
        output_section = self._create_section(self.main_frame, "4. OUTPUT (COMPRESSED TEXT)", "📋")
        output_section.grid(row=5, column=0, sticky="ew", padx=30, pady=10)

        output_header = ctk.CTkFrame(output_section, fg_color=CARD_BG)
        output_header.pack(fill="x", padx=20, pady=(15, 5))

        output_title = ctk.CTkLabel(
            output_header,
            text="Your compressed text will appear here",
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color=TEXT_SECONDARY
        )
        output_title.pack(side="left")

        # Copy button
        self.copy_btn = ctk.CTkButton(
            output_header,
            text="📋 Copy",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            width=100,
            height=32,
            corner_radius=8,
            fg_color=CARD_BG,
            border_width=1,
            border_color=ACCENT_PURPLE,
            text_color=TEXT_PRIMARY,
            hover_color="#2a1d4a",
            command=self._copy_output
        )
        self.copy_btn.pack(side="right")

        # Output text area
        self.output_textbox = ctk.CTkTextbox(
            output_section,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="word",
            corner_radius=10,
            fg_color="#0d0f14",
            border_width=1,
            border_color=CARD_BORDER,
            height=150
        )
        self.output_textbox.pack(fill="x", padx=20, pady=10)
        self.output_textbox.insert("0.0", "Compressed text will appear here...")
        self.output_textbox.configure(state="disabled")

        # Output stats + Save button
        output_stats = ctk.CTkFrame(output_section, fg_color=CARD_BG)
        output_stats.pack(fill="x", padx=20, pady=(0, 15))

        self.output_word_label = ctk.CTkLabel(
            output_stats,
            text="0 words",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=TEXT_SECONDARY
        )
        self.output_word_label.pack(side="left")

        self.output_char_label = ctk.CTkLabel(
            output_stats,
            text="|  0 characters",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=TEXT_MUTED
        )
        self.output_char_label.pack(side="left", padx=(10, 0))

        # Save as .txt button
        self.save_btn = ctk.CTkButton(
            output_stats,
            text="💾 Save as .txt",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            width=130,
            height=32,
            corner_radius=8,
            fg_color=ACCENT_GREEN,
            hover_color="#059669",
            text_color="white",
            command=self._save_output
        )
        self.save_btn.pack(side="right")

        # ========== FOOTER ==========
        footer = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        footer.grid(row=6, column=0, sticky="ew", padx=30, pady=(10, 20))

        # Footer badges
        footer_badges = ctk.CTkFrame(footer, fg_color=BG_COLOR)
        footer_badges.pack(fill="x")

        self._create_footer_badge(footer_badges, "🛡️", "Semantic Understanding", "Deep understanding\nof context and meaning").pack(side="left", fill="both", expand=True, padx=(0, 5))
        self._create_footer_badge(footer_badges, "⚡", "Super Fast", "Optimized for speed\nand efficiency").pack(side="left", fill="both", expand=True, padx=5)
        self._create_footer_badge(footer_badges, "🔒", "Privacy First", "Your data stays on\nyour device").pack(side="left", fill="both", expand=True, padx=5)
        self._create_footer_badge(footer_badges, "📤", "Export Ready", "Save as .txt and use\nanywhere").pack(side="left", fill="both", expand=True, padx=(5, 0))

        # Bottom bar
        bottom_bar = ctk.CTkFrame(footer, fg_color=BG_COLOR)
        bottom_bar.pack(fill="x", pady=(15, 0))

        bottom_text = ctk.CTkLabel(
            bottom_bar,
            text="Built with CustomTkinter  •  FLAN-T5 Model  •  Local AI Power",
            font=ctk.CTkFont(family="Helvetica", size=11),
            text_color=TEXT_MUTED
        )
        bottom_text.pack(side="left")

        version_text = ctk.CTkLabel(
            bottom_bar,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(family="Helvetica", size=11),
            text_color=TEXT_MUTED
        )
        version_text.pack(side="right")

    def _create_section(self, parent, title, icon):
        section = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=15, border_width=1, border_color=CARD_BORDER)

        header = ctk.CTkFrame(section, fg_color=CARD_BG)
        header.pack(fill="x", padx=20, pady=(15, 0))

        icon_label = ctk.CTkLabel(
            header,
            text=icon,
            font=ctk.CTkFont(family="Helvetica", size=18),
            text_color=ACCENT_PURPLE
        )
        icon_label.pack(side="left")

        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        title_label.pack(side="left", padx=(10, 0))

        return section

    def _create_stat_card(self, parent, title, value, unit, icon):
        card = ctk.CTkFrame(parent, fg_color="#0d0f14", corner_radius=12, border_width=1, border_color=CARD_BORDER)

        title_lbl = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            text_color=TEXT_SECONDARY
        )
        title_lbl.pack(pady=(15, 5))

        icon_lbl = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(family="Helvetica", size=28),
            text_color=ACCENT_PURPLE
        )
        icon_lbl.pack()

        value_lbl = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(family="Helvetica", size=32, weight="bold"),
            text_color=ACCENT_PURPLE
        )
        value_lbl.pack()

        unit_lbl = ctk.CTkLabel(
            card,
            text=unit,
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=TEXT_MUTED
        )
        unit_lbl.pack(pady=(0, 15))

        return card

    def _create_ai_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color="#0d0f14", corner_radius=50, border_width=2, border_color=ACCENT_PURPLE, width=80, height=80)
        card.pack_propagate(False)

        ai_label = ctk.CTkLabel(
            card,
            text="AI",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
            text_color=ACCENT_PURPLE
        )
        ai_label.pack(expand=True)

        return card

    def _create_badge(self, parent, icon, title, desc, accent=False):
        color = ACCENT_GREEN if accent else TEXT_SECONDARY
        badge = ctk.CTkFrame(parent, fg_color="#0d0f14", corner_radius=10, border_width=1, border_color=CARD_BORDER)

        content = ctk.CTkFrame(badge, fg_color="#0d0f14")
        content.pack(padx=10, pady=10)

        icon_lbl = ctk.CTkLabel(
            content,
            text=icon,
            font=ctk.CTkFont(family="Helvetica", size=20),
            text_color=color
        )
        icon_lbl.pack(anchor="w")

        title_lbl = ctk.CTkLabel(
            content,
            text=title,
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        title_lbl.pack(anchor="w", pady=(5, 0))

        desc_lbl = ctk.CTkLabel(
            content,
            text=desc,
            font=ctk.CTkFont(family="Helvetica", size=10),
            text_color=TEXT_MUTED
        )
        desc_lbl.pack(anchor="w")

        return badge

    def _create_footer_badge(self, parent, icon, title, desc):
        badge = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=CARD_BORDER)

        content = ctk.CTkFrame(badge, fg_color=CARD_BG)
        content.pack(padx=10, pady=10)

        top_row = ctk.CTkFrame(content, fg_color=CARD_BG)
        top_row.pack(fill="x")

        icon_lbl = ctk.CTkLabel(
            top_row,
            text=icon,
            font=ctk.CTkFont(family="Helvetica", size=18),
            text_color=ACCENT_PURPLE
        )
        icon_lbl.pack(side="left")

        title_lbl = ctk.CTkLabel(
            top_row,
            text=title,
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        title_lbl.pack(side="left", padx=(8, 0))

        desc_lbl = ctk.CTkLabel(
            content,
            text=desc,
            font=ctk.CTkFont(family="Helvetica", size=10),
            text_color=TEXT_MUTED
        )
        desc_lbl.pack(anchor="w", pady=(5, 0))

        return badge

    def _update_input_stats(self, event=None):
        text = self.input_textbox.get("0.0", "end").strip()
        if text == "Paste your text here...":
            words = 0
            chars = 0
        else:
            words = count_words(text)
            chars = count_chars(text)

        self.input_word_label.configure(text=f"📄 {words} words")
        self.input_char_label.configure(text=f"|  {chars} characters")

        # Update compression stats cards
        target = max(words // RATIO, 0)
        # Find and update the stat card values
        for widget in self.main_frame.winfo_children():
            self._update_stat_values(widget, words, target)

    def _update_stat_values(self, widget, words, target):
        """Recursively find and update stat card values."""
        if isinstance(widget, ctk.CTkLabel):
            text = widget.cget("text")
            if text == "0" and widget.cget("font").cget("size") == 32:
                # Check parent to determine which card this is
                parent = widget.master
                for sibling in parent.winfo_children():
                    if isinstance(sibling, ctk.CTkLabel):
                        sibling_text = sibling.cget("text")
                        if sibling_text == "Your Text":
                            widget.configure(text=str(words))
                        elif sibling_text == "Compressed Output":
                            widget.configure(text=str(target))

        for child in widget.winfo_children():
            self._update_stat_values(child, words, target)

    def _add_log(self, message):
        """Add a log message to the logs textbox."""
        timestamp = time.strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"

        self.logs_textbox.configure(state="normal")
        self.logs_textbox.insert("end", log_line)
        self.logs_textbox.see("end")
        self.logs_textbox.configure(state="disabled")

    def _update_progress(self, percentage, status_text=""):
        """Update progress bar and status. Fixed to handle string status."""
        self.progress_bar.set(percentage / 100.0)
        self.progress_pct_label.configure(text=f"{int(percentage)}%")

        if status_text:
            self.eta_label.configure(text=status_text)
        elif percentage >= 100:
            self.eta_label.configure(text="Done!")
        else:
            self.eta_label.configure(text="Processing...")

    def _load_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a document",
            filetypes=[
                ("All Supported Files", "*.txt;*.pdf;*.docx;*.doc"),
                ("PDF Files", "*.pdf"),
                ("Text Files", "*.txt"),
                ("Word Documents", "*.docx;*.doc"),
                ("All Files", "*.*")
            ]
        )
        if filepath:
            try:
                text = extract_text(filepath)
                self.input_textbox.delete("0.0", "end")
                self.input_textbox.insert("0.0", text)
                self._update_input_stats()
                self.ready_label.configure(text=f"✓ Loaded: {os.path.basename(filepath)}")
                self._add_log(f"[INFO] File loaded: {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
                self._add_log(f"[ERROR] Failed to load file: {str(e)}")

    def _compress(self):
        text = self.input_textbox.get("0.0", "end").strip()
        if not text or text == "Paste your text here...":
            messagebox.showwarning("No Text", "Please paste text or load a file first.")
            return

        if not TRANSFORMERS_AVAILABLE:
            messagebox.showerror(
                "Missing Dependency",
                "The AI engine requires:\n\n"
                "pip install transformers torch\n\n"
                "Please install and restart."
            )
            return

        # Clear logs and reset progress
        self.logs_textbox.configure(state="normal")
        self.logs_textbox.delete("0.0", "end")
        self.logs_textbox.configure(state="disabled")
        self._add_log("[INFO] Starting compression...")

        self.compress_btn.configure(state="disabled", text="⏳ Compressing...")
        self.ready_label.configure(text="Processing with AI...")
        self._update_progress(0, "Initializing...")
        self.log_start_time = time.time()

        def process():
            try:
                clean = clean_text(text)
                original_words = count_words(clean)
                target_words = max(original_words // RATIO, 50)

                self.after(0, lambda: self._update_progress(5, "Loading AI model..."))
                self.after(0, lambda: self._add_log(f"[INFO] Input: {original_words} words. Target: {target_words} words."))

                if original_words < 100:
                    result = clean
                    self.after(0, lambda: self._update_progress(100, "Done!"))
                    self.after(0, lambda: self._add_log("[INFO] Text too short for AI compression. Returning as-is."))
                else:
                    result = self.engine.summarize_long_text(
                        clean, 
                        target_words,
                        status_callback=lambda msg: self.after(0, lambda: self.ready_label.configure(text=msg)),
                        log_callback=lambda msg: self.after(0, lambda: self._add_log(msg))
                    )
                    self.after(0, lambda: self._update_progress(100, "Done!"))

                output_words = count_words(result)
                output_chars = count_chars(result)

                self.after(0, lambda: self._show_output(result, original_words, output_words, output_chars))

            except Exception as e:
                self.after(0, lambda: self._show_error(str(e)))

        threading.Thread(target=process, daemon=True).start()

    def _show_output(self, result, original_words, output_words, output_chars):
        self.output_text = result

        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("0.0", "end")
        self.output_textbox.insert("0.0", result)
        self.output_textbox.configure(state="disabled")

        self.output_word_label.configure(text=f"{output_words} words")
        self.output_char_label.configure(text=f"|  {output_chars} characters")

        self.compress_btn.configure(state="normal", text="🚀 COMPRESS NOW")
        self.ready_label.configure(text=f"✓ Compressed {original_words} → {output_words} words")

        self._update_progress(100, "Done!")
        self._add_log(f"[OK] Final: {original_words} -> {output_words} words ({original_words//max(output_words,1)}:1 ratio)")

    def _show_error(self, message):
        self.compress_btn.configure(state="normal", text="🚀 COMPRESS NOW")
        self.ready_label.configure(text=f"Error: {message}")
        self._update_progress(0, "Error")
        self._add_log(f"[ERROR] {message}")
        messagebox.showerror("Error", message)

    def _copy_output(self):
        if self.output_text:
            self.clipboard_clear()
            self.clipboard_append(self.output_text)
            self.copy_btn.configure(text="✓ Copied!")
            self.after(2000, lambda: self.copy_btn.configure(text="📋 Copy"))

    def _save_output(self):
        if not self.output_text:
            messagebox.showwarning("No Output", "Compress text first before saving.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="compressed_output.txt"
        )
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.output_text)
            self.save_btn.configure(text="✓ Saved!")
            self.after(2000, lambda: self.save_btn.configure(text="💾 Save as .txt"))


# ============================================================
# MAIN ENTRY
# ============================================================

def main():
    app = SemanticTextCompressor()
    app.mainloop()


if __name__ == "__main__":
    main()
