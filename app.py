import streamlit as st
from deep_translator import GoogleTranslator

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Banana DNA: Ultimate", page_icon="🍌", layout="centered")

# --- DATABASE DNA (LOCKED) ---
# Data fisik: 171cm, 57kg, Lean Physique
MY_FACE_DNA = (
    "a young Southeast Asian man with a lean slender physique (171cm height, 57kg weight). "
    "He has a distinct oval face, sharp pointed chin, defined jawline, and a medium-width nose with a rounded tip. "
    "His hair is thick, black, and voluminous, styled with a messy textured fringe covering the forehead "
    "and neatly tapered low-fade sides. He has dark almond-shaped eyes, natural eyebrows, and thin lips with a subtle smirk."
)

MY_ACCESSORIES_FIXED = (
    "He is accessorized with a small silver cross necklace and a detailed CASIO AE-1300WH digital watch "
    "with a metallic red bezel and a black resin strap on his left wrist."
)

# --- FUNGSI TRANSLATE ---
def translate_to_en(text):
    """Menerjemahkan Indo -> Inggris secara otomatis"""
    if text and len(text) > 1:
        try:
            return GoogleTranslator(source='auto', target='en').translate(text)
        except:
            return text # Fallback jika error
    return text

st.title("🍌 Banana DNA: Ultimate")
st.caption("Auto-Translate 🇮🇩 | Director Mode 🎬 | Real Wardrobe 👕")

# --- FORM INPUT ---
with st.form(key='master_form'):
    
    # 1. KONTEKS (Bhs Indonesia)
    st.subheader("1. Konteks & Suasana (Indo)")
    user_action = st.text_area("Lagi ngapain?", 
                              placeholder="Contoh: Duduk santai di warkop sambil minum kopi...",
                              height=70)

    # 2. DIRECTOR MODE (Angle & Shot)
    st.subheader("2. Director Mode")
    col_angle, col_shot = st.columns(2)
    with col_angle:
        cam_angle = st.selectbox("Angle Kamera:", 
                                 ["Eye Level (Normal)", 
                                  "Low Angle (Terlihat Tinggi)", 
                                  "Frog Eye (Dari Tanah)", 
                                  "High Angle (Dari Atas)", 
                                  "Bird Eye (Tegak Lurus)"])
    with col_shot:
        shot_size = st.selectbox("Ukuran Shot:", 
                                 ["Medium Shot (Pinggang ke Atas)",
                                  "Long Shot (Full Body)", 
                                  "Medium Long (Lutut ke Atas)", 
                                  "Close Up (Dada ke Atas)", 
                                  "Big Close Up (Wajah)", 
                                  "Extreme Close Up (Mata/Mulut)"])

    # 3. WARDROBE (Real Size Logic)
    st.subheader("3. Wardrobe (OOTD)")
    col_top1, col_top2, col_top3 = st.columns([2, 2, 1.5])
    with col_top1:
        top_item = st.text_input("Baju (Indo):", value="Kaos Polos")
    with col_top2:
        top_color = st.text_input("Warna (Indo):", value="Hitam")
    with col_top3:
        # Logic ukuran L/XL vs Oversized L
        top_fit = st.selectbox("Fit:", ["Regular (L/XL)", "Oversized (L)", "Slim"])

    col_bot1, col_bot2 = st.columns(2)
    with col_bot1:
        bottom_item = st.text_input("Celana (Indo):", value="Celana Chino")
    with col_bot2:
        # Logic Size 30 vs Pendek
        bottom_style = st.selectbox("Model:", ["Panjang (Size 30)", "Pendek (Lutut)", "Relaxed"])

    # 4. ALAS KAKI
    st.markdown("**Alas Kaki:**")
    footwear_type = st.radio("Pilih:", ["Sepatu (Adidas Courtblock)", "Sandal (Fipper)", "Custom"], horizontal=True)
    
    final_footwear_en = ""
    # Pre-defined shoes (Sudah Inggris)
    if footwear_type == "Sepatu (Adidas Courtblock)":
        final_footwear_en = "wearing white Adidas Courtblock sneakers"
    elif footwear_type == "Sandal (Fipper)":
        strap_color = st.selectbox("Warna Tali Fipper:", ["Putih", "Hitam", "Merah", "Biru"])
        color_map = {"Putih": "white", "Hitam": "black", "Merah": "red", "Biru": "blue"}
        final_footwear_en = f"wearing black Fipper flip-flops with {color_map.get(strap_color)} straps"
    else:
        custom_shoes_indo = st.text_input("Sepatu Lain (Indo):", placeholder="Contoh: Sepatu Boots Kulit")

    # 5. TEKNIS
    st.subheader("4. Teknis & Rasio")
    col_cam1, col_cam2 = st.columns(2)
    with col_cam1:
        camera_lens = st.selectbox("Lensa:", ["iPhone 17 Pro Max - 0.5x Ultra Wide", "Cinematic Portrait", "Standard"])
    with col_cam2:
        aspect_ratio = st.selectbox("Rasio:", ["9:16 (TikTok)", "3:4 (IG Feed)", "16:9 (Landscape)", "1:1 (Square)"])
    
    submit = st.form_submit_button(label='GENERATE MASTER PROMPT 🚀', use_container_width=True)

