

## Screenshots

### Interface 1
![Interface 1](interface%201.png)








### Interface 2
![Interface 2](interface%202.png)






🧠 Semantic Text Compressor
Compress more. Understand everything.
AI-Powered Text Compression with Semantic Understanding

# Semantic Text Compressor



🤔 What is Semantic Text Compressor?
Semantic Text Compressor is a powerful desktop application that uses Artificial Intelligence to automatically compress long texts while preserving their core meaning. Unlike simple text summarizers that just extract sentences, this tool understands the context and rewrites content in a concise, coherent form.

Think of it as having a smart assistant that reads through pages of text and tells you exactly what matters most, saving you hours of reading time.

✨ Key Features
🤖 AI-Powered - Uses Google's FLAN-T5 model for deep semantic understanding of your text. The AI doesn't just copy sentences—it comprehends the meaning and rewrites it concisely.

📄 Multi-Format Support - Works seamlessly with .txt text files, .pdf documents, and .docx Word files. Just load and compress!

⚡ Fast Processing - Harnesses all your CPU cores for parallel processing, making compression lightning fast even for long documents.

🔍 Smart Filtering - Applies 5 intelligent quality filters to remove junk, duplicates, questions, incomplete sentences, and OCR garbage from the output.

🔒 Privacy First - Everything runs locally on your device. Your data never leaves your computer. No cloud uploads, no privacy concerns.

📤 Export Ready - Save compressed text as .txt files or copy directly to clipboard for use anywhere.

⚙️ How It Works
The Magic Behind the Scenes
The tool follows a simple 3-stage process that transforms lengthy text into concise, meaningful summaries:

📄 INPUT → 🧠 AI UNDERSTANDING → 🔍 QUALITY FILTERS → 📋 OUTPUT

🧩 Stage 1: Intelligent Chunking
Long texts are split into manageable chunks that the AI can process efficiently. Each chunk is handled independently while maintaining context across boundaries. This ensures even book-length documents can be compressed without losing the bigger picture.

🤖 Stage 2: AI Summarization with FLAN-T5
Each chunk is analyzed by the FLAN-T5 AI model, which extracts key concepts, relationships, and important facts. The AI then rewrites the content in a compressed form, removing redundancy and filler while preserving the essential meaning. The tool automatically calculates the perfect compression ratio of 10:1, meaning 10 words become 1.

🧹 Stage 3: Quality Filters
Five smart filters clean up the AI-generated summary:

❓ Remove Questions - Eliminates question sentences that don't add value to the summary.

🔄 Remove Repetitions - Filters out redundant content where words appear too frequently.

🔀 Remove Duplicates - Keeps only unique information, removing semantically similar sentences.

✏️ Fix Incomplete Sentences - Ensures proper punctuation and removes fragments that don't make sense.

🗑️ Remove OCR Garbage - Eliminates random characters, typos, and suspicious words that might come from scanned documents.

🚀 Applications
Where Can You Use This?
📚 Research - Quickly extract key points from academic papers and research articles without reading every word.

📝 News Analysis - Get the essence of long news articles and opinion pieces instantly.

📖 Book Summaries - Compress book chapters into digestible summaries for quick review.

📊 Report Generation - Create executive summaries from detailed business reports and proposals.

🎓 Study Notes - Condense lecture notes and textbook chapters for quick revision before exams.

💼 Business Communication - Summarize long emails, meeting transcripts, and project documentation.

📰 Content Curation - Extract important points from large documents for newsletters or briefings.

🧠 Personal Knowledge Management - Build a compressed library of everything you read.

📥 Installation & Setup
🪟 Windows / 🐧 Linux / 🍎 MacOS
Step 1: Install Python

Make sure you have Python 3.8 or higher installed on your system. You can download it from python.org if you don't have it yet.

Step 2: Download the Program

Clone the repository or download the Python file directly to your computer.

