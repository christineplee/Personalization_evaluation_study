"""
generate_content_questions.py

Pre-generates content-specific clarifying questions for each task using
GATE-style LLM prompting. Output is reviewed by researchers and then
locked into questions.py before deployment.

Usage:
    cd backend
    # Make sure .env has your Azure credentials
    python generate_content_questions.py

Output:
    generated_content_questions.json — review, edit, then paste into questions.py
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(Path(__file__).parent / ".env")

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

TASKS = [
    {
        "id": "task_planning",
        "prompt": "I want to start eating healthier but I'm busy and not a great cook. Can you help me plan meals for the week?",
    },
    {
        "id": "task_advice",
        "prompt": "I have a friend who I feel like has been pulling away lately. I don't know if I did something wrong or if they're just going through their own stuff. How should I handle this?",
    },
    {
        "id": "task_creative",
        "prompt": "I need to write a thank-you message to someone who really helped me through a tough time. Can you help me figure out what to say?",
    },
]

GENERATION_PROMPT = """You are helping design a research study on AI personalization. 

A user will ask an AI assistant the following request:
"{task_prompt}"

Your job: Generate exactly 10 clarifying questions that the AI could ask the user 
BEFORE generating its response, in order to give a much more personalized and 
relevant answer. These questions should help the AI understand the user's specific 
situation, preferences, constraints, and goals.

IMPORTANT DESIGN CONSTRAINTS:
- Each question must have 3-5 multiple-choice answer options
- Questions should be ordered from most essential (Q1) to least essential (Q10), 
  because some users will only see the first 3, others the first 6, and others all 10
- Questions should naturally mix different types:
  * SITUATIONAL: facts about the user's specific circumstances (who, what, when, where)
  * PREFERENCE: how the user likes things done, what they care about
  * GOAL: what the user is trying to achieve, what outcome they want
- Options should be mutually exclusive and collectively cover the common cases
- Keep questions short and easy to answer quickly
- Don't ask anything that would be too personal or invasive for an anonymous online study

Format your response as a JSON array of 10 objects, each with:
- "id": a short identifier like "cq_plan_1" (use the prefix I give you)
- "text": the question text
- "type_tag": one of "situational", "preference", or "goal" (for researcher coding)
- "options": array of 3-5 string options

Use the ID prefix: "{id_prefix}"

Return ONLY valid JSON, no other text."""


def generate_questions_for_task(client, task):
    """Call the LLM to generate content questions for one task."""
    id_prefix = task["id"].replace("task_", "cq_")

    response = client.chat.completions.create(
        model=AZURE_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": "You are a research study designer. Return only valid JSON.",
            },
            {
                "role": "user",
                "content": GENERATION_PROMPT.format(
                    task_prompt=task["prompt"],
                    id_prefix=id_prefix,
                ),
            },
        ],
        temperature=0.7,
        max_tokens=4096,
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[:-3]
    return json.loads(raw)


def main():
    if not AZURE_API_KEY or AZURE_API_KEY == "your-api-key-here":
        print("ERROR: Set AZURE_OPENAI_API_KEY in .env to generate questions.")
        print("You can also manually write questions in questions.py.")
        return

    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
    )

    all_questions = {}
    for task in TASKS:
        print(f"Generating questions for: {task['id']}...")
        try:
            questions = generate_questions_for_task(client, task)
            all_questions[task["id"]] = questions
            print(f"  ✓ Generated {len(questions)} questions")

            # Print summary
            for i, q in enumerate(questions):
                tag = q.get("type_tag", "?")
                print(f"    Q{i+1} [{tag}]: {q['text']}")
                print(f"         Options: {q['options']}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            all_questions[task["id"]] = []

    # Save to file for review
    output_path = Path(__file__).parent / "generated_content_questions.json"
    with open(output_path, "w") as f:
        json.dump(all_questions, f, indent=2)

    print(f"\n✓ Saved to {output_path}")
    print("\nNEXT STEPS:")
    print("1. Review the generated questions in generated_content_questions.json")
    print("2. Edit any questions/options that don't feel right")
    print("3. Check that Q1-3 are the most essential (these are what the P3 condition sees)")
    print("4. Verify the type_tag coding (situational/preference/goal)")
    print("5. Copy the final questions into CONTENT_QUESTIONS in questions.py")
    print("   (remove the type_tag field — it's for your research notes only)")

    # Also generate a Python-ready snippet
    snippet_path = Path(__file__).parent / "generated_content_questions_py.txt"
    with open(snippet_path, "w") as f:
        f.write("# Copy this into CONTENT_QUESTIONS in questions.py\n")
        f.write("# Remove type_tag before deployment (it's for researcher coding only)\n\n")
        f.write("CONTENT_QUESTIONS = ")
        # Format without type_tag for questions.py
        clean = {}
        for task_id, qs in all_questions.items():
            clean[task_id] = [
                {"id": q["id"], "text": q["text"], "options": q["options"]}
                for q in qs
            ]
        f.write(json.dumps(clean, indent=4))
        f.write("\n")

    print(f"✓ Python snippet saved to {snippet_path}")


if __name__ == "__main__":
    main()
