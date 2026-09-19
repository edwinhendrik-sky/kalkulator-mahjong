import streamlit as st

class KalkulatorPemulaJ2:
    def __init__(self):
        # Format Baru: "Bahasa Awam": (Poin Joker, Poin Murni, "Nama Resmi", "CONTOH VISUAL UBIN")
        self.katalog_visual = {
            "🔀 Campur aduk (Ada seri, ada kembar, beda warna)": (0, 0, "CHICKEN HAND", 
                "🀙🀚🀛  🀔🀔🀔  🀝🀞🀟  🀇🀈🀉  +  🀀🀀"),
            "🔢 Semuanya berupa susunan SERI BERURUTAN (Chow)": (2, 2, "ALL SEQUENCES", 
                "🀙🀚🀛  🀔🀕🀖  🀝🀞🀟  🀇🀈🀉  +  🀀🀀"),
            "🀄 Semuanya berupa 3-KEMBAR (Pong)": (3, 3, "ALL TRIPLETS", 
                "🀙🀙🀙  🀔🀔🀔  🀄🀄🀄  🀇🀇🀇  +  🀀🀀"),
            "🧱 Semuanya berupa 4-KEMBAR (Kong)": (15, 25, "ALL QUADRUPLETS", 
                "🀙🀙🀙🀙  🀔🀔🀔🀔  🀄🀄🀄🀄  🀇🀇🀇🀇  +  🀀🀀"),
            "🎨 Warnanya MURNI SATU JENIS saja (Tanpa huruf)": (10, 20, "FULL COLOUR", 
                "🀙🀚🀛  🀙🀙🀙  🀝🀞🀟  🀡🀡🀡  +  🀠🀠"),
            "🖌️ Satu warna dasar, TAPI dicampur tulisan Naga/Angin": (4, 4, "MIXED / SEMI FLUSH", 
                "🀙🀚🀛  🀙🀙🀙  🀝🀞🀟  🀄🀄🀄  +  🀀🀀"),
            "👑 Murni hanya keping tulisan NAGA dan ANGIN saja": (10, 20, "ALL HONOURS", 
                "🀀🀀🀀  🀁🀁🀁  🀄🀄🀄  🀆🀆🀆  +  🀅🀅"),
            "🐉 Ada 3 set kembar Naga komplit (Merah, Hijau, Putih)": (10, 20, "3 SCHOLARS (BIG 3 DRAGONS)", 
                "🀄🀄🀄  🀅🀅🀅  🀆🀆🀆  🀙🀚🀛  +  🀀🀀"),
            "🐲 Ada 2 set kembar Naga + 1 pasang (Pair) Naga": (5, 5, "SMALL THREE DRAGONS", 
                "🀄🀄🀄  🀅🀅🀅  🀙🀚🀛  🀔🀔🀔  +  🀆🀆"),
            "🌬️ Ada 4 set kembar Angin lengkap (T, S, B, U)": (12, 22, "4 BLESSINGS (BIG 4 WINDS)", 
                "🀀🀀🀀  🀁🀁🀁  🀂🀂🀂  🀃🀃🀃  +  🀄🀄"),
            "🌪️ Ada 3 set kembar Angin + 1 pasang (Pair) Angin": (10, 20, "SMALL FOUR WINDS", 
                "🀀🀀🀀  🀁🀁🀁  🀂🀂🀂  🀙🀚🀛  +  🀃🀃"),
            "👯 Terdiri dari 7 pasang keping yang berbeda (7 Pair)": (10, 20, "SEVEN PAIRS", 
                "🀙🀙  🀔🀔  🀝🀝  🀇🀇  🀀🀀  🀄🀄  🀁🀁"),
            "🛑 Isinya HANYA angka 1, angka 9, dan tulisan huruf saja": (3, 3, "MIXED TERMINALS", 
                "🀙🀙🀙  🀡🀡🀡  🀀🀀🀀  🀄🀄🀄  +  🀁🀁"),
            "⛔ Isinya MURNI hanya angka 1 dan angka 9 (tanpa huruf)": (10, 20, "ALL TERMINALS", 
                "🀙🀙🀙  🀡🀡🀡  🀐🀐🀐  🀘🀘🀘  +  🀇🀇"),
            "⛩️ Formasi rahasia 111-2345678-999 satu warna": (12, 22, "NINE GATES", 
                "🀙🀙🀙 🀚🀛🀜 🀝🀞🀟 🀠 🀡🀡🀡  +  🀚"),
            "🌟 Keping ujung (1, 9, angin, naga) beda-beda semua": (15, 25, "13 ORPHANS", 
                "🀙 🀡 🀐 🀘 🀇 🀏 🀀 🀁 🀂 🀃 🀄 🀅 🀆  +  🀄"),
            "👼 Keping langsung menang dari pembagian awal": (15, 25, "TIANHU / DI HU", 
                "(Kondisi Instan dari Bandar/Buangan Pertama)")
        }

    def hitung_skor(self, ciri_keping, jumlah_joker, bonus_lain, is_batal):
        if is_batal:
            return -30, "🚨 PENALTI FALSE HU! Karena poin kurang dari 3 atau salah panggil, Anda didenda 30 poin."

        data_hand = self.katalog_visual[ciri_keping]
        poin_joker, poin_murni, nama_resmi = data_hand[0], data_hand[1], data_hand[2]
        
        pakai_joker = jumlah_joker > 0
        skor = 0

        if poin_joker != poin_murni:
            skor = poin_joker if pakai_joker else poin_murni
        else:
            skor = poin_joker
            if not pakai_joker:
                skor += 2 

        skor += jumlah_joker
        skor += bonus_lain
        return skor, nama_resmi

