import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

SKILL_DB = {
    "Python": ["python", "pandas", "numpy"],
    "Machine Learning": ["machine learning", "sklearn", "scikit-learn"],
    "Deep Learning": ["deep learning", "tensorflow", "pytorch", "keras"],
    "NLP": ["nlp", "natural language", "transformers", "bert", "spacy", "nltk"],
    "Generative AI": ["generative ai", "genai", "llm", "langchain", "rag", "gpt", "hugging face"],
    "Data Analysis": ["data analysis", "data analytics", "matplotlib", "seaborn"],
    "SQL": ["sql", "mysql", "postgresql"],
    "Cloud & DevOps": ["aws", "azure", "docker", "kubernetes", "gcp"],
    "MLOps & Git": ["mlops", "git", "github", "ci/cd", "jenkins"],
    "Web Development": ["html", "css", "react", "flask", "django", "javascript"]
}

JOB_ROLES = {
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP", "Generative AI", "Cloud & DevOps"],
    "Data Scientist": ["Python", "Machine Learning", "Data Analysis", "SQL", "Deep Learning"],
    "GenAI Engineer": ["Python", "Generative AI", "NLP", "Deep Learning", "Cloud & DevOps", "MLOps & Git"],
    "ML Engineer": ["Python", "Machine Learning", "Deep Learning", "MLOps & Git", "Cloud & DevOps"],
    "Full Stack Developer": ["Web Development", "SQL", "Python", "Cloud & DevOps"]
}

COURSE_MAP = {
    "Python": {"course": "Python for Everybody", "platform": "Coursera", "link": "https://www.coursera.org/specializations/python", "days": 21, "priority": "High"},
    "Machine Learning": {"course": "ML by Andrew Ng", "platform": "Coursera", "link": "https://www.coursera.org/specializations/machine-learning-introduction", "days": 30, "priority": "High"},
    "Deep Learning": {"course": "Deep Learning Specialization", "platform": "Coursera", "link": "https://www.coursera.org/specializations/deep-learning", "days": 45, "priority": "High"},
    "NLP": {"course": "Hugging Face NLP Course", "platform": "Hugging Face", "link": "https://huggingface.co/learn/nlp-course", "days": 25, "priority": "High"},
    "Generative AI": {"course": "Generative AI with LLMs", "platform": "Coursera", "link": "https://www.coursera.org/learn/generative-ai-with-llms", "days": 20, "priority": "High"},
    "Data Analysis": {"course": "Google Data Analytics", "platform": "Coursera", "link": "https://www.coursera.org/professional-certificates/google-data-analytics", "days": 20, "priority": "Medium"},
    "SQL": {"course": "SQL for Data Science", "platform": "Udemy", "link": "https://www.udemy.com/topic/sql/", "days": 14, "priority": "Medium"},
    "Cloud & DevOps": {"course": "AWS Cloud + Docker", "platform": "AWS", "link": "https://aws.amazon.com/training/", "days": 30, "priority": "High"},
    "Web Development": {"course": "Meta Full Stack", "platform": "Coursera", "link": "https://www.coursera.org/professional-certificates/meta-front-end-developer", "days": 30, "priority": "Low"},
    "MLOps & Git": {"course": "MLOps Zoomcamp", "platform": "GitHub", "link": "https://github.com/DataTalksClub/mlops-zoomcamp", "days": 20, "priority": "Medium"}
}

def extract_skills_advanced(text):
    text_lower = text.lower()
    found = {}
    for skill, keywords in SKILL_DB.items():
        for kw in keywords:
            if kw in text_lower:
                score = 85 if text_lower.count(kw) > 2 else 70
                if kw in ["python", "machine learning", "sql"]:
                    score = min(95, score + 10)
                found[skill] = max(found.get(skill, 0), score)
                break
    if not found:
        found = {"Python": 60}
    return found

def analyze_gap_pro(found_skills, job_role):
    required = JOB_ROLES.get(job_role, [])
    matched = [s for s in required if s in found_skills]
    missing = [s for s in required if s not in found_skills]
    score = int((len(matched) / len(required) * 100)) if required else 0
    if score >= 80:
        level = "Highly Ready - FAANG Level"
    elif score >= 60:
        level = "Moderately Ready"
    elif score >= 40:
        level = "Needs Improvement"
    else:
        level = "Significant Gap"
    radar_values = [found_skills.get(s, 0) for s in required]
    return {"score": score, "matched": matched, "missing": missing, "required": required, "level": level, "radar_values": radar_values}

def generate_roadmap(missing_skills):
    roadmap = []
    total = 0
    for skill in missing_skills:
        info = COURSE_MAP.get(skill, {"course": f"Learn {skill}", "platform": "YouTube", "link": f"https://www.youtube.com/results?search_query={skill}", "days": 15, "priority": "Medium"})
        roadmap.append({"skill": skill, **info})
        total += info["days"]
    return roadmap, total

def career_path_mapping(current_score):
    if current_score < 40:
        return {"path": "Beginner -> Junior Developer -> Practice Projects", "next_role": "Python Developer Intern", "months": 3}
    elif current_score < 70:
        return {"path": "Junior -> Mid Level -> Build Portfolio", "next_role": "Data Scientist / AI Engineer", "months": 2}
    else:
        return {"path": "Mid -> Senior -> Ready for FAANG", "next_role": "Senior AI Engineer / MLOps", "months": 1}

def trend_analysis():
    return {
        "Hot Skills 2026": ["GenAI", "LLM Fine-tuning", "RAG", "MLOps", "LangChain"],
        "High Demand": "AI Engineer +40%, GenAI +120% YoY",
        "Salary Trend": "AI Engineer Avg 12-18 LPA India"
    }