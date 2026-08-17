from fpdf import FPDF
from models import ReviewResult
import os

def generate_pdf_report(repo_name: str, pr_number: int, analysis: ReviewResult) -> str:
    """
    Generates a PDF report for the code review.
    Returns the file path.
    """
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "CodeGuard AI - Enterprise Code Review Report", ln=True, align='C')
    pdf.ln(10)

    # Meta
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Repository: {repo_name}", ln=True)
    pdf.cell(0, 10, f"Pull Request: #{pr_number}", ln=True)
    pdf.ln(5)

    # Score & Recommendation
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Score: {analysis.score} / 100", ln=True)

    if analysis.recommendation == "APPROVED":
        pdf.set_text_color(0, 150, 0) # Green
    else:
        pdf.set_text_color(200, 0, 0) # Red

    pdf.cell(0, 10, f"Deploy Recommendation: {analysis.recommendation}", ln=True)
    pdf.set_text_color(0, 0, 0) # Reset
    pdf.ln(10)

    # Comments
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Review Comments:", ln=True)
    pdf.set_font("Arial", size=12)

    for c in analysis.comments:
        line_text = f"Line {c.line}: " if c.line > 0 else "General: "
        # Sanitize text to latin-1 to avoid FPDF UnicodeEncodeError
        safe_comment = c.comment.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, f"{line_text}{safe_comment}")
        pdf.ln(2)

    os.makedirs("/tmp/reports", exist_ok=True)
    file_path = f"/tmp/reports/report_{repo_name.replace('/', '_')}_{pr_number}.pdf"
    pdf.output(file_path)

    return file_path
