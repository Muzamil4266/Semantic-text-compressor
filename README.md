

## Screenshots

### Interface 1
![Interface 1](interface%201.png)








### Interface 2
![Interface 2](interface%202.png)






🧠 Semantic Text Compressor
AI that reads your text and tells you what really matters

🤔 What Is This?
Semantic Text Compressor is a smart desktop app that uses Artificial Intelligence to shrink long texts down to just 10% of their original size while keeping all the important meaning.

Imagine you have a 100-page report or a long article. Instead of reading everything, you just paste it in, click a button, and the AI gives you a short version that captures the key points. It's like having a smart friend who reads everything and tells you what's important.

✨ Why Use It?
📚 Save Time - Stop spending hours reading long documents. Get the key points in minutes.

🧠 Understand Better - The AI doesn't just cut sentences. It actually understands the meaning and rewrites it clearly.

📄 Any Document - Works with PDFs, Word files, and plain text. Just load and go.

🔒 Private - Everything runs on your computer. Your documents never go to the cloud.

💾 Save & Share - Copy the compressed text or save it as a file.

⚙️ How It Works
Simple 3 Steps
1️⃣ Paste or Load - Type your text or upload a PDF, DOCX, or TXT file.

2️⃣ Click Compress - The AI reads and understands your text.

3️⃣ Get Summary - A short version appears, ready to copy or save.

What Happens Behind the Scenes
📝 Text is Cleaned - The app removes extra spaces, links, and formatting that might confuse the AI.

🧩 Text is Split - If your text is long, it's broken into smaller chunks so the AI can handle it.

🤖 AI Reads Each Chunk - Using Google's FLAN-T5 model, the AI understands the meaning and creates a short summary for each part.

🔀 Combined & Polished - All the summaries are combined into one final compressed version.

⚡ Fast Processing - The app works quickly, even with long documents.

🚀 When to Use This
🎓 Students - Summarize textbook chapters, lecture notes, and research papers.

💼 Professionals - Get the key points from reports, proposals, and emails.

📰 News Readers - Quickly understand long articles and opinion pieces.

📚 Researchers - Extract important information from academic papers.

✍️ Writers - Condense your own writing to check if the key points are clear.

🧠 Personal Use - Save time reading anything long.

📥 Installation
What You Need
Python 3.8 or Higher - Download from python.org

Step 1: Install Dependencies
Open your terminal and run:

bash
pip install customtkinter transformers torch PyPDF2 python-docx
Step 2: Download the App
Save the Python file to your computer.

Step 3: Run It
bash
python semantic_text_compressor.py
💡 First Run Note: The app will download the AI model (~300MB). This happens once. Be patient!

🎮 How to Use
The Interface
The app has four simple sections:

1. INPUT TEXT - Where you paste or load your text.

2. AUTOMATIC COMPRESSION - Shows your word count and the target size.

3. COMPRESS & SAVE - The big purple button that does the magic.

4. OUTPUT - Where your compressed text appears.

Step-by-Step
Load Your Text

Paste text directly into the box OR

Click "📁 Load File" to upload a PDF, DOCX, or TXT

Check the Stats

See how many words you have

See how many words the compressed version will be (10:1 ratio)

Click Compress

Hit the big "🚀 COMPRESS NOW" button

Watch the progress bar and live logs

Wait a few seconds while the AI works

Get Your Result

The compressed text appears in the output box

Copy it with "📋 Copy" or save as a file with "💾 Save as .txt"

Watch the Logs
While processing, you'll see:

Which chunk is being processed

How many words are being compressed

Time taken for each step

Final compression ratio

🛠️ What's Inside
🖥️ GUI - CustomTkinter for a modern dark theme

🧠 AI Model - Google FLAN-T5-Small for understanding and compressing text

📄 PDF Support - PyPDF2 reads PDF files

📝 DOCX Support - python-docx reads Word documents

⚡ Multi-Stage Compression - Handles long texts by breaking them into chunks

💡 Tips for Best Results
Use Clean Text - The app cleans text automatically, but clear text gives better results.

Long Documents - The app handles long texts by splitting them into chunks. A 10,000-word document takes about 2 minutes.

Check the Output - The compressed text should capture the main points. Read it to make sure it makes sense.

Short Texts - If your text is under 100 words, the app won't compress it. It's already short enough!

🔧 Troubleshooting
❌ "customtkinter not installed"
Run: pip install customtkinter

❌ "transformers not installed"
Run: pip install transformers torch

❌ "No text to compress"
Paste some text or load a file first!

❌ "Model download slow"
The first download is ~300MB. It happens once and is worth the wait.

🐌 App is slow on first run
The model is loading into memory. Next runs will be faster.

📄 PDF not loading
Make sure the PDF has readable text. Scanned images won't work.

💻 System Requirements
Operating System - Windows, Linux, or MacOS

Python - 3.8 or higher

RAM - 4GB minimum, 8GB recommended

Storage - 500MB for AI model and app

Internet - Only for first-time model download

📂 File Support
Format	Supported
.txt	✅ Yes
.pdf	✅ Yes
.docx	✅ Yes
.doc	✅ Yes (old Word format)
🎯 Project Structure
text
Semantic Text Compressor/
├── semantic_text_compressor.py    # Main app
├── requirements.txt                # Dependencies
└── README.md                       # This file
📝 License
Free to use. Modify and share as you like.

🙏 Acknowledgments
Built with these amazing tools:

CustomTkinter - Beautiful GUI

Hugging Face Transformers - FLAN-T5 AI model

PyPDF2 - Reading PDFs

python-docx - Reading Word files

💬 Need Help?
Check the Live Logs section while processing - it shows exactly what's happening.

If something goes wrong, the app will show an error message with details.

🧠 Compress more. Understand everything.
Stop reading everything. Start understanding faster.


