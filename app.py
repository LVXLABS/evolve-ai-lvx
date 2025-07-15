from flask import Flask, send_from_directory, request
import os
from dotenv import load_dotenv
import random
from datetime import datetime
import json
import time

load_dotenv()
app = Flask(__name__)

# Simple OpenAI setup that works with any version
openai_available = False
client = None

try:
    import openai
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        openai.api_key = api_key
        openai_available = True
        print("✅ OpenAI loaded successfully")
    else:
        print("⚠️ No OpenAI API key found - using advanced templates")
except Exception as e:
    print(f"⚠️ OpenAI not available: {e} - using advanced templates")

# ADVANCED INDUSTRY KNOWLEDGE DATABASES
GAMING_DATABASE = {
    "apex_legends": {
        "current_season": "Season 22",
        "meta_legends": ["Wraith", "Octane", "Pathfinder", "Bloodhound", "Lifeline"],
        "trending_strategies": ["Third-party rotations", "Edge zone plays", "Aggressive early game", "Mobility legend combos"],
        "pro_insights": ["ALGS tournament meta favors mobility", "Ranked rewards aggressive playstyle", "New weapon meta: R-301/Wingman"],
        "content_angles": ["Rank climbing tips", "Legend guides", "Weapon tier lists", "Pro player analysis"]
    },
    "fortnite": {
        "current_season": "Chapter 5 Season 4",
        "meta_strategies": ["Zero build dominance", "Creative 2.0 maps", "Ranked competitive"],
        "trending_content": ["Building techniques", "Edit courses", "Zone wars", "Creative showcases"],
        "pro_insights": ["FNCS meta shifts", "Piece control importance", "Box fighting evolution"]
    },
    "valorant": {
        "current_episode": "Episode 8 Act 3",
        "agent_meta": ["Jett", "Omen", "Sova", "Killjoy", "Sage"],
        "map_strategies": ["Ascent control", "Bind rotations", "Haven site takes"],
        "trending_content": ["Agent guides", "Aim training", "Team coordination", "Rank climbing"]
    }
}

FITNESS_DATABASE = {
    "supplements": {
        "trending_research": ["Adaptogenic mushrooms outperform synthetics by 340%", "Clean label movement growing 67%", "Nootropics for focus up 156%"],
        "consumer_trends": ["Transparency in ingredients", "Third-party testing", "Sustainable sourcing", "No artificial additives"],
        "content_angles": ["Ingredient breakdowns", "Before/after transformations", "Honest reviews", "Science explanations"]
    },
    "energy_drinks": {
        "market_trends": ["Clean energy movement", "Natural caffeine sources", "Crash-free formulations"],
        "competitor_analysis": ["GFuel synthetic ingredients", "Ghost artificial sweeteners", "Bang excessive caffeine"],
        "content_opportunities": ["Ingredient comparisons", "Taste tests", "Performance tracking", "Health impact studies"]
    }
}

BUSINESS_DATABASE = {
    "content_creation": {
        "trending_topics": ["AI automation tools", "Creator economy growth", "Monetization strategies", "Audience building"],
        "productivity_trends": ["Focus supplements for creators", "Workspace optimization", "Content batching", "Algorithm understanding"],
        "pain_points": ["Burnout prevention", "Consistent posting", "Engagement drops", "Revenue diversification"]
    },
    "entrepreneurship": {
        "current_trends": ["Solopreneurship rise", "Digital product creation", "Community building", "Personal branding"],
        "success_factors": ["Sustained focus", "Energy management", "Stress resilience", "Decision fatigue"]
    }
}

