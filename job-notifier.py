import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Email setup
EMAIL_SENDER = "kamalakanta902@gmail.com"
EMAIL_PASSWORD = "okcv abmo jchq amxq"  # Use an app-specific password
EMAIL_RECEIVER = "kamalakanta902@gmail.com"

def fetch_internshala():
    url = "https://internshala.com/internships/cloud-internship/rss.xml"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'xml')
    jobs = []

    for item in soup.find_all("item")[:5]:
        title = item.title.text.strip()
        link = item.link.text.strip()
        jobs.append({
            "title": title,
            "link": link,
            "source": "Internshala"
        })
    return jobs

def fetch_remotive():
    url = "https://remoteok.com/api"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    jobs_data = resp.json()
    jobs = []

    for job in jobs_data:
        position = job.get('position', '')
        description = job.get('description', '')
        if any(keyword in position.lower() for keyword in ['cloud', 'devops']) and \
           any(level in position.lower() + description.lower() for level in ['intern', 'junior', 'entry', 'fresher']):
            jobs.append({
                "title": job['position'],
                "link": "https://remoteok.com" + job['url'],
                "source": "RemoteOK"
            })
    return jobs

def send_email(jobs):
    if not jobs:
        return

    message_body = f"<h2>{len(jobs)} Cloud/DevOps Jobs Found</h2><ul>"
    for job in jobs:
        message_body += f"<li><b>{job['title']}</b> - {job['source']}<br><a href='{job['link']}'>Apply</a></li>"
    message_body += "</ul>"

    msg = MIMEText(message_body, 'html')
    msg['Subject'] = f"🧑‍💻 {len(jobs)} New Fresher/Intern Jobs - {datetime.now().strftime('%d %b %Y %H:%M')}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

def job_notifier():
    all_jobs = fetch_internshala() + fetch_remotive()
    send_email(all_jobs)

# For manual run
if __name__ == "__main__":
    job_notifier()
