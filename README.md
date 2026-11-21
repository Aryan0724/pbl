# AI Question Paper Generator (PaperAI)
### BCA AI & Data Science — Problem Based Learning (PBL) Project

An AI-powered web application built with **Python Flask** and **Google Gemini API** that generates comprehensive examination question papers from user-entered topics or uploaded study material PDFs.

---

## 🌟 Features
- **AI-Powered Question Generation**: Automatically generates questions using Google Gemini API (`gemini-3-flash-preview`).
- **Multiple Question Formats**:
  - Multiple Choice Questions (MCQ) with 4 options & correct answer
  - Short Answer Questions
  - Long Answer / Descriptive Questions
  - Mixed Question Papers
- **Customizable Difficulty Levels**: Easy (Basic recall), Intermediate (Application), and Hard (Analysis & critical thinking).
- **PDF Study Material Upload**: Extracts selectable text directly from uploaded PDFs using PyPDF2.
- **SQLite Database**: Automatically saves generated papers with timestamp and difficulty.
- **Instant Printable PDF Export**:
  - Student Question Paper PDF (without answers)
  - Teacher Answer Key PDF (with complete model answers)
- **Paper History**: Review and re-download previously generated papers anytime.

---

## 🚀 Quick Setup & Run

### 1. Install Dependencies
```bash
cd AI_Question_Paper_Generator
pip install -r requirements.txt
```

### 2. Configure Environment (`.env`)
Create a `.env` file inside `AI_Question_Paper_Generator/`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3-flash-preview
FLASK_SECRET_KEY=pbl-paperai-secret-2024-xk9j2m
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open in Browser
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)
