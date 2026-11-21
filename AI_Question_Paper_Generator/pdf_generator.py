from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, KeepTogether
)


def create_pdf(paper, file_path, show_answers=False):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "PaperTitle", parent=styles["Title"],
        alignment=TA_CENTER, textColor=colors.HexColor("#34256F"),
        spaceAfter=12
    )
    question_style = ParagraphStyle(
        "Question", parent=styles["BodyText"],
        leading=16, spaceAfter=5
    )
    normal_style = ParagraphStyle(
        "PaperBody", parent=styles["BodyText"],
        leading=14, spaceAfter=4
    )

    doc = SimpleDocTemplate(
        file_path, pagesize=A4,
        rightMargin=20 * mm, leftMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm
    )

    elements = []
    elements.append(Paragraph(
        escape(paper.get("title", "Question Paper")), title_style
    ))
    elements.append(Paragraph(
        f"<b>Subject:</b> {escape(str(paper.get('subject', '')))}",
        normal_style
    ))
    elements.append(Paragraph(
        f"<b>Topic:</b> {escape(str(paper.get('topic', '')))}",
        normal_style
    ))
    elements.append(Paragraph(
        f"<b>Difficulty:</b> {escape(str(paper.get('difficulty', '')))}",
        normal_style
    ))

    questions = paper.get("questions", [])
    total_marks = sum(int(q.get("marks", 1)) for q in questions)
    elements.append(Paragraph(
        f"<b>Maximum Marks:</b> {total_marks}", normal_style
    ))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "<b>Instructions:</b> Answer all questions.",
        normal_style
    ))
    elements.append(Spacer(1, 10))

    for q in questions:
        block = []
        question_text = escape(str(q.get("question", "")))
        q_type = escape(str(q.get("type", "")))
        q_marks = int(q.get("marks", 1))
        block.append(Paragraph(
            f"<b>Q{q.get('number', '')}. {question_text}</b> "
            f"<font color='#6250A8'>[{q_marks} marks | {q_type}]</font>",
            question_style
        ))
        for option_index, option in enumerate(q.get("options", [])):
            label = chr(65 + option_index)
            block.append(Paragraph(
                f"{label}. {escape(str(option))}", normal_style
            ))
        if show_answers:
            block.append(Paragraph(
                f"<b>Answer:</b> {escape(str(q.get('answer', '')))}",
                normal_style
            ))
        block.append(Spacer(1, 10))
        elements.append(KeepTogether(block))

    doc.build(elements)
