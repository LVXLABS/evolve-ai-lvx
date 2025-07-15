@app.route('/generate', methods=['POST'])
def generate():
    from flask import request
    intent = request.form['intent']
    category = request.form['category']
    game_industry = request.form.get('game_industry', '')
    audience = request.form['audience']
    
    # Create detailed, dynamic AI prompt
    prompt = f"""
    You are E-Volve.ai, the premier TikTok strategy expert for LVX Labs and Metafyzical Smart Energy.
    
    USER REQUEST: {intent}
    CATEGORY: {category}
    GAME/INDUSTRY: {game_industry}
    TARGET AUDIENCE: {audience}
    
    Create a UNIQUE, detailed TikTok strategy that includes:
    
    1. VIRAL HOOK (3 different options):
    - Option A: Question-based hook
    - Option B: Shock/surprise hook  
    - Option C: Story-based hook
    
    2. DETAILED 60-SECOND SCRIPT:
    - 0-3s: Hook
    - 3-15s: Problem setup
    - 15-45s: Solution/value
    - 45-60s: CTA + LVX Labs mention
    
    3. VISUAL STRATEGY:
    - Camera angles
    - Transitions
    - Text overlays
    - Background/setting
    
    4. HASHTAG RESEARCH (15 hashtags):
    - 5 trending hashtags
    - 5 niche hashtags for {category}
    - 5 LVX Labs branded hashtags
    
    5. POSTING OPTIMIZATION:
    - Best time for {audience}
    - Caption strategy
    - Comment seeding ideas
    
    6. ENGAGEMENT TACTICS:
    - How to respond to comments
    - Cross-platform promotion
    - Community building tips
    
    7. METAFYZICAL SMART ENERGY INTEGRATION:
    - Natural product mentions
    - Energy/focus angle
    - Gaming performance benefits
    
    Make this strategy SPECIFIC to the request and completely unique each time.
    """
    
    try:
        if client and openai_available:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are E-Volve.ai, an expert TikTok strategist for LVX Labs. Create detailed, unique strategies every time."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.8  # Higher creativity
            )
            strategy = response.choices[0].message.content
        else:
            # Enhanced fallback with more variety
            strategy = create_dynamic_template(intent, category, game_industry, audience)
    except Exception as e:
        strategy = create_dynamic_template(intent, category, game_industry, audience)
    
    return f'''[same styling as before with strategy content]'''

def create_dynamic_template(intent, category, game_industry, audience):
    import random
    
    hooks = [
        f"Stop scrolling! This {category} secret will blow your mind...",
        f"POV: You're about to discover the {category} hack everyone's hiding...",
        f"Why is nobody talking about this {category} strategy?",
        f"I tried this {category} method for 30 days and here's what happened..."
    ]
    
    # More dynamic content based on inputs
    return f"""🎯 CUSTOM E-VOLVE.AI STRATEGY FOR: {intent}

{random.choice(hooks)}

[Rest of dynamic template with variations]"""

