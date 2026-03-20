"""
Study 2: Content-Specific Personalization -- Dose-Response
16-item minimal set, 8 tasks (participants choose 3), content questions, eval scales.
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

# All 8 tasks from Study 1. Participants choose 3.
TASKS = [
    {"id": "task_advice", "category": "advice_seeking",
     "prompt": "I have a friend who I feel like has been pulling away lately. I don't know if I did something wrong or if they're just going through their own stuff. How should I handle this?",
     "short_label": "Navigating a friendship that's fading"},
    {"id": "task_explain", "category": "explanation",
     "prompt": "I always feel tired even when I get a full night's sleep. Why does that happen, and what can I actually do about it?",
     "short_label": "Understanding persistent tiredness"},
    {"id": "task_emotional", "category": "emotional",
     "prompt": "I had a really frustrating day at work - I kept sharing ideas in a meeting and they were either ignored or someone else got credit for them. What do you think I should do?",
     "short_label": "Dealing with being overlooked at work"},
    {"id": "task_planning", "category": "planning",
     "prompt": "I want to start eating healthier but I'm busy and not a great cook. Can you help me plan meals for the week?",
     "short_label": "Planning healthier meals on a busy schedule"},
    {"id": "task_creative", "category": "creative",
     "prompt": "I need to write a thank-you message to someone who really helped me through a tough time. Can you help me figure out what to say?",
     "short_label": "Writing a meaningful thank-you message"},
    {"id": "task_recommendation", "category": "recommendation",
     "prompt": "I want to pick up a new hobby but I have no idea where to start. I've got a few hours a week and a modest budget. Any suggestions?",
     "short_label": "Finding a new hobby"},
    {"id": "task_howto", "category": "technical",
     "prompt": "I have to give a short presentation at work next week and I'm nervous about public speaking. How should I prepare?",
     "short_label": "Preparing for a nerve-wracking presentation"},
    {"id": "task_ambiguous", "category": "value_laden",
     "prompt": "I've been feeling like I have no work-life balance lately. Everything blurs together and I'm always either working or thinking about work. How do people actually deal with this?",
     "short_label": "Struggling with work-life balance"},
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


# Content questions for all 8 tasks. 10 per task, nested (P3 sees Q1-3, etc.)
# The 3 original tasks have LLM-generated questions.
# The 5 new tasks have PLACEHOLDERS - run generate_content_questions.py to replace.

CONTENT_QUESTIONS = {
    "task_advice": [
        {
            "id": "cq_advice_1",
            "text": "How long have you noticed your friend pulling away?",
            "options": [
                "A few days",
                "A few weeks",
                "A few months",
                "I'm not sure"
            ]
        },
        {
            "id": "cq_advice_2",
            "text": "How often do you and your friend typically communicate?",
            "options": [
                "Daily",
                "A few times a week",
                "A few times a month",
                "Rarely"
            ]
        },
        {
            "id": "cq_advice_3",
            "text": "What kind of response are you hoping for from your friend?",
            "options": [
                "Reassurance that everything is okay",
                "A deeper conversation about their feelings",
                "An opportunity to apologize if needed",
                "I'm not sure yet"
            ]
        },
        {
            "id": "cq_advice_4",
            "text": "How comfortable are you with directly asking your friend if something is wrong?",
            "options": [
                "Very comfortable",
                "Somewhat comfortable",
                "Not very comfortable",
                "Not comfortable at all"
            ]
        },
        {
            "id": "cq_advice_5",
            "text": "Have there been any recent changes in your friend's life that could be affecting them?",
            "options": [
                "Yes, something significant happened",
                "Maybe, but I'm not sure",
                "No, not that I know of",
                "I haven't thought about it"
            ]
        },
        {
            "id": "cq_advice_6",
            "text": "What's the main priority for you in handling this situation?",
            "options": [
                "Maintaining the friendship",
                "Understanding what's going on",
                "Resolving any potential issues",
                "Giving them space if needed"
            ]
        },
        {
            "id": "cq_advice_7",
            "text": "Do you prefer handling sensitive situations like this in person or remotely?",
            "options": [
                "In person",
                "Over the phone",
                "Through text or messaging",
                "It depends on the situation"
            ]
        },
        {
            "id": "cq_advice_8",
            "text": "Have you communicated with your friend about this concern before?",
            "options": [
                "Yes, we've discussed it",
                "No, I haven't brought it up yet",
                "I've hinted at it but not directly",
                "I'm not sure how to approach it"
            ]
        },
        {
            "id": "cq_advice_9",
            "text": "Do you think your friend might need space or support right now?",
            "options": [
                "They might need space",
                "They might need support",
                "I'm not sure what they need",
                "I don't think this applies"
            ]
        },
        {
            "id": "cq_advice_10",
            "text": "How do you typically handle conflicts or misunderstandings in friendships?",
            "options": [
                "By discussing it openly",
                "By giving it time to resolve naturally",
                "By seeking advice or support from others",
                "I try to avoid direct confrontation"
            ]
        }
    ],
    "task_explain": [
        {
            "id": "cq_explain_1",
            "text": "How long have you been experiencing this tiredness?",
            "options": [
                "Less than a week",
                "1-4 weeks",
                "1-6 months",
                "More than 6 months"
            ]
        },
        {
            "id": "cq_explain_2",
            "text": "Do you usually feel tired at specific times of the day?",
            "options": [
                "Morning",
                "Afternoon",
                "Evening",
                "All day"
            ]
        },
        {
            "id": "cq_explain_3",
            "text": "How many hours of sleep do you typically get per night?",
            "options": [
                "Less than 4 hours",
                "4-6 hours",
                "6-8 hours",
                "More than 8 hours"
            ]
        },
        {
            "id": "cq_explain_4",
            "text": "Do you have any known medical conditions that might affect your energy levels?",
            "options": [
                "Yes, and they are diagnosed",
                "Yes, but they are undiagnosed",
                "No, not to my knowledge",
                "Prefer not to disclose"
            ]
        },
        {
            "id": "cq_explain_5",
            "text": "What kind of advice would be most helpful to you?",
            "options": [
                "Lifestyle changes (e.g., diet, exercise)",
                "Sleep improvement tips",
                "Stress management techniques",
                "Medical advice or when to consult a doctor"
            ]
        },
        {
            "id": "cq_explain_6",
            "text": "Are there any constraints you face in making lifestyle changes?",
            "options": [
                "Time constraints",
                "Financial limitations",
                "Physical limitations",
                "No major constraints"
            ]
        },
        {
            "id": "cq_explain_7",
            "text": "Do you have a specific goal related to your energy levels?",
            "options": [
                "Feel more alert during work or study",
                "Have more energy for physical activities",
                "Improve overall well-being",
                "Not sure yet"
            ]
        },
        {
            "id": "cq_explain_8",
            "text": "Do you use any tools or apps to track your sleep or energy levels?",
            "options": [
                "Yes, regularly",
                "Yes, occasionally",
                "No, but I'm open to it",
                "No, and I'm not interested"
            ]
        },
        {
            "id": "cq_explain_9",
            "text": "How much detail do you prefer in the AI's response?",
            "options": [
                "A brief summary",
                "A balanced explanation with some detail",
                "A fully detailed response",
                "Depends on the topic"
            ]
        },
        {
            "id": "cq_explain_10",
            "text": "Have you already tried anything to improve your energy levels?",
            "options": [
                "Yes, and it helped",
                "Yes, but it didn't help",
                "No, I haven't tried anything yet",
                "Prefer not to say"
            ]
        }
    ],
    "task_emotional": [
        {
            "id": "cq_emotional_1",
            "text": "Who were the people involved in the meeting where your ideas were ignored?",
            "options": [
                "My manager or supervisor",
                "Colleagues at my level",
                "A mix of managers and colleagues",
                "External stakeholders or clients"
            ]
        },
        {
            "id": "cq_emotional_2",
            "text": "How often do situations like this occur for you in meetings?",
            "options": [
                "This is the first time",
                "Occasionally, but not often",
                "Fairly regularly",
                "Almost every meeting"
            ]
        },
        {
            "id": "cq_emotional_3",
            "text": "What do you want to achieve by addressing this situation?",
            "options": [
                "I want my ideas to be recognized",
                "I want to improve communication dynamics",
                "I want to feel respected and valued",
                "I'm not sure yet, I just want to vent"
            ]
        },
        {
            "id": "cq_emotional_4",
            "text": "How comfortable are you with directly addressing this issue with the people involved?",
            "options": [
                "Very comfortable",
                "Somewhat comfortable",
                "Not very comfortable",
                "Not comfortable at all"
            ]
        },
        {
            "id": "cq_emotional_5",
            "text": "What kind of ideas were you trying to share in the meeting?",
            "options": [
                "Creative or innovative suggestions",
                "Process or workflow improvements",
                "Team or project updates",
                "Other types of ideas"
            ]
        },
        {
            "id": "cq_emotional_6",
            "text": "What would be your preferred way of receiving advice on this situation?",
            "options": [
                "Specific actionable steps",
                "General guidance and encouragement",
                "A mix of both",
                "I'm open to any type of advice"
            ]
        },
        {
            "id": "cq_emotional_7",
            "text": "Who do you think is most responsible for the issue you faced in the meeting?",
            "options": [
                "The people ignoring my ideas",
                "The person taking credit for my ideas",
                "Both equally",
                "I'm not sure"
            ]
        },
        {
            "id": "cq_emotional_8",
            "text": "How do you usually handle situations where you feel frustrated at work?",
            "options": [
                "I address it directly with the people involved",
                "I talk to someone I trust for advice",
                "I try to let it go and move on",
                "I haven't figured out a consistent approach"
            ]
        },
        {
            "id": "cq_emotional_9",
            "text": "What kind of work culture are you part of?",
            "options": [
                "Collaborative and supportive",
                "Competitive and high-pressure",
                "Neutral or mixed",
                "I'm not sure how to describe it"
            ]
        },
        {
            "id": "cq_emotional_10",
            "text": "What's the most important outcome you'd like from advice on this issue?",
            "options": [
                "Better communication skills",
                "Stronger recognition of my contributions",
                "Improved confidence in sharing ideas",
                "A way to move past the frustration"
            ]
        }
    ],
    "task_planning": [
        {
            "id": "cq_planning_1",
            "text": "How many meals per day would you like help planning?",
            "options": [
                "1 meal per day",
                "2 meals per day",
                "3 meals per day",
                "Only dinners",
                "It varies day to day"
            ]
        },
        {
            "id": "cq_planning_2",
            "text": "Do you have any dietary restrictions or preferences?",
            "options": [
                "None",
                "Vegetarian",
                "Vegan",
                "Gluten-free",
                "Other (e.g., allergies)"
            ]
        },
        {
            "id": "cq_planning_3",
            "text": "What level of cooking effort are you comfortable with?",
            "options": [
                "Minimal (e.g., microwave or no-cook)",
                "Basic (e.g., simple stovetop recipes)",
                "Intermediate (e.g., recipes with several steps)",
                "I don't mind complex recipes",
                "Depends on the day"
            ]
        },
        {
            "id": "cq_planning_4",
            "text": "Do you have any budget considerations for groceries?",
            "options": [
                "No specific budget",
                "Low-budget meals",
                "Moderate budget",
                "Flexible budget",
                "Unsure"
            ]
        },
        {
            "id": "cq_planning_5",
            "text": "What is your main goal for eating healthier?",
            "options": [
                "Weight management",
                "Improved energy levels",
                "Better overall health",
                "Specific dietary goals (e.g., more protein)",
                "Other"
            ]
        },
        {
            "id": "cq_planning_6",
            "text": "How much time do you have for meal prep on average?",
            "options": [
                "Less than 15 minutes",
                "15 to 30 minutes",
                "30 to 60 minutes",
                "Over an hour",
                "Depends on the day"
            ]
        },
        {
            "id": "cq_planning_7",
            "text": "Do you prefer meals with familiar ingredients or are you open to trying new foods?",
            "options": [
                "Familiar ingredients",
                "Mostly familiar with some new",
                "Open to trying new foods",
                "No preference",
                "Depends on the recipe"
            ]
        },
        {
            "id": "cq_planning_8",
            "text": "Do you have access to common kitchen appliances (e.g., stove, oven, microwave)?",
            "options": [
                "Yes, I have all standard appliances",
                "Some appliances only (e.g., microwave)",
                "Limited access to kitchen appliances",
                "Unsure",
                "Other"
            ]
        },
        {
            "id": "cq_planning_9",
            "text": "Would you like meals with leftovers for future days?",
            "options": [
                "Yes, I prefer leftovers",
                "No, single servings only",
                "Some meals with leftovers, some without",
                "Depends on the meal",
                "Unsure"
            ]
        },
        {
            "id": "cq_planning_10",
            "text": "Are there specific cuisines you enjoy or want to include in your meal plan?",
            "options": [
                "No preference",
                "American/Western",
                "Asian (e.g., Chinese, Indian, Japanese)",
                "Mediterranean",
                "Other (please specify)"
            ]
        }
    ],
    "task_creative": [
        {
            "id": "cq_creative_1",
            "text": "Who is the thank-you message for?",
            "options": [
                "A close friend or family member",
                "A colleague or professional connection",
                "A teacher, mentor, or coach",
                "Someone I don't know very well"
            ]
        },
        {
            "id": "cq_creative_2",
            "text": "What kind of help did they provide?",
            "options": [
                "Emotional support during a hard time",
                "Practical or financial assistance",
                "Advice or guidance",
                "A mix of different types of help"
            ]
        },
        {
            "id": "cq_creative_3",
            "text": "What tone would you like the message to have?",
            "options": [
                "Warm and heartfelt",
                "Formal and professional",
                "Casual and friendly",
                "Creative or unique"
            ]
        },
        {
            "id": "cq_creative_4",
            "text": "How long do you want the message to be?",
            "options": [
                "Just a few sentences",
                "A short paragraph",
                "A detailed and thoughtful message"
            ]
        },
        {
            "id": "cq_creative_5",
            "text": "Would you like to include any specific details about what they did?",
            "options": [
                "Yes, I want to mention their specific actions",
                "No, just a general thank-you is fine",
                "I'm not sure yet"
            ]
        },
        {
            "id": "cq_creative_6",
            "text": "Do you want to include anything about how their help impacted you?",
            "options": [
                "Yes, I want to explain how it made a difference",
                "No, I prefer to keep it simple",
                "I'm not sure yet"
            ]
        },
        {
            "id": "cq_creative_7",
            "text": "Should the message include any mention of future plans or staying in touch?",
            "options": [
                "Yes, I'd like to mention staying in touch",
                "No, just focusing on the thank-you is enough",
                "I'm not sure yet"
            ]
        },
        {
            "id": "cq_creative_8",
            "text": "Do you want the message to include any expressions of gratitude beyond words?",
            "options": [
                "Yes, like offering to return the favor",
                "No, just words are enough",
                "I'm not sure yet"
            ]
        },
        {
            "id": "cq_creative_9",
            "text": "Should the message reference when the help occurred?",
            "options": [
                "Yes, I want to mention the timing",
                "No, I prefer not to include that",
                "I'm not sure yet"
            ]
        },
        {
            "id": "cq_creative_10",
            "text": "How will you send the message?",
            "options": [
                "By email",
                "As a handwritten note",
                "Through a text or messaging app",
                "I'm not sure yet"
            ]
        }
    ],
    "task_recommendation": [
        {
            "id": "cq_recommendation_1",
            "text": "What type of activities do you generally enjoy?",
            "options": [
                "Creative (e.g., art, writing)",
                "Physical (e.g., sports, fitness)",
                "Intellectual (e.g., reading, puzzles)",
                "Social (e.g., group activities)",
                "Other"
            ]
        },
        {
            "id": "cq_recommendation_2",
            "text": "Do you prefer indoor or outdoor hobbies?",
            "options": [
                "Mostly indoor",
                "Mostly outdoor",
                "No preference"
            ]
        },
        {
            "id": "cq_recommendation_3",
            "text": "What is your primary goal for picking up a new hobby?",
            "options": [
                "Relaxation and stress relief",
                "Learning new skills",
                "Meeting new people",
                "Physical fitness",
                "Other"
            ]
        },
        {
            "id": "cq_recommendation_4",
            "text": "How much time per week are you realistically able to dedicate to a new hobby?",
            "options": [
                "1-2 hours",
                "3-5 hours",
                "6-10 hours",
                "More than 10 hours"
            ]
        },
        {
            "id": "cq_recommendation_5",
            "text": "What is your approximate budget for this hobby?",
            "options": [
                "Free or very low-cost",
                "Up to $50 per month",
                "Up to $100 per month",
                "More than $100 per month"
            ]
        },
        {
            "id": "cq_recommendation_6",
            "text": "Would you prefer a hobby that you can do alone or with others?",
            "options": [
                "Alone",
                "With others",
                "No preference"
            ]
        },
        {
            "id": "cq_recommendation_7",
            "text": "Do you want a hobby that involves learning new skills or building on skills you already have?",
            "options": [
                "Learning new skills",
                "Building on existing skills",
                "I'm open to either"
            ]
        },
        {
            "id": "cq_recommendation_8",
            "text": "Are there any physical or logistical constraints you'd like to consider (e.g., limited mobility, space at home)?",
            "options": [
                "Yes, I have physical constraints",
                "Yes, I have space constraints",
                "No constraints"
            ]
        },
        {
            "id": "cq_recommendation_9",
            "text": "Would you prefer a hobby that produces tangible results (e.g., art, crafts) or more experiential (e.g., sports, games)?",
            "options": [
                "Tangible results",
                "Experiential",
                "No preference"
            ]
        },
        {
            "id": "cq_recommendation_10",
            "text": "Do you want a hobby that could potentially become a side business or is purely for leisure?",
            "options": [
                "Potential side business",
                "Purely for leisure",
                "Open to either"
            ]
        }
    ],
    "task_howto": [
        {
            "id": "cq_howto_1",
            "text": "What is the length of your presentation?",
            "options": [
                "Less than 5 minutes",
                "5-10 minutes",
                "10-20 minutes",
                "More than 20 minutes"
            ]
        },
        {
            "id": "cq_howto_2",
            "text": "How familiar are you with the topic of your presentation?",
            "options": [
                "Very familiar",
                "Somewhat familiar",
                "Not very familiar",
                "Not familiar at all"
            ]
        },
        {
            "id": "cq_howto_3",
            "text": "What type of audience will you be presenting to?",
            "options": [
                "Peers or colleagues",
                "Supervisors or managers",
                "Clients or customers",
                "A mixed audience"
            ]
        },
        {
            "id": "cq_howto_4",
            "text": "What is your main goal for this presentation?",
            "options": [
                "Educating the audience",
                "Persuading or convincing",
                "Sharing updates or progress",
                "Building rapport or connection"
            ]
        },
        {
            "id": "cq_howto_5",
            "text": "What is your biggest concern about public speaking?",
            "options": [
                "Forgetting what to say",
                "Appearing nervous",
                "Keeping the audience engaged",
                "Not being prepared"
            ]
        },
        {
            "id": "cq_howto_6",
            "text": "What type of preparation do you prefer?",
            "options": [
                "Practicing in front of others",
                "Practicing alone or with notes",
                "Using visual aids like slides",
                "Improvising with minimal preparation"
            ]
        },
        {
            "id": "cq_howto_7",
            "text": "What setting will your presentation take place in?",
            "options": [
                "A small meeting room",
                "A large conference room",
                "Virtual via video call",
                "Other"
            ]
        },
        {
            "id": "cq_howto_8",
            "text": "How much time do you have available to prepare?",
            "options": [
                "A few hours",
                "A full day",
                "Several days",
                "A week or more"
            ]
        },
        {
            "id": "cq_howto_9",
            "text": "Do you prefer structured or flexible advice?",
            "options": [
                "Very structured (step-by-step)",
                "Somewhat structured",
                "Flexible and adaptable",
                "Minimal guidance"
            ]
        },
        {
            "id": "cq_howto_10",
            "text": "What tools or resources would you like to use?",
            "options": [
                "Slides or visuals",
                "Cue cards or notes",
                "Rehearsal software",
                "None of the above"
            ]
        }
    ],
    "task_ambiguous": [
        {
            "id": "cq_ambiguous_1",
            "text": "What type of work schedule do you currently have?",
            "options": [
                "Regular 9-to-5 hours",
                "Shift work or irregular hours",
                "Freelance or self-employed with flexible hours",
                "Unemployed or between jobs",
                "Other"
            ]
        },
        {
            "id": "cq_ambiguous_2",
            "text": "Where do you typically work from?",
            "options": [
                "An office or workplace outside my home",
                "Primarily from home",
                "A mix of home and office",
                "On the move or in various locations",
                "Other"
            ]
        },
        {
            "id": "cq_ambiguous_3",
            "text": "What is your main goal in improving your work-life balance?",
            "options": [
                "Spending more time on personal or family activities",
                "Reducing stress and mental fatigue",
                "Improving my productivity during work hours",
                "Finding time for hobbies or self-care",
                "Other"
            ]
        },
        {
            "id": "cq_ambiguous_4",
            "text": "What is your biggest challenge in maintaining work-life balance?",
            "options": [
                "Too much work or tight deadlines",
                "Difficulty disconnecting from work after hours",
                "Unclear boundaries between work and home life",
                "Lack of support from colleagues or family",
                "Other"
            ]
        },
        {
            "id": "cq_ambiguous_5",
            "text": "How much structure do you prefer in your daily routine?",
            "options": [
                "A highly structured schedule with clear time blocks",
                "A loose structure with some flexibility",
                "No structure. I prefer to go with the flow",
                "It depends on the day or situation",
                "Other"
            ]
        },
        {
            "id": "cq_ambiguous_6",
            "text": "Do you already have any strategies or habits for managing work-life balance?",
            "options": [
                "Yes, but they aren't working well",
                "Yes, and they work somewhat",
                "No, I don't have any strategies",
                "I haven't thought about it before",
                "Other"
            ]
        },
        {
            "id": "cq_ambiguous_7",
            "text": "How do you prefer to spend your personal or leisure time?",
            "options": [
                "Socializing with family or friends",
                "Engaging in hobbies or creative activities",
                "Exercising or focusing on physical health",
                "Relaxing or doing nothing in particular",
                "Other"
            ]
        },
        {
            "id": "cq_ambiguous_8",
            "text": "What kind of advice or support are you looking for?",
            "options": [
                "Practical tips or techniques to try",
                "Encouragement or mindset shifts",
                "Tools or apps to help organize my time",
                "Examples of how others handle this",
                "Other"
            ]
        },
        {
            "id": "cq_ambiguous_9",
            "text": "How do you usually feel about work-life balance advice?",
            "options": [
                "I find it helpful and motivating",
                "It's often unrealistic for my situation",
                "It's interesting, but hard to apply",
                "I'm skeptical or unsure about it",
                "Other"
            ]
        },
        {
            "id": "cq_ambiguous_10",
            "text": "How urgently do you want to address your work-life balance?",
            "options": [
                "Immediately. I need help now",
                "Soon, within the next few weeks",
                "Eventually, when I have time",
                "Not sure, it's not a priority yet",
                "Other"
            ]
        }
    ]
}

EVALUATION_ITEMS = [
    {"id": "eval_content_fit", "text": "The response addressed my specific situation and needs, not just the general topic."},
    {"id": "eval_personalization", "text": "This response felt like it was written for someone like me, not a generic answer."},
    {"id": "eval_satisfaction", "text": "Overall, I am satisfied with this response."},
    {"id": "eval_effort", "text": "Getting a response that fit my needs felt easy and low-effort."},
]
