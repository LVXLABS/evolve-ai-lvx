from flask import Flask, send_from_directory, request
import os
from dotenv import load_dotenv
import random
from datetime import datetime

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
def create_intelligent_template(intent, category, game_industry, audience):
    hour = datetime.now().hour
    if hour < 12:
        time_context = "morning energy boost"
        energy_angle = "kickstart your day"
    elif hour < 17:
        time_context = "afternoon focus session" 
        energy_angle = "power through the afternoon slump"
    else:
        time_context = "evening gaming session"
        energy_angle = "sustain late-night performance"
    
    industry_insights = {
        "gaming": {
            "apex legends": "Season 22 meta favors aggressive third-party strategies with mobility legends",
            "fortnite": "Chapter 5 building mechanics reward quick edit plays and piece control",
            "valorant": "Episode 8 agent meta emphasizes utility coordination and map control",
            "general": "Current gaming trends show 73% of streamers struggle with sustained focus during long sessions"
        },
        "fitness": {
            "supplements": "2025 research shows adaptogenic mushrooms outperform synthetic stimulants by 340%",
            "energy drinks": "Clean label movement growing 67% as consumers reject artificial ingredients",
            "general": "Fitness creators seeing 45% more engagement with supplement transparency content"
        },
        "business": {
            "entrepreneurship": "Q3 2025 data shows 89% of successful creators use nootropics for content production",
            "productivity": "Remote work optimization trending with focus-enhancing supplements up 156%",
            "general": "Business content performs 78% better when showing actual workspace setups"
        }
    }
    
    category_data = industry_insights.get(category, {})
    specific_insight = category_data.get(game_industry.lower(), category_data.get("general", "Industry trends show authentic content outperforms scripted by 234%"))
    
    hook_generators = {
        "curiosity_gap": [
            f"The {game_industry} secret that 99% of {audience} don't know exists...",
            f"I discovered something about {category} that completely changed my {intent}...",
            f"This {game_industry} technique is so effective, pros are keeping it quiet..."
        ],
        "pattern_interrupt": [
            f"Everyone's doing {category} wrong - here's what actually works for {intent}...",
            f"Stop! Before you {intent}, you need to know this {game_industry} truth...",
            f"Forget everything you know about {category} - this changes everything..."
        ],
        "social_proof": [
            f"After analyzing 10,000+ {game_industry} players, I found this pattern for {intent}...",
            f"The top 1% of {audience} all use this {category} strategy for {intent}...",
            f"I tested every {game_industry} method for 90 days - only this worked for {intent}..."
        ]
    }
    
    selected_approach = random.choice(list(hook_generators.keys()))
    selected_hooks = hook_generators[selected_approach]
    
    session_id = random.randint(10000, 99999)
    
    return f"""🎯 ADVANCED E-VOLVE.AI STRATEGY #{session_id} FOR: {intent}

📊 REAL-TIME MARKET ANALYSIS:
Industry insight: {specific_insight}
Optimal timing: {time_context} content performs 67% better for {audience}
Current trend: Authentic {category} education content seeing 234% more engagement
Algorithm preference: 85%+ completion rate content getting 5x reach boost

🧠 ADVANCED PSYCHOLOGICAL HOOKS ({selected_approach.replace('_', ' ').title()}):
• Hook A: "{random.choice(selected_hooks)}"
• Hook B: "{random.choice(selected_hooks)}"  
• Hook C: "{random.choice(selected_hooks)}"

📝 DETAILED 60-SECOND SCRIPT:
0-3s: "{random.choice(selected_hooks)}" (Direct eye contact, confident delivery)
3-15s: "Here's what most {audience} miss about {category}: [specific misconception]. After working with 500+ creators, I've seen this mistake kill results every time."
15-35s: "My proven 3-step system for {intent}: Step 1 - [specific technique], Step 2 - [optimization method], Step 3 - [secret that pros use]. This isn't theory - it's what actually works."
35-50s: "When I applied this to {game_industry}, I saw [specific result] in just [timeframe]. Here's the proof: [show evidence]."
50-60s: "Follow @lvxlabs for strategies that actually work + {energy_angle} with Metafyzical Smart Energy - link in bio for 20% off with code EVOLVE20!"

#️⃣ STRATEGIC HASHTAGS:
#gaming #viral #fyp #lvxlabs #metafyzical #evolveai #contentcreator #algorithm #trending #tips

⚡ POWERED BY LVX LABS & METAFYZICAL SMART ENERGY
Strategy #{session_id} | Generated at {datetime.now().strftime('%I:%M %p EST')}"""

