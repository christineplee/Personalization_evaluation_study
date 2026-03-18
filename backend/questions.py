"""
Study 2: Content-Specific Personalization -- Dose-Response
16-item minimal set (from Study 1 LASSO), 3 tasks, content questions, eval scales.
All text uses plain ASCII dashes (-) to avoid unicode rendering issues.
"""

PROFILING_QUESTIONS = [
    {"id": "pi_8",  "tier": "primals", "section": "primals", "instrument": "PI-18", "type": "likert6", "text": "No matter where we are or what the topic might be, the world is fascinating.", "anchors": ["Strongly Disagree", "Strongly Agree"]},
    {"id": "pi_16", "tier": "primals", "section": "primals", "instrument": "PI-18", "type": "likert6", "text": "Everything happens for a reason and on purpose.", "anchors": ["Strongly Disagree", "Strongly Agree"]},
    {"id": "pi_6",  "tier": "primals", "section": "primals", "instrument": "PI-18", "type": "likert6", "text": "Most things in life are kind of boring.", "anchors": ["Strongly Disagree", "Strongly Agree"]},
    {"id": "pi_1",  "tier": "primals", "section": "primals", "instrument": "PI-18", "type": "likert6", "text": "In life, there's way more beauty than ugliness.", "anchors": ["Strongly Disagree", "Strongly Agree"]},
    {"id": "pi_12", "tier": "primals", "section": "primals", "instrument": "PI-18", "type": "likert6", "text": "Events seem to lack any cosmic or bigger purpose.", "anchors": ["Strongly Disagree", "Strongly Agree"]},
    {"id": "bfi_20", "tier": "bigfive", "section": "bigfive", "instrument": "BFI-2-S", "type": "likert5", "stem": "I am someone who...", "text": "Has few artistic interests.", "anchors": ["Disagree Strongly", "Agree Strongly"]},
    {"id": "bfi_12", "tier": "bigfive", "section": "bigfive", "instrument": "BFI-2-S", "type": "likert5", "stem": "I am someone who...", "text": "Assumes the best about people.", "anchors": ["Disagree Strongly", "Agree Strongly"]},
    {"id": "bfi_7",  "tier": "bigfive", "section": "bigfive", "instrument": "BFI-2-S", "type": "likert5", "stem": "I am someone who...", "text": "Is sometimes rude to others.", "anchors": ["Disagree Strongly", "Agree Strongly"]},
    {"id": "bfi_24", "tier": "bigfive", "section": "bigfive", "instrument": "BFI-2-S", "type": "likert5", "stem": "I am someone who...", "text": "Feels secure, comfortable with self.", "anchors": ["Disagree Strongly", "Agree Strongly"]},
    {"id": "p2", "tier": "projective", "section": "projective", "text": "Which are you more drawn to?", "type": "forced_choice",
     "options": ["Cooking - improvise, taste, adjust", "Baking - measure precisely, follow the recipe"]},
    {"id": "p5", "tier": "projective", "section": "projective", "text": "When someone pitches you an idea, what do you want to hear first?", "type": "forced_choice",
     "options": ["The concrete details - how it works, what it costs, what the steps are", "The big vision - what it could become and why it matters"]},
    {"id": "p3", "tier": "projective", "section": "projective", "text": "You're lost in an unfamiliar city. Which companion do you prefer?", "type": "forced_choice",
     "options": ["Someone who takes the lead and suggests detours to cool spots", "Someone who waits for you to decide, then helps you get there"]},
    {"id": "i4", "tier": "vignettes", "section": "vignettes", "dimension": "initiative", "type": "bipolar7",
     "text": "You ask the AI for advice about your personal financial situation.",
     "left_anchor": "Flags related concerns or opportunities I might not have thought of",
     "right_anchor": "Only addresses what I specifically asked about"},
    {"id": "s5", "tier": "vignettes", "section": "vignettes", "dimension": "structure", "type": "bipolar7",
     "text": "You're researching an unfamiliar professional field and ask the AI to bring you up to speed.",
     "left_anchor": "Structured outline progressing from fundamentals to advanced topics",
     "right_anchor": "Conversational explanation that builds my understanding organically"},
    {"id": "v4", "tier": "vignettes", "section": "vignettes", "dimension": "verbosity", "type": "bipolar7",
     "text": "You ask the AI about a legal situation you're personally dealing with.",
     "left_anchor": "Brief and focused, just the essentials",
     "right_anchor": "Thorough - covering nuances, exceptions, and implications"},
    {"id": "s2", "tier": "vignettes", "section": "vignettes", "dimension": "structure", "type": "bipolar7",
     "text": "You ask the AI to summarize a complicated situation involving multiple people, events, and factors.",
     "left_anchor": "Organized with clear sections separating each element",
     "right_anchor": "Flowing narrative that tells the story in connected prose"},
]

