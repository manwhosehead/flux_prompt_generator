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

# --- Enhancers ---
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

    if tone == "elegant":
        base = base.replace("woman", "elegant woman")
    elif tone == "moody":
        base = base.replace("woman", "melancholic woman")
    elif tone == "playful":
        base = base.replace("woman", "playful woman")

    return base.capitalize()

def enhance_mood(text):
    return random.choice(mood_templates) if len(text.strip().split()) < 6 else text.strip().capitalize()

def enhance_style(text):
    if text.strip() == "":
        return random.choice(style_templates)
    elif len(text.strip().split()) < 5:
        match = [s for s in style_templates if text.lower() in s.lower()]
        return match[0] if match else random.choice(style_templates)
    return text.strip().capitalize()

# --- UI ---
st.set_page_config(page_title="Flux AI Modular Prompt Generator")
st.title("🤖 Modular Prompt Builder")

# Input blocks
st.header("1. Subject Outline")
subject_input = st.text_input("Enter subject outline")
tone = st.selectbox("Select tone", ["default", "elegant", "playful", "moody"])
length = st.selectbox("Description length", ["short", "medium", "long"])
subject_enhanced = ""
if st.button("Enhance Subject"):
    subject_enhanced = rewrite_subject(subject_input, tone, length)
    st.text_area("Enhanced Subject", subject_enhanced, height=100)

st.header("2. Mood / Setting")
mood_input = st.text_input("Enter mood/setting")
mood_enhanced = ""
if st.button("Enhance Mood"):
    mood_enhanced = enhance_mood(mood_input)
    st.text_area("Enhanced Mood", mood_enhanced, height=100)

st.header("3. Style / Era Reference")
style_input = st.text_input("Enter style reference (optional)")
style_enhanced = ""
if st.button("Enhance Style"):
    style_enhanced = enhance_style(style_input)
    st.text_area("Enhanced Style", style_enhanced, height=100)

# Final output
st.header("4. Final Prompt Output")
if subject_enhanced and mood_enhanced and style_enhanced:
    loras = ", ".join(f"<lora:{tag}>" for tag in random.choice(lora_sets))
    prompt = f"Prompt: {subject_enhanced}\n{mood_enhanced}\n{style_enhanced}\n\nLoRA: {loras}\nWidth: {settings['width']}, Height: {settings['height']}, Steps: {settings['steps']}, Sampler: {settings['sampler']}, Scheduler: {settings['scheduler']}"
    st.text_area("Final Prompt", prompt, height=300)
    st.caption(f"Character count: {len(prompt)}")
else:
    st.warning("Enhance all three sections to preview the full prompt.")