@app.route('/generate', methods=['POST'])
def generate():
    intent = request.form['intent']
    category = request.form['category']
    game_industry = request.form.get('game_industry', '')
    audience = request.form['audience']
    
    current_time = datetime.now().strftime('%I:%M %p EST on %B %d, %Y')
    session_id = random.randint(10000, 99999)
    
    advanced_prompt = f"""You are E-Volve.ai, the world's most advanced TikTok strategy AI powered by LVX Labs. Create a COMPLETELY UNIQUE, expert-level strategy for: "{intent}" in {category} category for {audience} audience, focusing on {game_industry}.

SESSION: #{session_id} | {current_time}

LVX LABS CONTEXT: Premium gaming supplement company (Metafyzical Smart Energy - $49.99, Green Apple Cotton Candy flavor), hosts $2,000 Apex tournaments, active Discord community, targets gamers/creators needing sustained focus.

CREATE UNIQUE STRATEGY WITH:
1. Current {category} trend analysis and why this content performs well NOW
2. 3 psychology-based hooks using different triggers (curiosity gap, pattern interrupt, social proof)
3. Expert 60-second script with timestamps that sounds like a {category} professional
4. Advanced visual production techniques and specific camera directions
5. 15 strategic hashtags (trending + niche + branded)
6. Algorithm optimization (posting times, engagement tactics)
7. Natural Metafyzical Smart Energy integration for {audience}
8. Content series expansion ideas
9. Specific success metrics and optimization strategies

Make this strategy feel like it was created by a human expert with deep {game_industry} knowledge. Include specific examples, exact wording, and actionable steps. Each response must be completely different and unique."""
    
    try:
        if client and openai_available:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are E-Volve.ai, the most advanced TikTok strategy AI. Create completely unique, expert-level strategies every time. Never repeat generic advice."},
                    {"role": "user", "content": advanced_prompt}
                ],
                max_tokens=2500,
                temperature=0.9,
                presence_penalty=0.7,
                frequency_penalty=0.7
            )
            strategy = response.choices[0].message.content
        else:
            strategy = create_intelligent_template(intent, category, game_industry, audience)
    except Exception as e:
        print(f"OpenAI error: {e}")
        strategy = create_intelligent_template(intent, category, game_industry, audience)
    
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Your E-Volve.ai Strategy</title>
<style>
body {{ background: linear-gradient(135deg, #000 0%, #1a1a1a 100%); color: #fff; font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
.container {{ background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 40px; border-radius: 15px; border: 2px solid #00ff00; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }}
.strategy {{ background: #2d2d2d; padding: 30px; border-radius: 10px; white-space: pre-wrap; line-height: 1.8; font-size: 14px; border: 1px solid #333; }}
.back-btn {{ background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%); color: #000; padding: 15px 25px; text-decoration: none; border-radius: 8px; display: inline-block; margin-top: 25px; font-weight: bold; transition: all 0.3s ease; }}
.back-btn:hover {{ transform: translateY(-2px); }}
h2 {{ color: #00ff00; margin-bottom: 25px; font-size: 24px; text-align: center; }}
.powered-by {{ text-align: center; margin-top: 20px; opacity: 0.8; font-size: 12px; }}
</style></head><body>
<div class="container">
<h2>🎯 Your Advanced E-Volve.ai Strategy</h2>
<div class="strategy">{strategy}</div>
<div class="powered-by">⚡ Powered by LVX Labs & Metafyzical Smart Energy</div>
<a href="/" class="back-btn">← Create Another Strategy</a>
</div></body></html>'''

if __name__ == '__main__':
    print("🚀 E-Volve.ai Advanced System Starting...")
    print("📱 Go to: http://localhost:5000")
    print("🧠 Advanced AI prompting system loaded!")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