TASKS = [
    {"id": "task_planning", "category": "planning", "prompt": "I want to start eating healthier but I'm busy and not a great cook. Can you help me plan meals for the week?"},
    {"id": "task_advice", "category": "advice_seeking", "prompt": "I have a friend who I feel like has been pulling away lately. I don't know if I did something wrong or if they're just going through their own stuff. How should I handle this?"},
    {"id": "task_creative", "category": "creative", "prompt": "I need to write a thank-you message to someone who really helped me through a tough time. Can you help me figure out what to say?"},
]

ATTENTION_CHECKS = [
    {"id": "attn_primals", "tier": "primals", "section": "primals", "type": "likert6",
     "text": "To make sure you are reading carefully, please select Strongly Disagree (1) for this item.",
     "anchors": ["Strongly Disagree", "Strongly Agree"],
     "is_attention_check": True, "expected_answer": 1, "insert_after": "pi_6"},
    {"id": "attn_bigfive", "tier": "bigfive", "section": "bigfive", "type": "likert5",
     "stem": "I am someone who...",
     "text": "To show you are reading carefully, please select Agree (4) for this item.",
     "anchors": ["Disagree Strongly", "Agree Strongly"],
     "is_attention_check": True, "expected_answer": 4, "insert_after": "bfi_12"},
    {"id": "attn_eval_1", "type": "eval_attention",
     "text": "This is an attention check. Please select 2 on the scale below.",
     "is_attention_check": True, "expected_answer": 2, "in_task": 1},
    {"id": "attn_eval_2", "type": "eval_attention",
     "text": "Please read carefully and select 6 for this item.",
     "is_attention_check": True, "expected_answer": 6, "in_task": 2},
]

def get_profiling_questions_with_attention_checks():
    questions = list(PROFILING_QUESTIONS)
    profiling_checks = [ac for ac in ATTENTION_CHECKS if ac.get("insert_after")]
    for check in reversed(profiling_checks):
        anchor = check["insert_after"]
        for i, q in enumerate(questions):
            if q["id"] == anchor:
                questions.insert(i + 1, check)
                break
    return questions

