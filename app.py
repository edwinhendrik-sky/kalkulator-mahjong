import streamlit as st

class J2MahjongCalculator:
    def __init__(self):
        # Database Hand Kemenangan dengan penamaan yang lebih deskriptif (UI Friendly)
        self.base_hands = {
            "🐔 CHICKEN HAND (Campur aduk biasa)": (0, 0),
            "🔢 ALL SEQUENCES (Semua 4 set berurutan/Chow)": (2, 2),
            "🀄 ALL TRIPLETS (Semua 4 set kembar/Pong)": (3, 3),
            "🏁 MIXED TERMINALS (Hanya angka 1, 9, dan Honour)": (3, 3),
            "🎨 MIXED / SEMI FLUSH (Satu warna/suit + Honour)": (4, 4),
            "🐉 SMALL THREE DRAGONS (2 set Naga + 1 pair Naga)": (5, 5),
            "👯 SEVEN PAIRS (7 Pasang Pair berbeda)": (10, 20),
            "🌈 FULL COLOUR (Murni 1 warna/suit saja)": (10, 20),
            "🐲 3 SCHOLARS / BIG 3 DRAGON (3 set Naga komplit)": (10, 20),
            "🌬️ SMALL FOUR WINDS (3 set Angin + 1 pair Angin)": (10, 20),
            "🤫 ALL CONCEALED TRIPLETS (4 Pong tertutup/ambil sendiri)": (10, 20),
            "👑 ALL HONOURS (Isi keping murni Naga dan Angin saja)": (10, 20),
            "🛑 ALL TERMINALS (Isi keping murni angka 1 dan 9)": (10, 20),
            "⛩️ NINE GATES (Kombinasi 111-2345678-999 satu warna)": (12, 22),
            "🌪️ 4 BLESSINGS / BIG 4 WINDS (4 set Angin komplit)": (12, 22),
            "🌟 13 ORPHANS (13 keping ujung & honour berbeda)": (15, 25),
            "🧱 ALL QUADRUPLETS (Semua 4 set berupa Kong)": (15, 25),
            "👼 TIANHU / DI HU (Menang instan di awal putaran)": (15, 25)
        }

    def calculate(self, hand_name, joker_count, bonuses, is_false_hu):
        if is_false_hu:
            return -30, "🚨 PELANGGARAN! Penalti 30 poin. Setiap lawan menerima +10 poin."

        base_scores = self.base_hands[hand_name]
        has_joker = joker_count > 0
        
        # Penentuan Poin Dasar
        if base_scores[0] != base_scores[1]:
            # Hand bernilai ganda (Bonus tanpa joker otomatis masuk ke nilai maksimal)
            score = base_scores[0] if has_joker else base_scores[1]
        else:
            # Hand reguler
            score = base_scores[0]
            if not has_joker:
                score += 2  # Bonus Murni (Tanpa Joker)

        # Tambahan Poin
        score += joker_count
        score += bonuses

        return score, ""

# --- SETUP HALAMAN ---
st.set_page_config(page_title="Kalkulator Mahjong Simple", layout="centered")
st.title("🀄 Kalkulator J2 Mahjong")
st.markdown("Ikuti **3 Langkah** di bawah ini untuk menghitung poin Anda.")

app = J2MahjongCalculator()

# --- LANGKAH 1: POLA DASAR ---
with st.container(border=True):
    st.subheader("Langkah 1: Pola Utama")
    hand_pilihan = st.selectbox("Apa bentuk pola kemenangan Anda?", list(app.base_hands.keys()))
    
# --- LANGKAH 2: JOKER & CARA MENANG ---
with st.container(border=True):
    st.subheader("Langkah 2: Status Kemenangan")
    col2a, col2b = st.columns(2)
    
    with col2a:
        jumlah_joker = st.number_input("Jumlah Joker yang dipakai:", min_value=0, max_value=4, value=0)
    with col2b:
        jenis_menang = st.radio("Menang dari mana?", ["RON (Ambil buangan lawan)", "ZIMO (Ambil keping sendiri)"])

# --- LANGKAH 3: BONUS ---
with st.container(border=True):
    st.subheader("Langkah 3: Bonus Tambahan (Opsional)")
    st.write("Ceklis yang sesuai dengan keping Anda:")
    
    bonus_total = 0
    
    # Checkbox sederhana untuk bonus umum
    if st.checkbox("Mempunyai set 3-Kembar (Pong) NAGA (+1/set)"): bonus_total += 1
    if st.checkbox("Mempunyai set 3-Kembar (Pong) ANGIN sesuai Kursi/Putaran (+1)"): bonus_total += 1
    if st.checkbox("Keping penutup (Pair/Mata) adalah angka 2 atau 8 (+1)"): bonus_total += 1
    if st.checkbox("Bunga Merah / Hitam Sesuai Kursi (+2 atau +1)"): bonus_total += 1
    
    # Menu tersembunyi untuk bonus yang jarang (agar UI tidak penuh)
    with st.expander("Lihat Bonus Ekstra / Kondisi Langka..."):
        if st.checkbox("Menang tanpa keping Bunga, Naga, Angin sama sekali (+2)"): bonus_total += 2
        if st.checkbox("Menang dari keping terakhir (Last Tile) (+2)"): bonus_total += 2
        if st.checkbox("Mencuri Kong (Stealing Kong) (+1)"): bonus_total += 1
        if st.checkbox("Punya FULL SET (4) Bunga Merah atau Hitam (+7 / +5)"): bonus_total += 5
        
    is_false_hu = st.checkbox("🚨 Kena Penalti (False Hu / Salah Panggil)", help="Centang ini jika pemain salah mendeklarasikan kemenangan")

st.divider()

# --- TOMBOL HASIL ---
hitung_btn = st.button("🧮 HITUNG TOTAL PEMBAYARAN", type="primary", use_container_width=True)

if hitung_btn:
    total_skor, pesan_error = app.calculate(hand_pilihan, jumlah_joker, bonus_total, is_false_hu)
    
    if is_false_hu:
        st.error(pesan_error)
    elif total_skor < 3:
        st.warning(f"Skor Anda: **{total_skor} Poin**. \n\n⚠️ **TIDAK SAH MENANG!** Total skor (termasuk bonus) minimal harus 3 poin.")
    else:
        st.success(f"## 🎉 SKOR FINAL: {total_skor} Poin")
        
        st.markdown("### 💰 Siapa yang harus membayar?")
        if "RON" in jenis_menang:
            st.info(f"👉 **Pemain yang Membuang Keping** membayar **{total_skor * 2} Chip/Poin** (2x Lipat).")
            st.info(f"👉 **Dua Pemain Lainnya** masing-masing membayar **{total_skor} Chip/Poin** (1x Lipat).")
        else: # ZIMO
            st.info(f"👉 **Ketiga Pemain Lawan** masing-masing membayar **{total_skor * 2} Chip/Poin** (2x Lipat).")