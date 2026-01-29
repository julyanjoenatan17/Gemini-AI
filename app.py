import streamlit as st

st.set_page_config(page_title="Banana DNA Pro", page_icon="🍌")

# --- DATABASE DNA WAJAH FINAL (171cm/57kg) ---
MY_FACE_DNA = (
    "a young Southeast Asian man with a lean slender physique (171cm height, 57kg weight). "
    "He has a distinct oval face, sharp pointed chin, defined jawline, and a medium-width nose with a rounded tip. "
    "His hair is thick, black, and voluminous, styled with a messy textured fringe covering the forehead "
    "and neatly tapered low-fade sides. He has dark almond-shaped eyes, natural eyebrows, and thin lips with a subtle smirk."
)

MY_ACCESSORIES = (
    "He is wearing a small silver cross necklace and a detailed CASIO AE-1300WH digital watch "
    "with a metallic red bezel and a black resin strap on his left wrist."
)

st.title("🍌 Banana DNA: Ultimate Creator")
st.markdown("Generator prompt dengan **DNA Fisik**, **Aksesori**, dan **Pengaturan Rasio**.")

# --- FORM INPUT ---
with st.form(key='dna_form'):
    # Input 1: Aktivitas
    user_action = st.text_area("Aktivitas / Lokasi / Suasana:", 
                              placeholder="Contoh: Berdiri di pinggir jalan Tokyo saat hujan malam hari...",
                              height=100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input 2: Gaya Kamera
        camera_style = st.selectbox("Gaya Kamera:", 
                                    ["iPhone 17 Pro Max - 0.5x Ultra Wide", 
                                     "iPhone 17 Pro Max - Cinematic Portrait", 
                                     "Standard Photorealistic"])
    
    with col2:
        # Input 3: Rasio & Orientasi (FITUR BARU)
        aspect_ratio = st.selectbox("Rasio & Orientasi:", 
                                    ["9:16 (Portrait - TikTok/Story)", 
                                     "3:4 (Portrait - Instagram Feed)", 
                                     "16:9 (Landscape - Cinematic)", 
                                     "4:3 (Landscape - Standard)", 
                                     "1:1 (Square)"])
    
    submit = st.form_submit_button(label='GENERATE PROMPT 🚀')

# --- LOGIKA GENERATOR ---
def build_prompt(action, style, ratio):
    # 1. Menentukan Teknis Kamera
    if "0.5x" in style:
        tech = "Shot on iPhone 17 Pro Max using 0.5x ultra-wide lens, dynamic perspective, dramatic depth."
    elif "Cinematic" in style:
        tech = "Shot on iPhone 17 Pro Max, cinematic bokeh, f/1.8 aperture, soft background blur."
    else:
        tech = "High-fidelity 24MP resolution, natural lighting, sharp focus."

    # 2. Menentukan Keyword Rasio
    if "9:16" in ratio:
        ratio_prompt = "vertical 9:16 aspect ratio, full body shot, mobile screen framing"
    elif "3:4" in ratio:
        ratio_prompt = "vertical 3:4 aspect ratio, classic portrait composition"
    elif "16:9" in ratio:
        ratio_prompt = "wide 16:9 aspect ratio, cinematic widescreen composition"
    elif "4:3" in ratio:
        ratio_prompt = "landscape 4:3 aspect ratio, standard photography framing"
    else:
        ratio_prompt = "square 1:1 aspect ratio"

    # 3. Struktur Kalimat Final
    return (
        f"A high-fidelity 24MP portrait of {MY_FACE_DNA} {action}. "
        f"{MY_ACCESSORIES} {tech} "
        f"Cinematic lighting, natural skin texture with visible pores, high character fidelity, {ratio_prompt}, aesthetic smartphone photography style."
    )

# --- TAMPILAN HASIL ---
if submit:
    if user_action:
        result = build_prompt(user_action, camera_style, aspect_ratio)
        st.success("Prompt dengan Rasio & DNA Siap!")
        st.code(result, language="text")
        
        # Fitur Salin Cepat (Petunjuk)
        st.info("💡 **Tips:** Untuk rasio 9:16 (TikTok), pastikan saat generate di Gemini/Tool lain, kamu tidak memotong (crop) bagian kepala atau kaki.")
    else:
        st.warning("⚠️ Masukkan aktivitas atau lokasi dulu!")
