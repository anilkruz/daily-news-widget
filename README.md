# 🌍 Daily News Widget - Duniya Ka Halchal

Personal automated daily email newsletter in **Hinglish** style – subah 8:30 AM aur shaam 9:30 PM IST pe world ka latest halchal (focused on major news jaise US-Israel-Iran war, markets, crypto, India angle, Bengaluru weather) Gmail pe direct bhejta hai. Widget jaisa clean format with emojis, sections, aur images for quick read.

Perfect for someone jo Himalayan 450 pe Bengaluru roads pe ride karte time quick world update chahta hai! 🏍️🔥

![News Widget Illustration](https://thumbs.dreamstime.com/b/modern-thin-line-design-concept-news-website-banner-vector-illustration-product-services-information-recent-66374716.jpg)
*(Modern news summary widget vibe – crisp & engaging)*

## Features
- **Daily 2 Emails**: Morning (8:30 AM IST) update + Evening Roundup (9:30 PM IST) with day summary.
- **Focused News**: War (US-Israel-Iran), global headlines, India angle (Holi vibes, markets), crypto (BTC beast mode), Bengaluru weather for rides.
- **Sources**: NewsAPI.org (Reuters, BBC, Al Jazeera, CNN, WaPo etc. – reliable only).
- **Format**: Emojis, bold sections, short paras – Gmail mein widget feel.
- **Automated**: GitHub Actions se schedule (no local Mac dependency).
- **Secure**: Gmail App Password + GitHub Secrets.

![Himalayan 450 Ride](https://cdpcdn.dx1app.com/products/USA/RE/2025/MC/DUALPURP/HIMALAYAN_450/50/SLATE_POPPY_BLUE/2000000017.jpg)
*(Royal Enfield Himalayan 450 – Bengaluru traffic mein safe ride kar bhai!)*

## Setup Instructions (Quick Start)

1. **NewsAPI Key Le Le**  
   https://newsapi.org/ pe sign up → Free API key copy kar.

2. **Gmail App Password Bana** (Normal password nahi chalega)  
   Google Account > Security > 2-Step Verification on → App passwords > Generate for "Mail" → Copy 16-char code.

3. **GitHub Repo Secrets Add Kar**  
   Repo > Settings > Secrets and variables > Actions > New repository secret:  
   - `NEWS_API_KEY`  
   - `EMAIL_SENDER` (yourgmail@gmail.com)  
   - `EMAIL_PASSWORD` (App Password)

4. **Code Structure**  
   - `news_email.py`: Main script (News fetch + email send).  
   - `.github/workflows/daily-news.yml`: GitHub Actions workflow (cron jobs for 8:30 AM & 9:30 PM IST).

5. **Run Manually (Test)**  
   GitHub > Actions tab > "Daily News Widget Email" > Run workflow (main branch).

6. **Cron Schedules (UTC)**  
   - 03:00 UTC → 8:30 AM IST  
   - 16:00 UTC → 9:30 PM IST

## Customize Karna Chahe To
- News query change: `news_email.py` mein `q=US+Israel+Iran+war` ko tweak kar (e.g., add `crypto` ya `India`).
- HTML email bana (better image embed): MIMEHTML add kar sakte hain.
- More sections: Sports, tech, petrol prices – bol de add kar dete hain.

## Current War Context (March 2026)
US-Israel vs Iran escalation full on – Tehran strikes, death toll 1,000+, oil prices volatile, BTC holding strong ~$72k. Stay updated, petrol daam watch karna padega Bengaluru mein bhi.

![War Headlines Dramatic](https://media-cldnry.s-nbcnews.com/image/upload/c_fill,g_auto,w_2500,h_1667/rockcms/2026-03/260303-beirut-2-rs-0a5b08.jpg)
*(Middle East conflict smoke over city – tension high hai bhai)*

Bhai, ride safe on that Himalayan 450 – traffic + heat combo careful rakhna. Koi tweak chahiye README mein ya script mein, bata de. Ab repo live hai, Actions chal rahe honge daily! 🔥

Made with love in Bengaluru 🇮🇳🏍️