bash
git clone https://github.com/yourusername/semantic-text-compressor.git
cd semantic-text-compressor
Step 3: Install Required Dependencies

Open your terminal or command prompt and run this command to install everything you need:

bash
pip install customtkinter transformers torch PyPDF2 python-docx
Step 4: Run the Application

Launch the program with this simple command:

bash
python semantic_text_compressor.py
💡 First-time Note: The first time you run the app, it will download the FLAN-T5 AI model which is about 300MB. This happens only once, so be patient!

🎮 How to Use
🖥️ Interface Guide
📄 SECTION 1: INPUT TEXT

Start by pasting your text directly into the input area OR click the "📁 Load File" button to upload a .txt, .pdf, or .docx file. As you type or load text, you'll see live stats showing word count and character count.

📊 SECTION 2: AUTOMATIC COMPRESSION

The interface shows three cards in a row: Your Text → AI → Compressed Output. The word counts update automatically, and the AI calculates the perfect compression target. The system works with a 10:1 ratio, so a 1000-word document becomes a 100-word summary.

🚀 SECTION 3: COMPRESS & SAVE

Click the big purple "COMPRESS NOW" button to start the AI magic. While processing, you'll see:

A progress bar showing exactly how far along the compression is

Live logs displaying every step of the process

Status updates telling you what the AI is doing

📋 SECTION 4: OUTPUT

Once compression is complete, your compressed text appears in the output area. You can:

Copy it to your clipboard with one click

Save it as a .txt file using the green save button

Review the word count and compression ratio achieved

📋 LIVE LOGS & PROGRESS

A dedicated log area shows you exactly what's happening in real-time. You'll see chunk processing status, AI model loading, quality filter application, and final compression statistics. This transparency helps you understand how your text is being transformed.

🛠️ Technology Stack
🖥️ GUI Framework - CustomTkinter provides the modern, dark-themed interface that's both beautiful and functional.

🧠 AI Model - Google's FLAN-T5-Small from the Transformers library does the heavy lifting of understanding and compressing text.

📄 PDF Support - PyPDF2 extracts text from PDF documents seamlessly.

📝 DOCX Support - python-docx reads Microsoft Word files effortlessly.

🔄 Parallel Processing - ThreadPoolExecutor harnesses all your CPU cores for maximum speed.

🧹 Quality Filters - Custom Python algorithms clean and polish the final output.

📊 Performance Expectations
For most texts, you can expect a 10:1 compression ratio, meaning a 500-word text becomes about 50 words. Processing time depends on your hardware, but the app is optimized for speed:

A short 500-word text compresses in about 10 seconds. A 2000-word document takes roughly 30 seconds. Even a 10,000-word research paper compresses in about 2 minutes. The parallel processing ensures your CPU is fully utilized.

🔧 Troubleshooting
❌ "customtkinter not installed" - Run pip install customtkinter in your terminal.

❌ "transformers not installed" - Run pip install transformers torch to install the AI engine.

❌ "No text to compress" - Make sure you've pasted text or loaded a file before clicking compress.

❌ "Model download slow" - The first-time download is about 300MB. This happens only once, so be patient.

🐌 "App is slow" - The FLAN-T5-Small model runs on CPU. On first run, it loads the model into memory. Subsequent runs will be faster.

📄 "Can't load PDF" - Ensure your PDF is text-based, not scanned images. For scanned PDFs, you'll need OCR software first.

💾 "Out of memory" - For very large documents (50,000+ words), try splitting your text into smaller files.

📝 License
This project is open-source and available under the MIT License. Feel free to use, modify, and distribute it for personal or commercial purposes.

🙏 Acknowledgments
Built with ❤️ using amazing open-source tools:

CustomTkinter for the beautiful GUI

Hugging Face Transformers for the FLAN-T5 model

PyPDF2 and python-docx for document support

💬 Support
Have questions or suggestions? Feel free to open an issue on GitHub or reach out to the community. Your feedback helps make this tool better for everyone!
