# utils/analyzer.py

import ollama
import json
import re

def analyze_resume_with_ollama(text: str) -> dict:
    prompt = f"""
You are an expert resume reviewer. Based on the resume below, return a JSON with the following fields:

{{
  "summary": "Short summary of candidate profile",
  "strengths": ["List 3-5 strong points in resume"],
  "areas_to_improve": ["List 3-5 suggestions to improve resume"],
  "job_roles_fit": ["Suggest 3-5 job titles suitable for the resume"],
  "keyword_suggestions": ["List of missing keywords to improve ATS visibility"],
  "final_tips": ["Any last tips or recommendations"]
}}

Resume:
{text}

Respond ONLY with JSON.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return safe_json_extract(response['message']['content'])

def match_resume_to_job(resume: str, job_description: str) -> dict:
    prompt = f"""
Given the candidate resume and job description, return a JSON with:

{{
  "match_score": float between 0.0 to 1.0,
  "matched_skills": ["skills present in both resume and JD"],
  "missing_skills": ["skills required in JD but not found in resume"],
  "recommendations": ["suggestions to improve resume for this JD"],
  "summary": "short summary about candidate fit"
}}

Resume:
{resume}

Job Description:
{job_description}

Respond ONLY with JSON.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return safe_json_extract(response['message']['content'])

def safe_json_extract(content: str) -> dict:
    try:
        # Try to extract the first JSON object from the content
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            json_str = match.group()
            return json.loads(json_str)
        return {"error": "No JSON object found in LLM response", "raw_output": content}
    except Exception:
        return {"error": "Failed to parse response from LLM", "raw_output": content}