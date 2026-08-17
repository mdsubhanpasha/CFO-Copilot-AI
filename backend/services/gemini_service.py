import os
from google import genai
from pydantic import BaseModel, Field
import json
from models import ReviewResult, ReviewComment

def analyze_code_diff(diff_str: str) -> ReviewResult:
    """
    Uses Gemini 2.0 Pro to analyze the PR diff for bugs, security vulnerabilities, performance issues, and PEP8 violations.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return ReviewResult(
            score=0,
            recommendation="ERROR: Missing API Key",
            comments=[ReviewComment(line=0, comment="Gemini API Key is not set in environment variables.")]
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are an expert Enterprise Code Review Assistant (CodeGuard AI).
        Please analyze the following GitHub PR code diff for:
        1. Bugs
        2. Security Vulnerabilities
        3. Performance Issues
        4. PEP8 Violations

        Give a score out of 100 based on the quality.
        Give a "Deploy Recommendation: APPROVED" if score > 80 and no severe security bugs, otherwise "NEEDS FIX".
        Generate human-readable review comments line-by-line (or file-by-file if line isn't obvious) on the code.

        PR Diff:
        {diff_str}

        Return the result EXACTLY as a JSON object matching this schema:
        {{
            "score": <integer between 0 and 100>,
            "recommendation": "<APPROVED or NEEDS FIX>",
            "comments": [
                {{"line": <integer roughly indicating line or just 0 if general>, "comment": "<your comment>"}}
            ]
        }}
        """

        response = client.models.generate_content(
            model='gemini-2.0-pro-exp-02-05',
            contents=prompt,
        )

        # We need to extract the JSON from the response text
        # Usually it comes in a markdown block, e.g., ```json ... ```
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
             text = text.split("```")[1].strip()

        data = json.loads(text)

        comments = [ReviewComment(**c) for c in data.get("comments", [])]

        return ReviewResult(
            score=data.get("score", 0),
            recommendation=data.get("recommendation", "NEEDS FIX"),
            comments=comments
        )

    except Exception as e:
         return ReviewResult(
            score=0,
            recommendation=f"ERROR: {str(e)}",
            comments=[ReviewComment(line=0, comment=f"Failed to analyze diff: {str(e)}")]
        )
