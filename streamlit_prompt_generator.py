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
    "an elegant demeanor", "a playful spirit", "a calm presence",
    "a charismatic energy", "a poised elegance", "a whimsical charm"
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

style_keywords = {
    "polaroid": [style_templates[3], "Soft hues and gentle contrast give the photo a nostalgic Polaroid character.", "Like a sun-faded instant film print, the image has warmth and imperfection."],
    "1970": [style_templates[0], "Retro tones and grain texture place this scene squarely in the 1970s aesthetic."],
    "70s": [style_templates[0]],
    "helmut": [style_templates[1], "Dramatic lighting and confident posture mirror Helmut Newton's signature editorial style."],
    "newton": [style_templates[1]],
    "irving": [style_templates[2], "Understated elegance and clarity recall the iconic style of Irving Penn."],
    "penn": [style_templates[2]],
    "analog": [style_templates[4], "Grainy textures and soft highlights simulate the character of classic analog film."],
    "cinematic": [style_templates[4]]
}

mood_keywords = {
    "beach": [
        "The sunlight sparkles on the waves while sea breeze rustles the palms, creating a relaxed coastal mood.",
        "Gentle ocean waves crash in the distance as warm light washes over the sandy shore.",
        "A soft breeze carries the scent of salt and sunscreen across the sunlit beach scene."
    ],
    "night": [
        "Moonlight softly illuminates the scene, casting long shadows across a quiet, nocturnal setting.",
        "Dim streetlights flicker through misty air, creating an atmospheric and dreamlike mood."
    ],
    "urban": [
        "Neon lights reflect off wet pavement, bringing vibrant energy to the bustling city backdrop.",
        "Steel and glass architecture towers above a crowded street, buzzing with motion and light."
    ],
    "forest": [
        "Dappled sunlight filters through thick trees, lending a serene, natural ambiance.",
        "Pine needles carpet the quiet forest floor as rays of light pierce the canopy."
    ],
    "studio": [
        "Softbox light sculpts the figure in a clean, controlled indoor setting.",
        "A seamless backdrop and balanced lighting create a crisp, editorial-style composition."
    ],
    "mountain": [
        "High-altitude sunlight filters through crisp, cool air, with jagged peaks as backdrop.",
        "Wind stirs through alpine meadows, and clouds skim the snow-dusted ridges above."
    ],
    "desert": [
        "Dry golden light creates long shadows on dusty terrain, evoking solitude and warmth.",
        "Rippling dunes stretch to the horizon under an orange sky, evoking timeless isolation."
    ]
}

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
        elif any(kw in lw for kw in ["sweater", "dress", "shirt", "blouse", "skirt", "pants", "bikini", "cape"]):
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
    for keyword, templates in mood_keywords.items():
        if keyword in text.lower():
            return random.choice(templates)
    return random.choice(mood_templates)

def enhance_style(text):
    for keyword, templates in style_keywords.items():
        if keyword in text.lower():
            return random.choice(templates)
    if text.strip():
        return text.strip().capitalize()
    return random.choice(style_templates)

# --- UI ---
st.set_page_config(page_title="Flux AI Modular Prompt Generator")
st.title("🤖 Modular Prompt Builder")

# Initialize session state
for key in ["subject_enhanced", "mood_enhanced", "style_enhanced"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# Input blocks
st.header("1. Subject Outline")
subject_input = st.text_input("Enter subject outline")
tone = st.selectbox("Select tone", ["default", "elegant", "playful", "moody"])
length = st.selectbox("Description length", ["short", "medium", "long"])
if st.button("Enhance Subject"):
    st.session_state.subject_enhanced = rewrite_subject(subject_input, tone, length)
st.text_area("Enhanced Subject", st.session_state.subject_enhanced, height=100)

st.header("2. Mood / Setting")
mood_input = st.text_input("Enter mood/setting")
if st.button("Enhance Mood"):
    st.session_state.mood_enhanced = enhance_mood(mood_input)
st.text_area("Enhanced Mood", st.session_state.mood_enhanced, height=100)

st.header("3. Style / Era Reference")
style_input = st.text_input("Enter style reference (optional)")
if st.button("Enhance Style"):
    st.session_state.style_enhanced = enhance_style(style_input)
st.text_area("Enhanced Style", st.session_state.style_enhanced, height=100)

# Final output
st.header("4. Final Prompt Output")
if all([st.session_state.subject_enhanced, st.session_state.mood_enhanced, st.session_state.style_enhanced]):
    loras = ", ".join(f"<lora:{tag}>" for tag in random.choice(lora_sets))
    prompt = f"Prompt: {st.session_state.subject_enhanced}\n{st.session_state.mood_enhanced}\n{st.session_state.style_enhanced}\n\nLoRA: {loras}\nWidth: {settings['width']}, Height: {settings['height']}, Steps: {settings['steps']}, Sampler: {settings['sampler']}, Scheduler: {settings['scheduler']}"
    st.text_area("Final Prompt", prompt, height=300)
    st.caption(f"Character count: {len(prompt)}")
else:
    st.warning("Enhance all three sections to preview the full prompt.")
    
