import json
import os
import uuid
from dotenv import load_dotenv
from flask import (
    Flask, render_template, request, redirect,
    url_for, send_file, flash
)
from werkzeug.utils import secure_filename
from generator import generate_questions
from pdf_reader import read_pdf
from pdf_generator import create_pdf
from database import create_table, save_paper, get_paper, list_papers

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv(
    "FLASK_SECRET_KEY", "change-this-development-secret"
)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "generated_papers"
ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

create_table()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    uploaded_path = None
    try:
        subject = request.form.get("subject", "").strip()
        topic = request.form.get("topic", "").strip()
        question_type = request.form.get("question_type", "")
        difficulty = request.form.get("difficulty", "")
        number = int(request.form.get("number", 10))
        marks = int(request.form.get("marks", 2))

        if not subject or not topic:
            raise ValueError("Enter both subject and topic.")
        if question_type not in {"MCQ", "Short", "Long", "Mixed"}:
            raise ValueError("Select a valid question type.")
        if difficulty not in {"Easy", "Intermediate", "Hard"}:
            raise ValueError("Select a valid difficulty level.")
        if not 1 <= number <= 30:
            raise ValueError("Number of questions must be from 1 to 30.")
        if marks not in {1, 2, 3, 5, 10}:
            raise ValueError("Select a valid marks value.")

        content = topic
        uploaded_file = request.files.get("pdf_file")
        if uploaded_file and uploaded_file.filename:
            if not allowed_file(uploaded_file.filename):
                raise ValueError("Only PDF files are allowed.")
            safe_name = secure_filename(uploaded_file.filename)
            unique_name = f"{uuid.uuid4().hex}_{safe_name}"
            uploaded_path = os.path.join(UPLOAD_FOLDER, unique_name)
            uploaded_file.save(uploaded_path)
            content = read_pdf(uploaded_path)

        paper = generate_questions(
            topic=topic,
            content=content,
            question_type=question_type,
            difficulty=difficulty,
            number_of_questions=number,
            subject=subject,
            marks=marks
        )
        paper_id = save_paper(subject, topic, difficulty, paper)
        return redirect(url_for("result", paper_id=paper_id))

    except Exception as error:
        app.logger.exception("Question paper generation failed")
        flash(str(error))
        return redirect(url_for("home"))
    finally:
        if uploaded_path and os.path.exists(uploaded_path):
            os.remove(uploaded_path)


@app.route("/result/<int:paper_id>")
def result(paper_id):
    record = get_paper(paper_id)
    if not record:
        return "Question paper not found.", 404
    paper = json.loads(record["paper_data"])
    return render_template(
        "result.html", paper=paper, paper_id=paper_id
    )


@app.route("/download/<int:paper_id>")
def download(paper_id):
    record = get_paper(paper_id)
    if not record:
        return "Question paper not found.", 404
    paper = json.loads(record["paper_data"])
    file_path = os.path.join(
        OUTPUT_FOLDER, f"question_paper_{paper_id}.pdf"
    )
    create_pdf(paper, file_path, show_answers=False)
    return send_file(
        file_path, as_attachment=True,
        download_name=f"Question_Paper_{paper_id}.pdf"
    )


@app.route("/answer-key/<int:paper_id>")
def answer_key(paper_id):
    record = get_paper(paper_id)
    if not record:
        return "Question paper not found.", 404
    paper = json.loads(record["paper_data"])
    file_path = os.path.join(
        OUTPUT_FOLDER, f"answer_key_{paper_id}.pdf"
    )
    create_pdf(paper, file_path, show_answers=True)
    return send_file(
        file_path, as_attachment=True,
        download_name=f"Answer_Key_{paper_id}.pdf"
    )


@app.route("/history")
def history():
    papers = list_papers()
    return render_template("history.html", papers=papers)


@app.errorhandler(413)
def file_too_large(error):
    flash("The uploaded PDF exceeds the 10 MB limit.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