# --- TAMPILAN APLIKASI (UI) ---
st.set_page_config(page_title="Kalkulator Mahjong Pemula", layout="centered", page_icon="🀄")

# --- SIDEBAR: ASISTEN PEMULA ---
with st.sidebar:
    st.header("📖 Kamus Contekan")
    st.write("Lupa cara baca keping? Intip di sini diam-diam:")
    with st.expander("🔢 Keping Angka Kanji (Karakter)"):
        st.markdown("- **一** = 1  |  **二** = 2  |  **三** = 3\n- **四** = 4  |  **伍** = 5  |  **六** = 6\n- **七** = 7  |  **八** = 8  |  **九** = 9")
    with st.expander("🧭 Keping Angin & Naga"):
        st.markdown("- **東** = Timur (East)\n- **南** = Selatan (South)\n- **西** = Barat (West)\n- **北** = Utara (North)")
        st.divider()
        st.markdown("- **中 (Merah)** = Naga Merah\n- **發 (Hijau)** = Naga Hijau\n- **Kotak Kosong** = Naga Putih")

st.title("🀄 Kalkulator Mahjong J2")
st.markdown("*(Dilengkapi dengan Visualizer Kombinasi Keping)*")

app = KalkulatorPemulaJ2()

# -- KOTAK 1: BENTUK KEPING & PREVIEW VISUAL --
st.success("### TAHAP 1: Ciri-ciri Keping Anda")
ciri_pilihan = st.selectbox(
    "Pilih deskripsi yang paling cocok dengan formasi di meja:", 
    list(app.katalog_visual.keys())
)

# Menampilkan gambar preview dari pilihan di atas
contoh_visual = app.katalog_visual[ciri_pilihan][3]
st.markdown("💡 **Contoh Bentuk Kepingnya:**")
st.markdown(f"<div style='text-align: center; background-color: #f0f2f6; padding: 15px; border-radius: 10px;'><span style='font-size: 32px;'>{contoh_visual}</span></div>", unsafe_allow_html=True)
st.write("")

# -- KOTAK 2: PENGGUNAAN JOKER & MENANG --
st.info("### TAHAP 2: Penggunaan Joker & Status")
col1, col2 = st.columns(2)
with col1:
    jumlah_joker = st.number_input("Berapa keping Joker yang dipakai?", min_value=0, max_value=4, value=0)
with col2:
    cara_menang = st.radio("Dapat keping terakhir dari mana?", ["RON (Buangan teman)", "ZIMO (Ambil sendiri)"])

# -- KOTAK 3: BONUS MUDAH --
st.warning("### TAHAP 3: Tambahan Poin (Opsional)")
st.write("Centang jika keping Anda memiliki unsur ini:")
bonus_total = 0
if st.checkbox("Mempunyai set 3-kembar tulisan NAGA (+1/set)"): bonus_total += 1
if st.checkbox("Mempunyai set 3-kembar tulisan ANGIN yang sesuai meja/kursi (+1)"): bonus_total += 1
if st.checkbox("Dua keping penutup (Mata) adalah keping angka 2 atau 8 (+1)"): bonus_total += 1
if st.checkbox("Punya Bunga Merah/Hitam yang cocok dengan kursi (+2 atau +1)"): bonus_total += 1
if st.checkbox("Punya FULL SET 4 Bunga (+5 / +7)"): bonus_total += 5

is_batal = st.checkbox("🚨 Kena Penalti (Batal Menang karena ketahuan salah susun / Poin < 3)")

st.divider()

# -- FITUR TOMBOL GANDA (CEK VS HITUNG) --
st.markdown("### TAHAP 4: Eksekusi")
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    cek_btn = st.button("🔍 CEK AMAN NGGAK? (Simulasi)", use_container_width=True)
with col_btn2:
    hitung_btn = st.button("🧮 SAH! HITUNG TAGIHAN", type="primary", use_container_width=True)

# -- LOGIKA TOMBOL --
if cek_btn:
    skor_akhir, nama_kombinasi = app.hitung_skor(ciri_pilihan, jumlah_joker, bonus_total, is_batal)
    if is_batal:
        st.error("Anda mencentang kotak penalti!")
    elif skor_akhir < 3:
        st.error(f"🛑 **SSTT! Jangan teriak menang!** Poin Anda baru **{skor_akhir}**. Butuh minimal 3 poin.")
    else:
        st.success(f"✅ **AMAN! Gas teriak MAHJONG!** Poin Anda sudah mencapai **{skor_akhir}**.")

if hitung_btn:
    skor_akhir, nama_kombinasi = app.hitung_skor(ciri_pilihan, jumlah_joker, bonus_total, is_batal)
    if is_batal or skor_akhir < 3:
        st.error(f"❌ **TIDAK SAH MENANG!** Skor total Anda cuma: **{skor_akhir} Poin**. Anda terkena penalti False Hu.")
    else:
        st.balloons()
        st.success(f"# 🎉 SKOR SAH: {skor_akhir} POIN")
        st.markdown(f"*(Sistem mendeteksi kombinasi Anda sebagai: **{nama_kombinasi}**)*")
        st.markdown("### 💰 TAGIHAN PEMBAYARAN CIP:")
        if cara_menang == "RON (Buangan teman)":
            st.info(f"😡 **Teman yang membuang keping terakhir** harus bayar **{skor_akhir * 2} Cip** (Denda 2x).")
            st.info(f"😰 **Dua teman lainnya** masing-masing cukup bayar **{skor_akhir} Cip**.")
        else:
            st.info(f"😭 Karena Anda ambil sendiri dari tumpukan (Zimo), **KETIGA TEMAN ANDA** masing-masing wajib bayar **{skor_akhir * 2} Cip**.")