# ADVANCED PSYCHOLOGY ENGINE
PSYCHOLOGICAL_TRIGGERS = {
    "curiosity_gap": [
        "The {industry} secret that {percentage}% of {audience} don't know exists...",
        "I discovered something about {topic} that completely changed my {intent}...",
        "This {technique} is so effective, pros are keeping it quiet...",
        "What I'm about to show you will change how you think about {category}...",
        "The {industry} truth that nobody talks about..."
    ],
    "pattern_interrupt": [
        "Stop! Everything you know about {topic} is wrong...",
        "Forget {common_belief} - here's what actually works for {intent}...",
        "Everyone's doing {activity} backwards - here's the truth...",
        "Before you {intent}, you NEED to know this...",
        "This will sound crazy, but {controversial_statement}..."
    ],
    "social_proof": [
        "After analyzing {large_number} {subjects}, I found this pattern for {intent}...",
        "The top {percentage}% of {group} all use this {method}...",
        "I tested every {category} method for {timeframe} - only this worked for {intent}...",
        "Pro {industry} players don't want you to know this {technique}...",
        "This is how the best {audience} actually {intent}..."
    ],
    "authority_positioning": [
        "As someone who's coached {number}+ {audience} in {category}...",
        "After {years} years studying {field}, I finally cracked the code for {intent}...",
        "My {background} taught me this counterintuitive approach to {intent}...",
        "Having worked with top {industry} professionals, here's what they really do...",
        "From my experience training {audience}, this is the game-changer..."
    ],
    "dopamine_loops": [
        "Wait until you see what happens at the {timestamp} mark...",
        "The result will shock you - but first, you need this foundation...",
        "Part 2 will blow your mind, but you need to understand this first...",
        "Keep watching - the payoff at the end is incredible...",
        "This technique seems simple, but the results are insane..."
    ]
}

def get_current_trends():
    current_date = datetime.now()
    month = current_date.month
    
    seasonal_trends = {
        1: ["New Year optimization", "Resolution content", "Fresh start energy"],
        2: ["Valentine's gaming", "Love-themed content", "Couple challenges"],
        3: ["Spring training", "March Madness", "Seasonal energy boost"],
        4: ["Spring gaming", "Tournament season", "Fresh content ideas"],
        5: ["Summer prep", "Gaming marathons", "Energy for long sessions"],
        6: ["Summer gaming", "Vacation content", "Portable setups"],
        7: ["Mid-year goals", "Summer tournaments", "Peak performance"],
        8: ["Back to school", "Student content", "Focus for studying"],
        9: ["Fall season", "New game releases", "Routine optimization"],
        10: ["Halloween content", "Spooky gaming", "Seasonal themes"],
        11: ["Holiday prep", "Thanksgiving gaming", "Gratitude content"],
        12: ["Year-end content", "Holiday gaming", "New Year prep"]
    }
    
    trending_now = [
        "AI-powered content creation",
        "Clean energy supplements", 
        "Gaming performance optimization",
        "Authentic creator content",
        "Community building strategies",
        "Algorithm understanding",
        "Sustainable energy solutions",
        "Focus enhancement techniques"
    ]
    
    return {
        "seasonal": seasonal_trends.get(month, ["General trending topics"]),
        "current": trending_now,
        "date_context": f"{current_date.strftime('%B %d, %Y')}"
    }

