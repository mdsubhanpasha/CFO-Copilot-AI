from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(title="CodeGuard AI", description="Enterprise Code Review SaaS")

# Basic dependency to check role based on a dummy token
def verify_role(roles: list[str]):
    def _verify(token: str):
        # Dummy verification: Token is just "role_token" e.g., "Developer_token"
        for role in roles:
            if token == f"{role}_token":
                return token
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return _verify

class ReviewRequest(BaseModel):
    repo_name: str
    pr_number: int

class ReviewResponse(BaseModel):
    score: int
    recommendation: str
    comments: list[dict]

@app.get("/")
def read_root():
    return {"message": "Welcome to CodeGuard AI"}

from services.github_service import fetch_pr_diff
from services.gemini_service import analyze_code_diff
from services.pdf_service import generate_pdf_report
from fastapi.responses import FileResponse
from models import ReviewResult

@app.post("/analyze", response_model=ReviewResult)
def analyze_pr(request: ReviewRequest, token: str = Depends(verify_role(["Developer", "QA"]))):
    diff = fetch_pr_diff(request.repo_name, request.pr_number)
    if diff.startswith("Error"):
        raise HTTPException(status_code=500, detail=diff)

    analysis = analyze_code_diff(diff)
    return analysis

@app.post("/export-pdf")
def export_pdf(request: ReviewRequest, analysis: ReviewResult, token: str = Depends(verify_role(["Client"]))):
    pdf_path = generate_pdf_report(request.repo_name, request.pr_number, analysis)
    return FileResponse(path=pdf_path, filename=f"Review_Report_PR_{request.pr_number}.pdf", media_type="application/pdf")
