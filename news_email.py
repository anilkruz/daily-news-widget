import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
import os

# Secrets
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
SENDER = os.getenv('EMAIL_SENDER')
PASSWORD = os.getenv('EMAIL_PASSWORD')
RECEIVER = os.getenv('EMAIL_RECEIVER')

def get_ist_time():
    return datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)

def is_morning():
    return get_ist_time().hour < 12

def get_news():
    url = f"https://newsapi.org/v2/everything?q=US+Israel+Iran+war+OR+Hormuz+OR+Hezbollah+rockets+OR+Mojtaba+Khamenei&sortBy=publishedAt&language=en&pageSize=8&apiKey={NEWS_API_KEY}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            arts = resp.json()['articles'][:5]
            lines = []
            for a in arts:
                title = a.get('title', 'No title')
                desc = a.get('description') or (a.get('content')[:120] + '...') if a.get('content') else 'No desc'
                source = a['source']['name']
                date = a['publishedAt'][:10]
                lines.append(f"**{title}** ({source} - {date})\n{desc}\n---")
            return '\n'.join(lines) or "Koi fresh nahi 😅"
        return f"Fail: {resp.status_code}"
    except:
        return "News load fail"

def send_email():
    now = get_ist_time()
    morn = is_morning()
    subj = "Halchal Morning 🌍" if morn else "Halchal Evening 🌍"
    
    news = get_news()
    
    body = f"""
Iran ke new Supreme Leader Mojtaba Khamenei ne first statement mein bola: Strait of Hormuz band rahega – "tool to pressure enemy" aur US bases band karo warna attack! 🚢💥 (State TV pe read kiya gaya, wo public mein nahi dikhe abhi.)

Oil Brent ~$99-100+ pahunch gaya (up 8%+ aaj), shipping full mess Strait mein, Asia mein fuel panic aur global supply biggest disruption ever.

Hezbollah ne overnight 100-200+ rockets barrage kiya Lebanon se Israel pe (north + Haifa, Tel Aviv tak), sirens baj gaye, millions bomb shelters mein gaye. Iran proxies se missiles continue, dono taraf heavy strikes chal rahe.

Fresh headlines NewsAPI se:
{news}
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = subj
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        server.quit()
        print("Sent! 🔥")
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    send_email()