# --- ENGINE ---
def build_prompt(action_en, angle, shot, top_i_en, top_c_en, top_f, bot_i_en, bot_s, shoes_en, lens, ratio):
    
    # A. LOGIKA ANGLE
    if "Low" in angle: angle_kw = "low-angle shot looking up"
    elif "Frog" in angle: angle_kw = "extreme low-angle frog's eye view shot from ground level"
    elif "High" in angle: angle_kw = "high-angle shot looking down"
    elif "Bird" in angle: angle_kw = "overhead bird's-eye view shot"
    else: angle_kw = "eye-level shot"

    # B. LOGIKA SHOT & VISIBILITAS (PENTING!)
    show_shoes = True
    show_pants = True
    
    if "Long Shot" in shot: shot_kw = "long shot (LS), full body framing from head to toe"
    elif "Medium Long" in shot: shot_kw = "medium long shot (MLS), framed from knees up"
    elif "Medium Shot" in shot: 
        shot_kw = "medium shot (MS), framed from waist up"
        show_shoes = False
    elif "Close Up" in shot: 
        shot_kw = "close-up (MCU), framed from chest up"
        show_shoes = False; show_pants = False
    elif "Big Close" in shot: 
        shot_kw = "big close-up (BCU), framing face tightly"
        show_shoes = False; show_pants = False
    elif "Extreme" in shot: 
        shot_kw = "extreme close-up (ECU), macro detail"
        show_shoes = False; show_pants = False
    else: shot_kw = "medium shot"

    # C. LOGIKA OUTFIT (Real Size Translation)
    # Atasan
    if "Oversized" in top_f: top_desc = f"a {top_c_en} {top_i_en} (trendy oversized fit, dropped shoulders)"
    elif "Regular" in top_f: top_desc = f"a {top_c_en} {top_i_en} (classic regular fit)"
    else: top_desc = f"a {top_c_en} {top_i_en} (slim fit)"

    # Rakit Outfit
    outfit_full = f"wearing {top_desc}"
    
    if show_pants:
        if "Panjang" in bot_s: bot_desc = f", {bot_i_en} (slim-tapered size 30 cut)"
        elif "Pendek" in bot_s: bot_desc = f", knee-length {bot_i_en}"
        else: bot_desc = f", {bot_i_en}"
        outfit_full += bot_desc
    
    if show_shoes and shoes_en:
        outfit_full += f", {shoes_en}"

    # D. TEKNIS & RASIO
    if "0.5x" in lens: tech = "Shot on iPhone 17 Pro Max, 0.5x ultra-wide lens, dynamic perspective."
    elif "Cinematic" in lens: tech = "Cinematic bokeh, f/1.8 aperture, soft blur."
    else: tech = "High-fidelity 24MP, sharp focus."

    if "9:16" in ratio: r_kw = "vertical 9:16 aspect ratio"
    elif "3:4" in ratio: r_kw = "vertical 3:4 aspect ratio"
    elif "16:9" in ratio: r_kw = "wide 16:9 aspect ratio"
    else: r_kw = "square 1:1 aspect ratio"

    # E. RAKIT FINAL
    return (
        f"A high-fidelity realistic {angle_kw}, {shot_kw} of {MY_FACE_DNA}. "
        f"{action_en}. "
        f"He is {outfit_full}. "
        f"{MY_ACCESSORIES_FIXED} "
        f"{tech} "
        f"Cinematic lighting, natural skin texture, {r_kw}, aesthetic smartphone photography style."
    )

# --- EKSEKUSI ---
if submit:
    if user_action:
        with st.spinner('Menerjemahkan & Merakit Prompt...'):
            # 1. Translate Input User
            act_en = translate_to_en(user_action)
            top_i_en = translate_to_en(top_item)
            top_c_en = translate_to_en(top_color)
            bot_i_en = translate_to_en(bottom_item)
            
            # Handle sepatu custom
            if footwear_type == "Custom":
                shoes_final = f"wearing {translate_to_en(custom_shoes_indo)}"
            else:
                shoes_final = final_footwear_en

            # 2. Build
            final_prompt = build_prompt(act_en, cam_angle, shot_size, top_i_en, top_c_en, top_fit, bot_i_en, bottom_style, shoes_final, camera_lens, aspect_ratio)
            
            st.success("Prompt Selesai! Salin di bawah ini 👇")
            st.code(final_prompt, language="text")
            
            with st.expander("🔍 Cek Hasil Terjemahan"):
                st.write(f"**Aktivitas:** {user_action} -> *{act_en}*")
                st.write(f"**Outfit:** {top_color} {top_item} -> *{top_c_en} {top_i_en}*")
    else:
        st.warning("⚠️ Masukkan aktivitas dulu!")
