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
<link rel="apple-touch-icon" href="/static/icon-192.jpg">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #000 0%, #1a1a1a 100%); min-height: 100vh; padding: 10px; color: #fff; }
.container { max-width: 500px; margin: 0 auto; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); overflow: hidden; border: 2px solid #00ff00; }
.header { background: linear-gradient(135deg, #000 0%, #1a1a1a 100%); padding: 30px 20px; text-align: center; border-bottom: 3px solid #00ff00; }
.lvx-logo-img { width: 200px; height: 120px; margin-bottom: 15px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,255,0,0.4); object-fit: contain; background: white; padding: 10px; }
.header h1 { font-size: 2.2em; margin-bottom: 5px; font-weight: 700; color: #00ff00; }
.header .subtitle { font-size: 1.1em; opacity: 0.9; color: #fff; }
.lvx-brand { color: #00ff00; font-weight: 800; }
.community-buttons { display: flex; gap: 10px; justify-content: center; margin: 20px; flex-wrap: wrap; }
.community-btn { background: linear-gradient(135deg, #5865F2 0%, #4752C4 100%); color: white; padding: 12px 20px; text-decoration: none; border-radius: 10px; font-weight: 600; transition: all 0.3s ease; }
.metafyzical-btn { background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%); color: #000; padding: 12px 20px; text-decoration: none; border-radius: 10px; font-weight: 600; transition: all 0.3s ease; }
.community-btn:hover, .metafyzical-btn:hover { transform: translateY(-2px); }
.powered-by { background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%); padding: 15px; margin: 20px; border-radius: 10px; text-align: center; font-weight: 700; color: #000; }
.features { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin: 20px; }
.feature { background: linear-gradient(135deg, #000 0%, #1a1a1a 100%); padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #333; transition: all 0.3s ease; }
.feature:hover { border-color: #00ff00; transform: translateY(-3px); }
.feature-icon { font-size: 1.5em; margin-bottom: 5px; color: #00ff00; }
.feature-text { font-size: 0.9em; font-weight: 600; color: #fff; }
.form-container { padding: 30px 20px; background: linear-gradient(180deg, #2d2d2d 0%, #1a1a1a 100%); }
.form-group { margin-bottom: 25px; }
label { display: block; margin-bottom: 8px; font-weight: 600; color: #fff; font-size: 1.1em; }
input, select, textarea { width: 100%; padding: 15px; border: 2px solid #333; border-radius: 12px; font-size: 16px; background: #000; color: #fff; }
input:focus, select:focus, textarea:focus { border-color: #00ff00; outline: none; background: #1a1a1a; }
textarea { resize: vertical; min-height: 100px; font-family: inherit; }
.generate-btn { background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%); color: #000; padding: 18px 30px; border: none; border-radius: 15px; font-size: 18px; font-weight: 700; cursor: pointer; width: 100%; transition: all 0.3s ease; text-transform: uppercase; }
.generate-btn:hover { transform: translateY(-3px); }
@media (max-width: 480px) { .lvx-logo-img { width: 150px; height: 90px; } .community-buttons { flex-direction: column; } .community-btn, .metafyzical-btn { width: 90%; text-align: center; } }
</style></head><body>
<div class="container">
<div class="header">
<img src="https://sintra-images.s3.eu-north-1.amazonaws.com/3cbc9bbb-56ff-485c-9503-18812da41c86/message-files/d32c86db-b7b1-43f1-88da-9384e2d303cf/LVX_LOGO.jpg" alt="LVX Labs Logo" class="lvx-logo-img">
<h1>E-Volve.ai</h1>
<div class="subtitle">Powered by <span class="lvx-brand">LVX Labs</span> • Metafyzical Smart Energy</div>
</div>
<div class="community-buttons">
<a href="https://discord.gg/F2qG7nZfsG" target="_blank" class="community-btn">🎮 Join Our Discord</a>
<a href="https://www.lvxlabs.com" target="_blank" class="metafyzical-btn">⚡ Power Up with Metafyzical</a>
</div>
<div class="powered-by"><strong>🎯 AI-Powered TikTok Strategy Generator</strong></div>
<div class="features">
<div class="feature"><div class="feature-icon">🎬</div><div class="feature-text">Viral Hooks</div></div>
<div class="feature"><div class="feature-icon">📈</div><div class="feature-text">Algorithm Optimized</div></div>
<div class="feature"><div class="feature-icon">⚡</div><div class="feature-text">Clean Energy</div></div>
<div class="feature"><div class="feature-icon">🔥</div><div class="feature-text">Gaming Focus</div></div>
</div>
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
<input type="text" name="game_industry" placeholder="e.g., Apex Legends, Supplements, Energy Drinks">
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
def create_advanced_template(intent, category, game_industry, audience):
    hooks_db = {
        "gaming": [
            f"The {game_industry} mistake that's costing you wins",
            f"Why pro {game_industry} players hide this strategy",
            f"I analyzed 1000 {game_industry} matches - found this pattern",
            f"This {game_industry} setting changed everything",
            f"The {game_industry} meta everyone's sleeping on"
        ],
        "fitness": [
            f"The supplement industry doesn't want you to know this",
            f"Why your pre-workout is making you weaker",
            f"I tested every energy drink for 30 days",
            f"This workout mistake kills your gains",
            f"The nutrition secret pros don't share"
        ],
        "product": [
            f"This {game_industry} product changed my setup",
            f"Why most {audience} waste money on supplements",
            f"I spent $500 testing energy drinks",
            f"The product that transformed my performance",
            f"This supplement hack saves you money"
        ]
    }
    
    selected_hooks = hooks_db.get(category, [
        f"The {category} secret that changed everything",
        f"Why everyone's doing {category} wrong",
        f"This {category} hack got me 500K views"
    ])
    
    return f"""🎯 ADVANCED E-VOLVE.AI STRATEGY FOR: {intent}

🧠 PSYCHOLOGY-BASED VIRAL HOOKS:
• Hook A: "{random.choice(selected_hooks)}..."
• Hook B: "{random.choice(selected_hooks)}..."
• Hook C: "{random.choice(selected_hooks)}..."

📝 DETAILED 60-SECOND SCRIPT:
0-3s: "{random.choice(selected_hooks)}..."
3-15s: "Most {audience} think {category} is about X, but I discovered it's actually about Y..."
15-35s: "Here's my exact 3-step method for {intent}: [Step 1], [Step 2], [Step 3]"
35-50s: "When I applied this to {game_industry}, I saw [specific result]..."
50-60s: "Follow @lvxlabs + fuel your focus with Metafyzical Smart Energy!"

#️⃣ HASHTAGS: #gaming #viral #fyp #lvxlabs #metafyzical #evolveai

⚡ POWERED BY LVX LABS & METAFYZICAL SMART ENERGY"""

@app.route('/generate', methods=['POST'])
def generate():
    intent = request.form['intent']
    category = request.form['category']
    game_industry = request.form.get('game_industry', '')
    audience = request.form['audience']
    
    advanced_prompt = f"""You are E-Volve.ai, the world's most advanced TikTok strategy AI powered by LVX Labs. Create a COMPLETELY UNIQUE, detailed strategy for: "{intent}" in {category} category for {audience} audience, focusing on {game_industry}.

CONTEXT: LVX Labs makes Metafyzical Smart Energy ($49.99, Green Apple Cotton Candy flavor), hosts $2,000 Apex tournaments, has active Discord community, targets gamers/creators who need sustained focus.

Include: 3 psychology-based hooks, detailed 60s script with timestamps, visual strategy, 15 strategic hashtags, posting optimization, engagement tactics, natural Metafyzical integration, content series ideas, success metrics. Make this strategy specific, actionable, and completely different each time."""
    
    try:
        if client and openai_available:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are E-Volve.ai, the most advanced TikTok strategy AI. Create completely unique, detailed strategies every time."},
                    {"role": "user", "content": advanced_prompt}
                ],
                max_tokens=2500,
                temperature=0.9,
                presence_penalty=0.6,
                frequency_penalty=0.6
            )
            strategy = response.choices[0].message.content
        else:
            strategy = create_advanced_template(intent, category, game_industry, audience)
    except Exception as e:
        strategy = create_advanced_template(intent, category, game_industry, audience)
    
    return f'''<style>body{{background:#000;color:#fff;font-family:Arial;max-width:1200px;margin:0 auto;padding:20px;line-height:1.6}}.container{{background:#1a1a1a;padding:40px;border-radius:15px;border:2px solid #00ff00}}.strategy{{background:#2d2d2d;padding:30px;border-radius:10px;white-space:pre-wrap;line-height:1.8;font-size:14px}}.back-btn{{background:#00ff00;color:#000;padding:15px 25px;text-decoration:none;border-radius:8px;display:inline-block;margin-top:25px;font-weight:bold}}h2{{color:#00ff00;margin-bottom:25px;font-size:24px}}</style><div class="container"><h2>🎯 Your Advanced E-Volve.ai Strategy</h2><div class="strategy">{strategy}</div><a href="/" class="back-btn">← Create Another Strategy</a></div>'''

if __name__ == '__main__':
    print("🚀 E-Volve.ai is starting up...")
    print("📱 Go to: http://localhost:5000")
    app.run(debug=True)
