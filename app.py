from flask import Flask, render_template, request, send_file
try:
    import pymupdf
    def read_pdf(file):
        doc = pymupdf.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
except:
    import fitz
    def read_pdf(file):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])

import docx
from skill_analyzer import extract_skills_advanced, analyze_gap_pro, generate_roadmap, JOB_ROLES, career_path_mapping, trend_analysis
import plotly.graph_objects as go
import plotly.express as px
import sqlite3
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('analysis_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, job_role TEXT, score INTEGER, matched TEXT, missing TEXT, date TEXT)''')
    conn.commit()
    conn.close()

def save_analysis(job_role, score, matched, missing):
    conn = sqlite3.connect('analysis_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (job_role, score, matched, missing, date) VALUES (?,?,?,?,?)", (job_role, score, str(matched), str(missing), datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('analysis_history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

init_db()

def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

@app.route('/', methods=['GET','POST'])
def index():
    result = None
    job_roles = list(JOB_ROLES.keys())
    if request.method == 'POST':
        job_role = request.form.get('job_role')
        text = ""
        if 'resume_file' in request.files and request.files['resume_file'].filename:
            f = request.files['resume_file']
            if f.filename.endswith('.pdf'):
                text = read_pdf(f)
            else:
                text = read_docx(f)
        else:
            text = request.form.get('resume_text','')
        if text:
            found = extract_skills_advanced(text)
            gap = analyze_gap_pro(found, job_role)
            roadmap, total_days = generate_roadmap(gap['missing'])
            career = career_path_mapping(gap['score'])
            trends = trend_analysis()
            save_analysis(job_role, gap['score'], gap['matched'], gap['missing'])
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=gap['radar_values'], theta=gap['required'], fill='toself', name='Your Skills'))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), title=f"Skill Profile - {job_role}")
            radar_html = fig_radar.to_html(full_html=False)
            fig_bar = px.bar(x=list(found.keys()), y=list(found.values()), title="Skill Proficiency %", color=list(found.values()), color_continuous_scale='Viridis')
            bar_html = fig_bar.to_html(full_html=False)
            result = {"found": found, "gap": gap, "roadmap": roadmap, "total_days": total_days, "radar": radar_html, "bar": bar_html, "text_len": len(text), "job_role": job_role, "career": career, "trends": trends}
    return render_template('index.html', result=result, job_roles=job_roles)

@app.route('/history')
def history_page():
    data = get_history()
    return render_template('history.html', data=data)

@app.route('/download_report/<role>/<int:score>')
def download_report(role, score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"AI Skill Gap Analyzer Pro - Report")
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Intern ID: DAS007968 | Task: AI-SS-014")
    p.drawString(100, 710, f"Job Role: {role}")
    p.drawString(100, 690, f"ATS Score: {score}%")
    p.drawString(100, 670, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Report_{role}_{score}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)