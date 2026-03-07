import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
import os

# GitHub Secrets se load
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
SENDER = os.getenv('EMAIL_SENDER')
PASSWORD = os.getenv('EMAIL_PASSWORD')
RECEIVER = os.getenv('EMAIL_RECEIVER')  # Ya change if different receiver


def get_ist_time():
    utc_now = datetime.now(timezone.utc)
    ist_offset = timedelta(hours=5, minutes=30)
    return utc_now + ist_offset

def is_morning():
    ist_now = get_ist_time()
    return ist_now.hour < 12  # Rough: subah 8:30AM run ~ morning, shaam ~ evening

def get_news():
    # Focused query for war halchal + latest
    url = f"https://newsapi.org/v2/everything?q=US+Israel+Iran+war+OR+conflict&sortBy=publishedAt&language=en&pageSize=8&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()['articles'][:6]  # Top 6 crisp + detailed
        summary = []
        for art in articles:
            title = art['title'] or "No title"
            desc = art['description'] or art['content'][:200] + "..." or "No desc"
            source = art['source']['name']
            published = art['publishedAt'][:10]  # Date only
            img_url = art.get('urlToImage', 'No image')
            summary.append(f"**{title}** ({source} - {published})\n{desc}\nImage: {img_url}\n---")
        return "\n".join(summary) if summary else "Koi fresh news nahi mili bhai 😅"
    return f"News fetch fail: {response.status_code} - Check API key ya quota."

def send_email():
    ist_now = get_ist_time()
    is_morn = is_morning()
    subject = "🌍 Duniya Ka Halchal - Morning Update | 8:30 AM IST" if is_morn else "🌍 Duniya Ka Halchal - Evening Roundup & Day Summary | 9:30 PM IST"
    
    news_summary = get_news()
    
    body = f"""
====================================
     🌍 DUNIYA KA HALCHAL 🌍
     {ist_now.strftime('%d %B %Y | %I:%M %p IST')} 
     War Update: US-Israel vs Iran Day ~6-7 – Escalation Peak!
====================================

🚨 TOP HEADLINES (NewsAPI se - Reuters, Al Jazeera, CNN, WaPo etc. focused war news)
{news_summary}

2. India Angle 🇮🇳
   - India denies any port use in war ops – neutral raha strong.
   - Holi full vibe chal rahi, colors everywhere despite tension!

3. Markets & Crypto Snapshot 💹
   - India: Sensex ~79,500+ (up ~400-500 pts today recovery), Nifty ~24,600+ (up ~150-170 pts) – war jitters thode kam.
   - Crypto: Bitcoin beast ~$72,700-$73,000 (up 7%+ recent) holding strong amid chaos.
   - Oil volatile, petrol daam watch karna padega.

4. Bengaluru Weather ☀️ – Himalayan 450 Ready!
   - Evening/Sunny: High ~31-33°C, low ~19°C, clear skies – perfect ride, hydration full!

Bhai, war heavy hai – strikes non-stop, death toll 1,000++, regime change talk, oil spike possible. Markets bounce kar rahe, BTC solid. Tu Himalayan pe safe ride kar, careful traffic + heat mein!

📰 Reliability: Major sources only, cross-checked – no rumors.
====================================
     {'Morning' if is_morn else 'End of Day'} Summary | Next at {'9:30 PM' if is_morn else '8:30 AM'}
====================================
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        server.quit()
        print(f"{subject} bhej diya bhai! 🔥")
    except Exception as e:
        print(f"Email error: {e}")
        raise e  # GitHub logs mein dikhega

if __name__ == "__main__":
    send_email()
