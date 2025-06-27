import streamlit as st
import random

# --- Descriptors & templates ---
descriptors = [
    "flowing black hair", "pale skin", "almond-shaped eyes", "high cheekbones",
    "slender build", "graceful posture", "confident smile", "soft expression",
    "full lips", "long legs", "delicate hands"
]

moods = [
    "The soft golden-hour light warms the scene, casting long shadows.",
    "A cool morning haze gives the image a quiet, introspective tone.",
    "The atmosphere is moody and subdued, with rain gently streaking the windows."
]

styles = [
    "The image resembles 1970s film photography, with natural light and grain.",
    "The composition evokes Helmut Newton's fashion editorials, bold yet intimate.",
    "Shot in the style of Irving Penn, the photo emphasizes contrast and subtlety."
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

# --- Prompt builders ---
def build_prompt(subject, mood, style):
    selected_descriptors = ", ".join(random.sample(descriptors, 4))
    subject_line = f"{subject.strip().capitalize()}, with {selected_descriptors}."
    mood_line = mood.strip().capitalize()
    style_line = style.strip().capitalize() if style else random.choice(styles)
    loras = ", ".join(f"<lora:{tag}>" for tag in random.choice(lora_sets))

    return f"""
Prompt: {subject_line}\n{mood_line}\n{style_line}

LoRA: {loras}
Width: {settings['width']}, Height: {settings['height']}, Steps: {settings['steps']}, Sampler: {settings['sampler']}, Scheduler: {settings['scheduler']}
""".strip()

# --- Streamlit UI ---
st.set_page_config(page_title="Flux AI Prompt Generator")
st.title("🤖 Flux AI Prompt Generator & Enhancer")

mode = st.radio("Choose Mode:", ["Suggest Prompt", "Enhance My Prompt"])

if mode == "Suggest Prompt":
    if st.button("Generate Random Prompt"):
        subject = "A young woman"
        mood = random.choice(moods)
        style = random.choice(styles)
        st.text_area("Generated Prompt", build_prompt(subject, mood, style), height=300)

elif mode == "Enhance My Prompt":
    subject_input = st.text_input("Enter subject outline")
    mood_input = st.text_input("Enter mood/setting")
    style_input = st.text_input("Optional: Style or era reference")

    if st.button("Enhance Prompt"):
        if subject_input and mood_input:
            result = build_prompt(subject_input, mood_input, style_input)
            st.text_area("Enhanced Prompt", result, height=300)
        else:
            st.warning("Please enter both subject and mood.")
