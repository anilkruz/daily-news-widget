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

def translate_to_hinglish(text):
    """Simple English to Hinglish translator"""
    if not text:
        return "Koi description nahi"
    
    # Common word replacements
    replacements = {
        # News related
        'says': 'boli/bola',
        'said': 'kaha',
        'told': 'bataya',
        'announced': 'announce kiya',
        'launched': 'launch kiya',
        'launches': 'launch kiya',
        'introduces': 'introduce kiya',
        'introduced': 'introduce kiya',
        'attacks': 'attack kiya',
        'attacked': 'attack kiya',
        'strikes': 'strike kiya',
        'hits': 'maara',
        'killed': 'mare gaye',
        'died': 'death ho gayi',
        'injured': 'ghayal',
        'wounded': 'ghayal',
        'arrested': 'arrest kiya',
        'detained': 'hafta kar liya',
        
        # Political
        'government': 'sarkar',
        'minister': 'mantri',
        'prime minister': 'PM',
        'chief minister': 'CM',
        'president': 'president',
        'election': 'chunav',
        'vote': 'vote',
        'parliament': 'sansad',
        'court': 'adalat',
        'law': 'kanoon',
        'bill': 'bill',
        
        # Economic
        'price': 'bhav',
        'prices': 'bhav',
        'market': 'bazaar',
        'stock market': 'share bazaar',
        'rupee': 'rupiya',
        'dollar': 'dollar',
        'economy': 'arthvyavastha',
        'business': 'karobar',
        'company': 'company',
        'tax': 'tax',
        
        # General
        'today': 'aaj',
        'yesterday': 'kal',
        'tomorrow': 'kal',
        'now': 'abhi',
        'new': 'naya',
        'big': 'bada',
        'huge': 'bahut bada',
        'important': 'jaruri',
        'breaking': 'breaking',
        'update': 'update',
        'news': 'khabar',
        'report': 'report',
        'investigation': 'jaanch',
        
        # Action words
        'will': 'karega',
        'can': 'sakta',
        'must': 'hoga',
        'should': 'chahiye',
        'going to': 'wala',
        'planning': 'plan bana raha',
        'considering': 'soch raha',
        
        # India specific
        'india': 'Bharat',
        'indian': 'Bharatiya',
        'delhi': 'Dilli',
        'mumbai': 'Mumbai',
        'kolkata': 'Kolkata',
        'chennai': 'Chennai',
        'bangalore': 'Bengaluru',
    }
    
    # Simple word-by-word replacement (basic version)
    words = text.split()
    hinglish_words = []
    
    for word in words:
        word_lower = word.lower().strip('.,!?;:()"\'')
        if word_lower in replacements:
            # Preserve original capitalization pattern
            if word[0].isupper():
                hinglish_words.append(replacements[word_lower].title())
            else:
                hinglish_words.append(replacements[word_lower])
        else:
            hinglish_words.append(word)
    
    hinglish_text = ' '.join(hinglish_words)
    
    # Common phrases
    hinglish_text = hinglish_text.replace('is a', 'ek hai')
    hinglish_text = hinglish_text.replace('is an', 'ek hai')
    hinglish_text = hinglish_text.replace('are', 'hain')
    hinglish_text = hinglish_text.replace('was', 'tha')
    hinglish_text = hinglish_text.replace('were', 'the')
    
    return hinglish_text

def get_news():
    # India + Middle East mix query
    url = f"https://newsapi.org/v2/everything?q=India+OR+Bharat+OR+Modi+OR+Delhi+OR+Mumbai+OR+US+Israel+Iran+war+OR+Hormuz+OR+Hezbollah&sortBy=publishedAt&language=en&pageSize=10&apiKey={NEWS_API_KEY}"
    
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            arts = resp.json().get('articles', [])[:7]  # 7 articles
            
            if not arts:
                return "Koi fresh news nahi mili 😅"
            
            lines = []
            lines.append("🇮🇳 **NAMASTE! Aaj ki Badi Khabrein** 🇮🇳\n")
            lines.append("═══════════════════════════════\n")
            
            for i, a in enumerate(arts, 1):
                title = a.get('title', 'No title')
                
                # Title Hinglish mein
                title_hing = translate_to_hinglish(title)
                
                # Description handle
                desc = a.get('description')
                if not desc and a.get('content'):
                    desc = a['content'][:120] + '...'
                elif not desc:
                    desc = 'Koi detail nahi mili'
                
                # Description Hinglish mein
                desc_hing = translate_to_hinglish(desc)
                
                source = a['source'].get('name', 'Unknown Source')
                
                # Date format
                raw_date = a.get('publishedAt', '')
                if raw_date:
                    date_obj = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
                    ist_date = date_obj + timedelta(hours=5, minutes=30)  # Convert to IST
                    date = ist_date.strftime('%d %b %Y, %I:%M %p')
                else:
                    date = 'Date nahi'
                
                # India news hai ya foreign, check karo
                is_india = any(word in title.lower() for word in ['india', 'bharat', 'modi', 'delhi', 'mumbai', 'bangalore', 'chennai', 'kolkata', 'indian'])
                flag = "🇮🇳" if is_india else "🌍"
                location = "Hindustan" if is_india else "Duniya"
                
                # Hinglish format with emojis
                lines.append(f"{flag} **Khabar {i}: {title_hing}**")
                lines.append(f"📝 {desc_hing}")
                lines.append(f"🏢 Source: {source} | 📍 {location} | 🕒 {date}")
                lines.append("───────────────────────────")
            
            return '\n'.join(lines)
        else:
            return f"News API fail: {resp.status_code}"
    except Exception as e:
        return f"News load nahi hua: {str(e)}"

def send_email():
    now = get_ist_time()
    morn = is_morning()
    
    # Subject Hinglish mein
    if morn:
        subj = "🌅 Suprabhat! Aaj ki Taaza Hinglish Khabrein"
    else:
        subj = "🌆 Shubh Sandhya! Shaam ki Badi Khabrein"
    
    news = get_news()
    
    # Sirf news body mein
    body = f"""{news}"""
    
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = subj
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        server.quit()
        print(f"✅ Hinglish email sent successfully at {now.strftime('%I:%M %p')}!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise

if __name__ == "__main__":
    send_email()