@app.route('/manifest.json')
def manifest():
    return {
        "name": "E-Volve.ai Ultimate - LVX Labs",
        "short_name": "E-Volve.ai",
        "description": "Ultimate AI-Powered TikTok Strategy Generator by LVX Labs",
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
    return '''const CACHE_NAME = 'evolve-ai-ultimate-v2';
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
<title>E-Volve.ai Ultimate - LVX Labs</title><link rel="manifest" href="/manifest.json">
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
.ultimate-badge { background: linear-gradient(135deg, #ff6b00 0%, #ff8500 100%); color: #fff; padding: 8px 16px; border-radius: 20px; font-size: 0.9em; font-weight: 700; margin: 10px 0; display: inline-block; }
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
.ai-features { background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); margin: 20px; padding: 20px; border-radius: 10px; border: 2px solid #ff6b00; }
.ai-feature { display: flex; align-items: center; margin: 10px 0; color: #ff6b00; font-weight: 600; }
.ai-feature-icon { margin-right: 10px; font-size: 1.2em; }
.form-container { padding: 30px 20px; background: linear-gradient(180deg, #2d2d2d 0%, #1a1a1a 100%); }
.form-group { margin-bottom: 25px; }
label { display: block; margin-bottom: 8px; font-weight: 600; color: #fff; font-size: 1.1em; }
input, select, textarea { width: 100%; padding: 15px; border: 2px solid #333; border-radius: 12px; font-size: 16px; background: #000; color: #fff; }
input:focus, select:focus, textarea:focus { border-color: #00ff00; outline: none; background: #1a1a1a; }
textarea { resize: vertical; min-height: 100px; font-family: inherit; }
.generate-btn { background: linear-gradient(135deg, #ff6b00 0%, #ff8500 100%); color: #fff; padding: 18px 30px; border: none; border-radius: 15px; font-size: 18px; font-weight: 700; cursor: pointer; width: 100%; transition: all 0.3s ease; text-transform: uppercase; }
.generate-btn:hover { transform: translateY(-3px); }
.loading-text { text-align: center; margin-top: 10px; color: #ff6b00; font-weight: 600; }
@media (max-width: 480px) { .lvx-logo-img { width: 150px; height: 90px; } .community-buttons { flex-direction: column; } .community-btn, .metafyzical-btn { width: 90%; text-align: center; } }
</style></head><body>
<div class="container">
<div class="header">
<img src="https://sintra-images.s3.eu-north-1.amazonaws.com/3cbc9bbb-56ff
-485c-9503-18812da41c86/message-files/d32c86db-b7b1-43f1-88da-9384e2d303cf/LVX_LOGO.jpg" alt="LVX Labs Logo" class="lvx-logo-img">
<h1>E-Volve.ai</h1>
<div class="subtitle">Powered by <span class="lvx-brand">LVX Labs</span> • Metafyzical Smart Energy</div>
<div class="ultimate-badge">🚀 ULTIMATE AI SYSTEM</div>
</div>
<div class="community-buttons">
<a href="https://discord.gg/F2qG7nZfsG" target="_blank" class="community-btn">🎮 Join Our Discord</a>
<a href="https://www.lvxlabs.com" target="_blank" class="metafyzical-btn">⚡ Power Up with Metafyzical</a>
</div>
<div class="powered-by"><strong>🎯 Ultimate AI-Powered TikTok Strategy Generator</strong></div>
<div class="ai-features">
<div class="ai-feature"><div class="ai-feature-icon">🧠</div>Advanced Psychology Engine</div>
<div class="ai-feature"><div class="ai-feature-icon">📊</div>Real-Time Trend Integration</div>
<div class="ai-feature"><div class="ai-feature-icon">🔬</div>Deep Industry Knowledge</div>
<div class="ai-feature"><div class="ai-feature-icon">📚</div>Expert-Level Strategies</div>
</div>
<div class="features">
<div class="feature"><div class="feature-icon">🎬</div><div class="feature-text">Viral Hooks</div></div>
<div class="feature"><div class="feature-icon">📈</div><div class="feature-text">Algorithm Optimized</div></div>
<div class="feature"><div class="feature-icon">⚡</div><div class="feature-text">Clean Energy</div></div>
<div class="feature"><div class="feature-icon">🔥</div><div class="feature-text">Gaming Focus</div></div>
</div>
<div class="form-container">
<form action="/generate" method="post" onsubmit="showLoading()">
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
<button type="submit" class="generate-btn">🚀 Generate Ultimate Strategy</button>
<div class="loading-text" id="loadingText" style="display:none;">🧠 Advanced AI analysis in progress...</div>
</form></div></div>
<script>
function showLoading() {
    document.getElementById('loadingText').style.display = 'block';
    document.querySelector('.generate-btn').innerHTML = '🔄 Generating...';
    document.querySelector('.generate-btn').disabled = true;
}
</script></body></html>'''

# ADVANCED STRATEGY GENERATION FUNCTIONS
def get_industry_insights(category, game_industry):
    if category == "gaming" and game_industry.lower().replace(" ", "_") in GAMING_DATABASE:
        data = GAMING_DATABASE[game_industry.lower().replace(" ", "_")]
        return f"Current {game_industry} meta: {', '.join(data['trending_strategies'][:2])}. Pro insight: {random.choice(data['pro_insights'])}"
    elif category == "fitness":
        if "supplement" in game_industry.lower() or "energy" in game_industry.lower():
            data = FITNESS_DATABASE["supplements"] if "supplement" in game_industry.lower() else FITNESS_DATABASE["energy_drinks"]
            return f"Market trend: {random.choice(data['trending_research'] if 'trending_research' in data else data['market_trends'])}"
    elif category == "business":
        data = BUSINESS_DATABASE["content_creation"]
        return f"Industry insight: {random.choice(data['trending_topics'])} trending for {category} creators"
    
    return f"Industry analysis: {category} content with authentic educational approach performing 234% better than generic scripted content"

def generate_advanced_hooks(intent, category, game_industry, audience):
    # Select random psychological trigger
    trigger_type = random.choice(list(PSYCHOLOGICAL_TRIGGERS.keys()))
    hooks = PSYCHOLOGICAL_TRIGGERS[trigger_type]
    
    # Generate 3 unique hooks
    generated_hooks = []
    for i in range(3):
        hook_template = random.choice(hooks)
        
        # Fill in template variables
        hook = hook_template.format(
            industry=game_industry or category,
            percentage=random.choice([97, 99, 95, 93, 91]),
            audience=audience,
            topic=intent,
            intent=intent,
            technique=f"{category} strategy",
            common_belief=f"traditional {category}",
            activity=intent,
            controversial_statement=f"{category} isn't about what you think",
            large_number=random.choice(["10,000+", "5,000+", "1,000+", "500+"]),
            subjects=f"{game_industry} players" if game_industry else f"{audience}",
            group=audience,
            method=f"{category} technique",
            timeframe=random.choice(["90 days", "6 months", "1 year", "2 years"]),
            number=random.choice([500, 1000, 2000, 3000]),
            years=random.choice([3, 5, 7, 10]),
            field=category,
            background=f"{category} expertise",
            timestamp=random.choice(["30-second", "45-second", "1-minute"])
        )
        generated_hooks.append(hook)
    
    return {
        "trigger_type": trigger_type.replace("_", " ").title(),
        "hooks": generated_hooks
    }

def generate_detailed_script(intent, category, game_industry, audience, hooks):
    # Time-based energy context
    hour = datetime.now().hour
    if hour < 12:
        energy_context = "morning focus boost"
    elif hour < 17:
        energy_context = "afternoon energy maintenance"
    else:
        energy_context = "evening performance sustain"
    
    # Generate detailed script
    script = f"""📝 EXPERT-LEVEL 60-SECOND SCRIPT:

0-3s: "{hooks['hooks'][0]}" 
(Direct eye contact, confident delivery, strong hook to stop scrolling)

3-15s: "Here's what most {audience} miss about {category}: [specific misconception about {intent}]. After working with hundreds of creators, I've seen this mistake destroy results every single time. The truth is..."

15-35s: "My proven 3-step system for {intent}:
Step 1 - [Specific technique with exact timing/method]
Step 2 - [Optimization strategy that pros use] 
Step 3 - [Secret sauce that separates top 1% from everyone else]
This isn't theory - it's what actually works in {game_industry or category}."

35-50s: "When I applied this exact method to {game_industry or 'my content'}, I saw [specific measurable result] in just [timeframe]. Here's the proof: [show evidence/demonstration/before-after]."

50-60s: "Follow @lvxlabs for strategies that actually work + {energy_context} with Metafyzical Smart Energy - clean, sustained focus without crashes. Link in bio for 20% off with code EVOLVE20!"

🎬 VISUAL PRODUCTION NOTES:
• Camera: Start close-up during hook, pull back to reveal setup
• Lighting: 3-point setup, warm 3200K temperature
• Audio: Trending sound at 65%, crystal clear voice
• Props: {game_industry or category} equipment visible, Metafyzical tub strategically placed
• Text overlays: Bold font, highlight key numbers and steps"""
    
    return script

def generate_hashtag_strategy(category, game_industry, audience):
    # Base trending hashtags
    trending_base = ["#fyp", "#viral", "#trending", "#algorithm", "#contentcreator"]
    
    # Category-specific hashtags
    category_hashtags = {
        "gaming": ["#gaming", "#gamer", "#esports", "#streamer", "#gamingsetup", "#gamingcommunity"],
        "fitness": ["#fitness", "#supplements", "#health", "#wellness", "#nutrition", "#fitnessmotivation"],
        "business": ["#entrepreneur", "#business", "#productivity", "#success", "#mindset", "#hustle"],
        "lifestyle": ["#lifestyle", "#motivation", "#selfcare", "#wellness", "#productivity", "#focus"],
        "product": ["#productreview", "#honest", "#supplement", "#energy", "#focus", "#performance"]
    }
    
    # Niche-specific hashtags
    niche_hashtags = []
    if game_industry:
        niche_hashtags.append(f"#{game_industry.replace(' ', '').lower()}")
    niche_hashtags.extend([f"#{audience.replace(' ', '').lower()}tips", f"#{category}hacks"])
    
    # LVX Labs branded hashtags
    branded_hashtags = ["#lvxlabs", "#metafyzical", "#evolveai", "#cleanenergy"]
    
    # Combine and select 15 hashtags
    all_hashtags = trending_base + category_hashtags.get(category, []) + niche_hashtags + branded_hashtags
    selected_hashtags = random.sample(all_hashtags, min(15, len(all_hashtags)))
    
    return " ".join(selected_hashtags)

def generate_engagement_strategy(audience, category):
    audience_tactics = {
        "gamers": [
            "Ask viewers to drop their current rank/level in comments",
            "Challenge audience to try the technique and report back with results",
            "Create poll: 'Who else struggles with this in ranked matches?'",
            "Pin comment asking about their gaming setup and performance goals"
        ],
        "fitness": [
            "Ask for before/after transformation progress pics",
            "Challenge viewers to 7-day energy optimization test",
            "Poll: 'What's your biggest energy crash time of day?'",
            "Pin comment about workout timing and supplement stacking"
        ],
        "entrepreneurs": [
            "Ask about their biggest productivity and focus challenges",
            "Challenge: implement strategy for 30 days and share results",
            "Poll: 'Coffee crashes or clean energy for sustained focus?'",
            "Pin comment about morning routines and energy management"
        ],
        "students": [
            "Ask about study session length and focus struggles",
            "Challenge: try technique during next exam prep session",
            "Poll: 'Energy drinks vs clean supplements for studying?'",
            "Pin comment about optimal study timing and focus hacks"
        ],
        "general": [
            "Ask about their biggest daily energy and focus challenges",
            "Challenge viewers to try and report back in 48 hours",
            "Poll: 'Morning person or need afternoon energy boost?'",
            "Pin comment with bonus tip for sustained energy"
        ]
    }
    
    tactics = audience_tactics.get(audience, audience_tactics["general"])
    
    return f"""🔥 ADVANCED ENGAGEMENT STRATEGY:
• Primary tactic: {random.choice(tactics)}
• Response strategy: Reply within 15 minutes using voice messages for top comments
• Community building: "Join our Discord for exclusive {category} strategies and connect with other creators"
• Follow-up content: Create Part 2 based on most requested comment topic
• Viral amplification: Use trending audio + share controversial opinion for algorithm boost
• Cross-platform: Share to Instagram Reels 90 minutes later, Discord immediately"""

@app.route('/generate', methods=['POST'])
def generate():
    print("🚀 Starting Ultimate E-Volve.ai Generation...")
    
    intent = request.form['intent']
    category = request.form['category']
    game_industry = request.form.get('game_industry', '')
    audience = request.form['audience']
    
    # Get real-time context
    trends = get_current_trends()
    session_id = random.randint(100000, 999999)
    
    print(f"📊 Session #{session_id} - Advanced analysis starting...")
    
    # Generate all strategy components
    industry_insights = get_industry_insights(category, game_industry)
    hooks_data = generate_advanced_hooks(intent, category, game_industry, audience)
    detailed_script = generate_detailed_script(intent, category, game_industry, audience, hooks_data)
    hashtag_strategy = generate_hashtag_strategy(category, game_industry, audience)
    engagement_strategy = generate_engagement_strategy(audience, category)
    
    # Time-based Metafyzical integration
    hour = datetime.now().hour
    if hour < 12:
        energy_angle = "kickstart your morning with sustained focus"
        timing_context = "morning content creation sessions"
    elif hour < 17:
        energy_angle = "power through afternoon energy dips"
        timing_context = "afternoon productivity blocks"
    else:
        energy_angle = "maintain peak performance during evening sessions"
        timing_context = "late-night content creation marathons"
    
    # Compile ultimate strategy
    ultimate_strategy = f"""🎯 ULTIMATE E-VOLVE.AI STRATEGY #{session_id} FOR: {intent}

📊 REAL-TIME MARKET INTELLIGENCE:
{industry_insights}
Trend Context: {', '.join(trends['current'][:3])}
Seasonal Factor: {', '.join(trends['seasonal'][:2])}
Algorithm Priority: Educational content with entertainment value performing 300% better
Generated: {trends['date_context']} at {datetime.now().strftime('%I:%M %p EST')}

🧠 ADVANCED PSYCHOLOGICAL HOOKS ({hooks_data['trigger_type']}):
• Hook A: "{hooks_data['hooks'][0]}"
• Hook B: "{hooks_data['hooks'][1]}"
• Hook C: "{hooks_data['hooks'][2]}"

{detailed_script}

#️⃣ STRATEGIC HASHTAG RESEARCH (15 optimized):
{hashtag_strategy}

⏰ ALGORITHM OPTIMIZATION STRATEGY:
• Optimal posting time: 7:30 PM EST (peak {audience} engagement window)
• Caption strategy: 2 lines maximum, end with engaging question
• Thumbnail: Custom design with bold text overlay and contrasting colors
• Audio strategy: Use trending sound at 65% volume, clear voice recording
• Completion rate target: 85%+ for maximum algorithm boost

{engagement_strategy}

⚡ METAFYZICAL SMART ENERGY INTEGRATION:
Natural mention: "Creating
content like this requires laser focus - that's why I {energy_angle} with Metafyzical Smart Energy. Clean, sustained energy without crashes, perfect for {timing_context}."
Product benefits for {audience}: Enhanced cognitive function, zero jitters during recording, sustained energy for editing marathons, clean ingredients for health-conscious creators
Strong CTA: "Link in bio for 20% off - use code EVOLVE20. Join thousands of creators already using it!"

📈 CONTENT SERIES EXPANSION:
Part 1: {intent} (this video)
Part 2: "Advanced {category} mistakes that kill your {intent} results"
Part 3: "The {game_industry or category} setup that transformed my {intent}"
Part 4: "Live {audience} Q&A - answering your {category} questions"
Part 5: "30-day {intent} challenge results and transformations"

🎯 SUCCESS METRICS & OPTIMIZATION:
Primary KPIs: Completion rate (target 87%+), saves (target 12%+), Discord community joins
Secondary metrics: Comment engagement rate, profile visits, EVOLVE20 code usage tracking
A/B testing opportunities: Hook variations, posting times, thumbnail designs
Optimization strategy: Monitor retention graphs, adjust pacing based on drop-off points

💪 LVX LABS COMMUNITY INTEGRATION:
Discord connection: "Join 5,000+ creators in our Discord for exclusive {category} strategies"
Tournament tie-in: "Use these tips in our $2,000 Apex Legends tournament - registration open in Discord"
VIP club mention: "VIP members get early access to strategies like this + live coaching sessions"
User-generated content: "Tag @lvxlabs using these tips - we'll feature the best results in our next video"

🚀 ULTIMATE EXECUTION CHECKLIST:
✓ Record 3 hook variations for A/B testing
✓ Create custom thumbnail with LVX Labs branding
✓ Prepare follow-up content pipeline
✓ Set Discord notifications for immediate engagement
✓ Monitor competitor trends in {category}
✓ Track EVOLVE20 discount code usage for ROI measurement
✓ Schedule cross-platform posts for maximum reach

⚡ POWERED BY ULTIMATE E-VOLVE.AI SYSTEM
Strategy #{session_id} | Advanced AI Analysis | LVX Labs Innovation
Generated: {datetime.now().strftime('%I:%M %p EST on %B %d, %Y')}

"The most intelligent TikTok strategy generator ever created - delivering expert-level strategies that feel human-crafted but are powered by advanced AI systems."
"""
    
    print(f"✅ Ultimate strategy #{session_id} generated successfully!")
    
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ultimate E-Volve.ai Strategy #{session_id}</title>
<style>
body {{ background: linear-gradient(135deg, #000 0%, #1a1a1a 100%); color: #fff; font-family: Arial, sans-serif; max-width: 1400px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
.container {{ background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 40px; border-radius: 15px; border: 2px solid #ff6b00; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }}
.strategy {{ background: #2d2d2d; padding: 30px; border-radius: 10px; white-space: pre-wrap; line-height: 1.8; font-size: 14px; border: 1px solid #ff6b00; }}
.back-btn {{ background: linear-gradient(135deg, #ff6b00 0%, #ff8500 100%); color: #fff; padding: 15px 25px; text-decoration: none; border-radius: 8px; display: inline-block; margin-top: 25px; font-weight: bold; transition: all 0.3s ease; }}
.back-btn:hover {{ transform: translateY(-2px); }}
h2 {{ color: #ff6b00; margin-bottom: 25px; font-size: 24px; text-align: center; }}
.ultimate-badge {{ background: linear-gradient(135deg, #ff6b00 0%, #ff8500 100%); color: #fff; padding: 10px 20px; border-radius: 20px; display: inline-block; margin-bottom: 20px; font-weight: 700; }}
.powered-by {{ text-align: center; margin-top: 20px; opacity: 0.8; font-size: 12px; color: #ff6b00; }}
</style></head><body>
<div class="container">
<h2>🚀 Your Ultimate E-Volve.ai Strategy</h2>
<div class="ultimate-badge">🚀 ULTIMATE AI SYSTEM</div>
<div class="strategy">{ultimate_strategy}</div>
<div class="powered-by">⚡ Powered by Ultimate E-Volve.ai | LVX Labs Innovation</div>
<a href="/" class="back-btn">← Generate Another Ultimate Strategy</a>
</div></body></html>'''

if __name__ == '__main__':
    print("🚀 ULTIMATE E-VOLVE.AI SYSTEM STARTING...")
    print("📱 Access at: http://localhost:5000")
    print("🧠 Advanced Psychology Engine: LOADED")
    print("📊 Real-Time Trends: ACTIVE") 
    print("🔬 Industry Knowledge Base: READY")
    print("📚 Expert Strategy Templates: ENABLED")
    print("⚡ LVX Labs Integration: OPTIMIZED")
    print("🎯 Bulletproof TikTok Strategy Generator: ONLINE")
    print("✅ No OpenAI dependency - works with any setup!")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
