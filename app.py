from flask import Flask, send_from_directory, request
import os
from dotenv import load_dotenv
import random

load_dotenv()
app = Flask(__name__)

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    openai_available = True
except Exception as e:
    print(f"OpenAI not available: {e}")
    client = None
    openai_available = False

@app.route('/manifest.json')
def manifest():
    return {
        "name": "E-Volve.ai - LVX Labs",
        "short_name": "E-Volve.ai",
        "description": "AI-Powered TikTok Strategy Generator by LVX Labs",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#000000",
        "theme_color": "#00ff00",
        "orientation": "portrait",
        "icons": [
            {"src": "/static/icon-192.jpg", "sizes": "192x192", "type": "image/jpeg"},
            {"src": "/static/icon-512.jpg", "sizes": "512x512", "type": "image/jpeg"}
        ]
    }

@app.route('/sw.js')
def service_worker():
    return '''const CACHE_NAME = 'evolve-ai-v1';
const urlsToCache = ['/', '/static/icon-192.jpg', '/static/icon-512.jpg'];
self.addEventListener('install', function(event) {
    event.waitUntil(caches.open(CACHE_NAME).then(function(cache) { return cache.addAll(urlsToCache); }));
});
self.addEventListener('fetch', function(event) {
    event.respondWith(caches.match(event.request).then(function(response) {
        if (response) { return response; }
        return fetch(event.request);
    }));
});''', 200, {'Content-Type': 'application/javascript'}

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>E-Volve.ai - LVX Labs</title><link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#00ff00"><meta name="apple-mobile-web-app-capable" content="yes">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #000 0%, #1a1a1a 100%); min-height: 100vh; padding: 10px; color: #fff; }
.container { max-width: 500px; margin: 0 auto; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); overflow: hidden; border: 2px solid #00ff00; }
.header { background: linear-gradient(135deg, #000 0%, #1a1a1a 100%); padding: 30px 20px; text-align: center; border-bottom: 3px solid #00ff00; }
.header h1 { font-size: 2.2em; margin-bottom: 5px; font-weight: 700; color: #00ff00; }
.form-container { padding: 30px 20px; }
.form-group { margin-bottom: 25px; }
label { display: block; margin-bottom: 8px; font-weight: 600; color: #fff; font-size: 1.1em; }
input, select, textarea { width: 100%; padding: 15px; border: 2px solid #333; border-radius: 12px; font-size: 16px; background: #000; color: #fff; }
input:focus, select:focus, textarea:focus { border-color: #00ff00; outline: none; background: #1a1a1a; }
.generate-btn { background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%); color: #000; padding: 18px 30px; border: none; border-radius: 15px; font-size: 18px; font-weight: 700; cursor: pointer; width: 100%; }
</style></head><body>
<div class="container">
<div class="header"><h1>E-Volve.ai</h1><div>Powered by LVX Labs • Metafyzical Smart Energy</div></div>
<div class="form-container">
<form action="/generate" method="post">
<div class="form-group">
<label>💡 What content do you want to create?</label>
<textarea name="intent" placeholder="e.g., Apex Legends ranked tips, promoting Metafyzical Smart Energy" rows="3" required></textarea>
</div>
<div class="form-group">
<label>📱 Content Category</label>
<select name="category" required>
<option value="">Choose Category</option>
<option value="gaming">🎮 Gaming</option>
<option value="fitness">💪 Fitness & Health</option>
<option value="lifestyle">✨ Lifestyle</option>
<option value="business">💼 Business</option>
<option value="product">⚡ Product Promotion</option>
</select>
</div>
<div class="form-group">
<label>🎯 Specific Game/Industry (Optional)</label>
<input type="text" name="game_industry" placeholder="e.g., Apex Legends, Supplements">
</div>
<div class="form-group">
<label>👥 Target Audience</label>
<select name="audience" required>
<option value="">Choose Audience</option>
<option value="gamers">🎮 Gamers (18-35)</option>
<option value="fitness">💪 Fitness Enthusiasts</option>
<option value="entrepreneurs">💼 Entrepreneurs</option>
<option value="students">📚 Students</option>
<option value="general">🌟 General (18-35)</option>
</select>
</div>
<button type="submit" class="generate-btn">⚡ Generate Strategy</button>
</form></div></div></body></html>'''

def create_dynamic_template(intent, category, game_industry, audience):
    hooks = [
        f"Stop scrolling! This {category} secret will blow your mind...",
        f"POV: You're about to discover the {category} hack everyone's hiding...",
        f"Why is nobody talking about this {category} strategy?",
        f"I tried this {category} method for 30 days and here's what happened...",
        f"This {category} tip got me 100K views in 24 hours..."
    ]
    
    hashtags = {
        "gaming": "#gaming #gamer #twitch #streamer #esports #apexlegends #fps #ranked #tips #viral #fyp #lvxlabs #metafyzical",
        "fitness": "#fitness #workout #health #nutrition #supplements #energy #focus #gains #motivation #fyp #lvxlabs #metafyzical",
        "business": "#entrepreneur #business #success #mindset #productivity #focus #energy #hustle #growth #tips #fyp #lvxlabs",
        "lifestyle": "#lifestyle #motivation #selfcare #productivity #energy #focus #wellness #tips #viral #fyp #lvxlabs #metafyzical",
        "product": "#product #review #energy #supplements #health #focus #gaming #performance #viral #fyp #lvxlabs #metafyzical"
    }
    
    selected_hashtags = hashtags.get(category, "#tips #viral #fyp #trending #motivation #lvxlabs #metafyzical")
    
    return f"""🎯 CUSTOM E-VOLVE.AI STRATEGY FOR: {intent}

🎬 VIRAL HOOK OPTIONS:
• Option A: {random.choice(hooks)}
• Option B: {random.choice(hooks)}
• Option C: {random.choice(hooks)}

📝 60-SECOND SCRIPT BREAKDOWN:
0-3s: Hook - {random.choice(hooks)}
3-15s: Problem - "Here's what most {audience} get wrong about {category}..."
15-45s: Solution - Your {intent} approach with specific examples
45-60s: CTA - "Follow @lvxlabs for more {category} strategies + try Metafyzical Smart Energy for sustained focus!"

📱 VISUAL STRATEGY:
• Start with close-up face shot for hook
• Quick cuts every 2-3 seconds
• Show {game_industry} gameplay/examples if applicable
• Use text overlays for key points
• End with clear LVX Labs branding

#️⃣ OPTIMIZED HASHTAGS:
{selected_hashtags}

⏰ OPTIMAL POSTING TIME:
7-9 PM EST (peak {audience} activity)

🔥 ENGAGEMENT TACTICS:
• Ask question in caption to boost comments
• Pin comment with additional tips
• Respond to all comments quickly
• Cross-promote in Discord community

💪 METAFYZICAL INTEGRATION:
"Fuel your {category} content creation with Metafyzical Smart Energy - clean, sustained focus without the crash!"

⚡ POWERED BY LVX LABS & METAFYZICAL SMART ENERGY"""

@app.route('/generate', methods=['POST'])
def generate():
    intent = request.form['intent']
    category = request.form['category']
    game_industry = request.form.get('game_industry', '')
    audience = request.form['audience']
    
    try:
        if client and openai_available:
            prompt = f"""You are E-Volve.ai, TikTok strategist for LVX Labs. Create a UNIQUE strategy for: {intent}, Category: {category}, Industry: {game_industry}, Audience: {audience}. Include: 3 viral hooks, detailed 60s script, visual strategy, 15 hashtags, posting time, engagement tactics, and natural Metafyzical Smart Energy mentions."""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.8
            )
            strategy = response.choices[0].message.content
        else:
            strategy = create_dynamic_template(intent, category, game_industry, audience)
    except Exception as e:
        strategy = create_dynamic_template(intent, category, game_industry, audience)
    
    return f'''<style>body{{background:#000;color:#fff;font-family:Arial;max-width:1000px;margin:0 auto;padding:20px}}.container{{background:#1a1a1a;padding:30px;border-radius:10px;border:2px solid #00ff00}}.strategy{{background:#2d2d2d;padding:20px;border-radius:8px;white-space:pre-wrap;line-height:1.6}}.back-btn{{background:#00ff00;color:#000;padding:10px 20px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:20px}}h2{{color:#00ff00;margin-bottom:20px}}</style><div class="container"><h2>🎯 Your E-Volve.ai Strategy</h2><div class="strategy">{strategy}</div><a href="/" class="back-btn">← Create Another Strategy</a></div>'''

if __name__ == '__main__':
    app.run(debug=True)
