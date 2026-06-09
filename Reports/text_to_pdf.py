from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
import os

# PATH SETUP
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
PDF_PATH = os.path.join(os.path.dirname(__file__), "contract_summaries.pdf")


doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    alignment=1  # Center
)

section_style = ParagraphStyle(
    "SectionStyle",
    parent=styles["Heading2"],
    spaceAfter=10
)

sub_section_style = ParagraphStyle(
    "SubSectionStyle",
    parent=styles["Heading3"],
    spaceAfter=8
)

body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["Normal"],
    spaceAfter=10
)

content =[]


content.append(Paragraph(
    "Legal Document Summarization Report",
    title_style
))
content.append(Spacer(1, 20))
content.append(Paragraph(
    "Extractive and Abstractive Summaries using CUAD Dataset",
    styles["Normal"]
))
content.append(PageBreak())


for i in range(1, 6):
    txt_file = os.path.join(OUTPUT_DIR, f"contract_{i}.txt")

    if not os.path.exists(txt_file):
        continue

    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Split sections
    extractive = ""
    abstractive = ""

    if "EXTRACTIVE SUMMARY" in text:
        extractive = text.split("EXTRACTIVE SUMMARY")[1].split("ABSTRACTIVE SUMMARY")[0].strip()
        abstractive = text.split("ABSTRACTIVE SUMMARY")[1].split("ROUGE")[0].strip()

    # Contract Title
    content.append(Paragraph(f"Contract {i}", section_style))
    content.append(Spacer(1, 10))

    # Extractive
    content.append(Paragraph("Extractive Summary", sub_section_style))
    content.append(Paragraph(extractive.replace("\n", "<br/>"), body_style))
    content.append(Spacer(1, 15))

    # Abstractive
    content.append(Paragraph("Abstractive Summary", sub_section_style))
    content.append(Paragraph(abstractive.replace("\n", "<br/>"), body_style))

    content.append(PageBreak())

# BUILD PDF
doc.build(content)

print("✅ contract_summaries.pdf generated with proper structure")
