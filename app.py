from flask import Flask, send_from_directory
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except Exception as e:
    print(f"OpenAI client error: {e}")
    client = None


@app.route('/generate', methods=['POST'])
def generate():
    from flask import request
    intent = request.form['intent']
    category = request.form['category']
    game_industry = request.form.get('game_industry', '')
    audience = request.form['audience']
    
    # Fallback strategy if OpenAI client fails
    if client is None:
        strategy = f"""
🎯 E-Volve.ai Strategy for {intent}

🎬 KILLER HOOK (0-3 seconds):
"Stop scrolling! This {category} tip will change everything..."

📝 SCRIPT OUTLINE:
- Hook: Grab attention with bold claim
- Problem: Address common {audience} pain point
- Solution: Your {intent} approach
- Proof: Quick example or result
- CTA: "Follow for more {category} tips!"

📱 VISUAL INSTRUCTIONS:
- Start with close-up face shot
- Quick cuts every 2-3 seconds
- Show {game_industry} gameplay/examples
- End with clear branding

#️⃣ HASHTAGS:
#{category} #{audience} #tips #viral #fyp #trending

⏰ OPTIMAL POSTING TIME:
7-9 PM EST (peak {audience} activity)

🔥 ENGAGEMENT TACTICS:
- Ask question in caption
- Pin comment with follow-up
- Respond to all comments quickly

💪 CALL-TO-ACTION:
"Join our Discord for exclusive {category} strategies!"
        """
    else:
        # Try OpenAI first
        try:
            prompt = f"You are E-Volve.ai, a TikTok strategist for LVX Labs. Create a strategy for: {intent}, Category: {category}, Industry: {game_industry}, Audience: {audience}. Include: 1. Hook 2. Script 3. Hashtags 4. Timing 5. Engagement tactics"
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            strategy = response.choices[0].message.content
        except Exception as e:
            # Fallback to template
            strategy = f"""
🎯 E-Volve.ai Strategy for {intent}

🎬 KILLER HOOK (0-3 seconds):
"Stop scrolling! This {category} tip will change everything..."

📝 SCRIPT OUTLINE:
- Hook: Grab attention with bold claim
- Problem: Address common {audience} pain point  
- Solution: Your {intent} approach
- Proof: Quick example or result
- CTA: "Follow for more {category} tips!"

📱 VISUAL INSTRUCTIONS:
- Start with close-up face shot
- Quick cuts every 2-3 seconds
- Show {game_industry} gameplay/examples
- End with clear branding

#️⃣ HASHTAGS:
#{category} #{audience} #tips #viral #fyp #trending

⏰ OPTIMAL POSTING TIME:
7-9 PM EST (peak {audience} activity)

🔥 ENGAGEMENT TACTICS:
- Ask question in caption
- Pin comment with follow-up
- Respond to all comments quickly

💪 CALL-TO-ACTION:
"Join our Discord for exclusive {category} strategies!"
            """
    
    return f'''<style>body{{background:#000;color:#fff;font-family:Arial;max-width:1000px;margin:0 auto;padding:20px}}.container{{background:#1a1a1a;padding:30px;border-radius:10px;border:2px solid #00ff00}}.strategy{{background:#2d2d2d;padding:20px;border-radius:8px;white-space:pre-wrap;line-height:1.6}}.back-btn{{background:#00ff00;color:#000;padding:10px 20px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:20px}}h2{{color:#00ff00;margin-bottom:20px}}</style><div class="container"><h2>🎯 Your E-Volve.ai Strategy</h2><div class="strategy">{strategy}</div><a href="/" class="back-btn">← Create Another Strategy</a></div>'''

def home():
    return '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>E-Volve.ai - LVX Labs</title>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#00ff00">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="E-Volve.ai">
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
.install-prompt { background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%); color: #000; padding: 15px; margin: 20px; border-radius: 10px; text-align: center; font-weight: 700; cursor: pointer; display: none; }
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
</style>
</head>
<body>
<div class="container">
<div class="header">
<img src="https://sintra-images.s3.eu-north-1.amazonaws.com/3cbc9bbb-56ff-485c-9503-18812da41c86/message-files/d32c86db-b7b1-43f1-88da-9384e2d303cf/LVX_LOGO.jpg" alt="LVX Labs Logo" class="lvx-logo-img">
<h1>E-Volve.ai</h1>
<div class="subtitle">Powered by <span class="lvx-brand">LVX Labs</span> • Metafyzical Smart Energy</div>
</div>
<div class="install-prompt" id="installPrompt">📱 Install E-Volve.ai App - Tap to Download!</div>
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
</form>
</div>
</div>
<script>
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
}
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    document.getElementById('installPrompt').style.display = 'block';
});
document.getElementById('installPrompt').addEventListener('click', () => {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            deferredPrompt = null;
            document.getElementById('installPrompt').style.display = 'none';
        });
    }
});
</script>
</body></html>'''

@app.route('/generate', methods=['POST'])
def generate():
    from flask import request
    intent = request.form['intent']
    category = request.form['category']
    game_industry = request.form.get('game_industry', '')
    audience = request.form['audience']
    
    prompt = f"You are E-Volve.ai, a TikTok strategist for LVX Labs. Create a strategy for: {intent}, Category: {category}, Industry: {game_industry}, Audience: {audience}. Include: 1. Hook 2. Script 3. Hashtags 4. Timing 5. Engagement tactics"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        strategy = response.choices[0].message.content
        return f'''<style>body{{background:#000;color:#fff;font-family:Arial;max-width:1000px;margin:0 auto;padding:20px}}.container{{background:#1a1a1a;padding:30px;border-radius:10px;border:2px solid #00ff00}}.strategy{{background:#2d2d2d;padding:20px;border-radius:8px;white-space:pre-wrap;line-height:1.6}}.back-btn{{background:#00ff00;color:#000;padding:10px 20px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:20px}}h2{{color:#00ff00;margin-bottom:20px}}</style><div class="container"><h2>🎯 Your E-Volve.ai Strategy</h2><div class="strategy">{strategy}</div><a href="/" class="back-btn">← Create Another Strategy</a></div>'''
    except Exception as e:
        return f'<div style="background:#1a1a1a;color:#fff;padding:20px;text-align:center;"><h2 style="color:#ff0000;">Error</h2><p>{str(e)}</p><a href="/" style="background:#00ff00;color:#000;padding:10px 20px;text-decoration:none;border-radius:5px;">← Try Again</a></div>'

if __name__ == '__main__':
    print("🚀 E-Volve.ai PWA is starting up...")
    print("📱 Go to: http://localhost:5000")
    app.run(debug=True)
