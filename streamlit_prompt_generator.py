import streamlit as st
import random

# --- Descriptors & templates ---
descriptors = [
    "long, flowing black hair", "porcelain skin", "almond-shaped eyes with a calm gaze",
    "high cheekbones and a soft jawline", "slender build with a graceful stance",
    "confident smile and expressive brows", "delicate collarbones", "gently curved lips",
    "smooth, even-toned complexion", "graceful posture", "long, delicate fingers"
]

personality_traits = [
    "a quiet confidence", "a mysterious allure", "an introspective nature",
    "an elegant demeanor", "a playful spirit", "a calm presence"
]

mood_templates = [
    "The soft golden-hour light warms the scene, casting long shadows across the ground.",
    "A cool morning haze envelops the surroundings, lending a quiet, introspective atmosphere.",
    "The dim, rain-filtered light through the window sets a somber and contemplative mood.",
    "Overcast skies mute the colors of the setting, amplifying a sense of isolation.",
    "The setting sun bathes the subject in orange-pink hues, evoking warmth and nostalgia."
]

style_templates = [
    "Styled in the manner of a 1970s film photograph, complete with visible grain and natural light.",
    "Captured like a Helmut Newton editorial, bold in contrast and rich in texture.",
    "The composition recalls Irving Penn's fashion work, minimal and elegant in tone.",
    "Photographed in the style of vintage Polaroid, the image is soft, warm, and slightly faded.",
    "Resembling the golden age of analog photography, the scene has tactile realism and cinematic depth."
]

lora_sets = [
    ["plump_slim_edited_modified:0.40", "mature_youthful:0.35", "cinematic-light-lora-v2.0:0.30"],
    ["sarabree:0.35", "old-young:0.30", "fluxabel:0.30"],
    ["hairy-flux:0.40", "detailedskin:0.30", "mature_youthful:0.30"]
]

settings = {
    "width": 1152,
    "height": 1920,
    "steps": 25,
    "sampler": "Euler",
    "scheduler": "simple"
}

# --- Advanced Subject Enhancer ---
def rewrite_subject(subject_input, tone="default", length="medium"):
    elements = [e.strip() for e in subject_input.split(',') if e.strip()]
    appearance, clothing, modifiers = [], [], []

    for word in elements:
        lw = word.lower()
        if any(kw in lw for kw in ["hair", "skin", "eyes", "lips", "face"]):
            appearance.append(word)
        elif any(kw in lw for kw in ["sweater", "dress", "shirt", "blouse", "skirt", "pants"]):
            clothing.append(word)
        elif lw in ["slender", "curvy", "athletic", "petite", "tall", "beauty", "beautiful"]:
            modifiers.append(word)
        else:
            appearance.append(word)

    # Compose base
    base = "A"
    if modifiers:
        joined_mods = ", ".join(modifiers[:-1]) + (" and " + modifiers[-1] if len(modifiers) > 1 else modifiers[0])
        base += f" {joined_mods} woman"
    else:
        base += " woman"

    if appearance:
        base += " with " + ", ".join(appearance)
    if clothing:
        base += ", dressed in " + ", ".join(clothing)

    d_count = 2 if length == "short" else 3 if length == "medium" else 4
    base += ", featuring " + ", ".join(random.sample(descriptors, d_count))
    base += ", and expressing " + random.choice(personality_traits) + "."

    # Tone adjustment
    if tone == "elegant":
        base = base.replace("woman", "elegant woman")
    elif tone == "moody":
        base = base.replace("woman", "melancholic woman")
    elif tone == "playful":
        base = base.replace("woman", "playful woman")

    return base.capitalize()

# --- Prompt builders ---
def build_prompt(subject, mood, style, tone="default", length="medium"):
    subject_line = rewrite_subject(subject, tone, length)

    if len(mood.strip().split()) < 6:
        mood_line = random.choice(mood_templates)
    else:
        mood_line = mood.strip().capitalize()

    if style.strip() == "":
        style_line = random.choice(style_templates)
    elif len(style.strip().split()) < 5:
        matching = [s for s in style_templates if style.lower() in s.lower()]
        style_line = matching[0] if matching else random.choice(style_templates)
    else:
        style_line = style.strip().capitalize()

    loras = ", ".join(f"<lora:{tag}>" for tag in random.choice(lora_sets))

    full_prompt = f"""
Prompt: {subject_line}\n{mood_line}\n{style_line}

LoRA: {loras}
Width: {settings['width']}, Height: {settings['height']}, Steps: {settings['steps']}, Sampler: {settings['sampler']}, Scheduler: {settings['scheduler']}
""".strip()

    return full_prompt

# --- Streamlit UI ---
st.set_page_config(page_title="Flux AI Prompt Generator")
st.title("🤖 Flux AI Prompt Generator & Enhancer")

mode = st.radio("Choose Mode:", ["Suggest Prompt", "Enhance My Prompt"])

if mode == "Suggest Prompt":
    if st.button("Generate Random Prompt"):
        subject = "A young woman"
        mood = random.choice(mood_templates)
        style = random.choice(style_templates)
        prompt = build_prompt(subject, mood, style)
        st.text_area("Generated Prompt", prompt, height=300)
        st.caption(f"Character count: {len(prompt)}")

elif mode == "Enhance My Prompt":
    subject_input = st.text_input("Enter subject outline")
    mood_input = st.text_input("Enter mood/setting")
    style_input = st.text_input("Optional: Style or era reference")
    tone = st.selectbox("Select tone", ["default", "elegant", "playful", "moody"])
    length = st.selectbox("Description length", ["short", "medium", "long"])

    if st.button("Enhance Prompt"):
        if subject_input and mood_input:
            result = build_prompt(subject_input, mood_input, style_input, tone, length)
            st.text_area("Enhanced Prompt", result, height=300)
            st.caption(f"Character count: {len(result)}")
        else:
            st.warning("Please enter both subject and mood.")