CONTENT_QUESTIONS = {
    "task_planning": [
        {"id": "cq_plan_1", "text": "Do you have any dietary restrictions or foods you avoid?",
         "options": ["No restrictions", "Vegetarian or vegan", "Gluten-free or dairy-free", "Religious dietary restrictions (halal, kosher, etc.)", "Other allergies or intolerances"]},
        {"id": "cq_plan_2", "text": "How much time can you realistically spend cooking on a typical weeknight?",
         "options": ["Less than 15 minutes", "15-30 minutes", "30-45 minutes", "I have more time on some nights than others"]},
        {"id": "cq_plan_3", "text": "How many people are you typically cooking for?",
         "options": ["Just myself", "Two people", "A family (3-5 people)", "It varies a lot week to week"]},
        {"id": "cq_plan_4", "text": "Do you prefer variety across the week, or are you okay eating similar meals?",
         "options": ["I want something different every day", "A few base meals with small variations is fine", "I'm happy eating the same thing most days if it's easy"]},
        {"id": "cq_plan_5", "text": "What's your approximate weekly grocery budget for food?",
         "options": ["Under $50", "$50-$100", "$100-$150", "Over $150", "I don't really track it"]},
        {"id": "cq_plan_6", "text": "What cooking equipment do you have easy access to?",
         "options": ["Just basics (stove, oven, microwave)", "I also have a slow cooker or Instant Pot", "I have an air fryer", "I have a well-equipped kitchen"]},
        {"id": "cq_plan_7", "text": "What does 'eating healthier' mean to you right now?",
         "options": ["Eating more vegetables and whole foods", "Cutting back on processed or fast food", "Losing weight or managing calories", "Managing a health condition", "Just generally feeling better and having more energy"]},
        {"id": "cq_plan_8", "text": "Are you open to meal prepping on weekends to save time during the week?",
         "options": ["Yes, I'd love a meal prep plan", "Maybe - an hour or so on Sunday", "Not really, I'd rather cook fresh each day"]},
        {"id": "cq_plan_9", "text": "What types of cuisine do you enjoy most?",
         "options": ["American / comfort food", "Mediterranean / Middle Eastern", "Asian (Chinese, Japanese, Thai, Indian, etc.)", "Latin American / Mexican", "I'm open to anything"]},
        {"id": "cq_plan_10", "text": "What kind of plan would be most useful to you?",
         "options": ["A full weekly plan with recipes and a shopping list", "A few flexible recipe ideas I can mix and match", "Just general guidelines and principles to follow", "Quick grab-and-go options that don't require cooking"]},
    ],
    "task_advice": [
        {"id": "cq_adv_1", "text": "How close is this friendship?",
         "options": ["One of my closest friends", "A good friend but not super close", "More of a casual or newer friend", "A work friend or colleague"]},
        {"id": "cq_adv_2", "text": "How long has this pulling-away feeling been going on?",
         "options": ["A few days", "A few weeks", "A month or more", "It's been gradual over several months"]},
        {"id": "cq_adv_3", "text": "Have you already tried reaching out to them about this?",
         "options": ["No, I haven't said anything yet", "I've tried reaching out casually but got short responses", "I brought it up directly and didn't get a clear answer", "I've been giving them space intentionally"]},
        {"id": "cq_adv_4", "text": "Can you think of a specific event that might have triggered the change?",
         "options": ["Yes - something happened between us", "Maybe - there was an awkward moment but I'm not sure", "No - it seems to have come out of nowhere", "I think they're dealing with something personal unrelated to me"]},
        {"id": "cq_adv_5", "text": "How do you usually handle conflict or tension in relationships?",
         "options": ["I prefer to address things directly and talk it out", "I tend to wait and see if things resolve on their own", "I usually adjust my own behavior first", "I tend to pull away myself when things feel off"]},
        {"id": "cq_adv_6", "text": "What outcome are you hoping for?",
         "options": ["I want to repair and strengthen the friendship", "I want to understand what happened, even if things change", "I want to know if I should move on", "I'm not sure - I just want to handle it well"]},
        {"id": "cq_adv_7", "text": "Has this person gone through any recent life changes that you know of?",
         "options": ["Yes - a major life event (job, health, relationship, move)", "Possibly - they've seemed stressed or busy", "Not that I'm aware of"]},
        {"id": "cq_adv_8", "text": "Is this a pattern that has happened before with this person?",
         "options": ["Yes, they tend to cycle between close and distant", "No, this is unusual for them", "I haven't known them long enough to say"]},
        {"id": "cq_adv_9", "text": "How much emotional energy do you have for this right now?",
         "options": ["I have the bandwidth and want to invest in fixing it", "I care but I'm also dealing with my own stuff", "I'm pretty drained and don't want a big emotional conversation"]},
        {"id": "cq_adv_10", "text": "What kind of advice would be most helpful to you?",
         "options": ["Specific things I could say or do", "Help understanding what might be going on from their side", "Reassurance and perspective on whether this is normal", "A balanced view of all my options"]},
    ],
    "task_creative": [
        {"id": "cq_cre_1", "text": "Who is this thank-you message for?",
         "options": ["A mentor or teacher", "A close friend", "A family member", "A coworker or boss", "A therapist, counselor, or professional"]},
        {"id": "cq_cre_2", "text": "How will you deliver this message?",
         "options": ["A handwritten card or letter", "An email or typed message", "A text message", "I'll say it in person but want to plan what to say"]},
        {"id": "cq_cre_3", "text": "What kind of tough time did they help you through?",
         "options": ["A personal or emotional crisis", "A career or work challenge", "A health issue", "A major life transition (move, breakup, loss)", "I'd rather keep it general and not specify"]},
        {"id": "cq_cre_4", "text": "What did this person specifically do that meant so much?",
         "options": ["They listened without judgment", "They gave me practical help or resources", "They believed in me when I didn't believe in myself", "They were just consistently present and reliable", "A combination of several things"]},
        {"id": "cq_cre_5", "text": "What tone do you want the message to have?",
         "options": ["Warm and heartfelt - I want them to feel my emotion", "Sincere but not overly emotional", "Lighthearted - serious gratitude but with some warmth and humor", "Brief and understated - they'd be uncomfortable with something too emotional"]},
        {"id": "cq_cre_6", "text": "How long should the message be?",
         "options": ["A few sentences - short and meaningful", "A substantial paragraph", "A longer message - I want to really express myself", "I'm not sure, whatever feels right"]},
        {"id": "cq_cre_7", "text": "Is there anything you want to avoid in the message?",
         "options": ["Don't make it too sappy or dramatic", "Don't bring up specific painful details of what I went through", "Don't make it sound like a formal letter", "No particular concerns"]},
        {"id": "cq_cre_8", "text": "What's your relationship like with this person now?",
         "options": ["We're still close and in regular contact", "We've drifted apart but I still care about them", "It's a professional relationship", "We see each other occasionally"]},
        {"id": "cq_cre_9", "text": "Is there a specific occasion prompting this message?",
         "options": ["A birthday, holiday, or milestone", "They recently did something kind again", "No - I just realized I never properly thanked them", "I'm processing things and want to express gratitude as part of that"]},
        {"id": "cq_cre_10", "text": "Would you like the AI to draft the full message, or give you building blocks?",
         "options": ["Write a complete draft I can edit", "Give me a few different options to choose from", "Give me key phrases and an outline I can put together myself"]},
    ],
}

EVALUATION_ITEMS = [
    {"id": "eval_content_fit", "text": "The response addressed my specific situation and needs, not just the general topic."},
    {"id": "eval_personalization", "text": "This response felt like it was written for someone like me, not a generic answer."},
    {"id": "eval_satisfaction", "text": "Overall, I am satisfied with this response."},
    {"id": "eval_effort", "text": "Getting a response that fit my needs felt easy and low-effort."},
]
