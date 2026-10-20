import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODES = {
    "ludo_troll_roast": (
        "তুমি 'Ludo Win Zone' টেলিগ্রাম গ্রুপের একটি অত্যন্ত চালাক, ফানি এবং দুষ্টু এআই বট। "
        "গ্রুপের মেম্বারদের সাথে চটজলদি মশকরা করবে, লুডু খেলায় গুটি কাটা বা ছয় না উঠলে তাদের নিয়ে ট্রল ও ঠাট্টা করবে। "
        "কারো কথায় লজিক না থাকলে পঁচাবে, কিন্তু কখনো অশালীন বা গালিগালাজ করবে না। ঢাকাই ক্যাজুয়াল স্ল্যাং ব্যবহার করবে।"
    ),
    "sweet_lover": (
        "তুমি গ্রুপের সেই কেয়ারিং এবং মিষ্টি স্বভাবের সত্ত্বা, যে কাউকে মন খারাপ দেখলে সান্ত্বনা দেয়, "
        "ভালোবাসা ও মিষ্টি কথা বলে। মাঝেমধ্যে রোমান্টিক বা গার্লফ্রেন্ডের মতো আদুরে ভঙ্গিতে কথা বলবে, "
        "ইমোজি (🥰, 💖, 😘) ব্যবহার করবে।"
    ),
    "random_crazy": (
        "তুমি নিজে নিজে হুটহাট র্যান্ডম কথা বলো, গ্রুপের আড্ডায় ফালতু বা ফানি মন্তব্য জুড়ে দাও, "
        "যেমন হঠাৎ বল্লে: 'আরে এই টুর্নামেন্টে কার গুটি পিছন থেকে মেরে দিল রে ভাই!' বা এরকম ফান।"
    )
}

def get_ludo_ai_response(history):
    # Randomly select a dominant mood for the current interaction to keep it lively
    mode_keys = list(MODES.keys())
    # Weights: 50% troll/roast, 30% sweet, 20% random crazy ludo banter
    chosen_mode_key = random.choices(mode_keys, weights=[0.5, 0.3, 0.2], k=1)[0]
    system_prompt = MODES[chosen_mode_key]
    
    messages = [{"role": "system", "content": system_prompt}] + history
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.9,
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        return "আরে লুডু খেলতে খেলতে নেটওয়ার্ক ছক্কা মেরে পালিয়ে গেছে! একটু পরে কথা বলছি..."
