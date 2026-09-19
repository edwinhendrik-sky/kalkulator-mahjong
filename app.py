import streamlit as st

class KalkulatorPemulaJ2:
    def __init__(self):
        # Mapping dari "Bahasa Awam (Visual)" ke "Aturan Skor J2"
        # Format: "Pertanyaan Awam": (Poin Pakai Joker, Poin Tanpa Joker, "Nama Resmi Hand")
        self.katalog_visual = {
            "🔀 Campur aduk (Ada seri, ada kembar, beda-beda warna)": (0, 0, "CHICKEN HAND"),
            "🔢 Semuanya berupa susunan SERI BERURUTAN (contoh: 1-2-3, 5-6-7)": (2, 2, "ALL SEQUENCES"),
            "🀄 Semuanya berupa 3-KEMBAR (tidak ada yang seri berurutan)": (3, 3, "ALL TRIPLETS"),
            "🧱 Semuanya berupa 4-KEMBAR (Pemain melakukan 4x Kong)": (15, 25, "ALL QUADRUPLETS"),
            "🎨 Warnanya MURNI SATU JENIS saja (tanpa ada campuran tulisan/angin)": (10, 20, "FULL COLOUR"),
            "🖌️ Satu jenis warna saja, TAPI dicampur tulisan Naga/Angin": (4, 4, "MIXED / SEMI FLUSH"),
            "👑 Semuanya murni hanya keping tulisan NAGA dan ANGIN saja": (10, 20, "ALL HONOURS"),
            "🐉 Ada 3 set kembar Naga (Merah + Hijau + Putih)": (10, 20, "3 SCHOLARS (BIG 3 DRAGONS)"),
            "🐲 Ada 2 set kembar Naga + 1 pasang (Pair) Naga": (5, 5, "SMALL THREE DRAGONS"),
            "🌬️ Ada 4 set kembar Angin lengkap (Timur, Selatan, Barat, Utara)": (12, 22, "4 BLESSINGS (BIG 4 WINDS)"),
            "🌪️ Ada 3 set kembar Angin + 1 pasang (Pair) Angin": (10, 20, "SMALL FOUR WINDS"),
            "👯 Terdiri dari 7 pasang keping yang berbeda (7 Pair)": (10, 20, "SEVEN PAIRS"),
            "🛑 Isinya HANYA angka 1, angka 9, dan tulisan huruf saja": (3, 3, "MIXED TERMINALS"),
            "⛔ Isinya MURNI hanya angka 1 dan angka 9 (tanpa huruf)": (10, 20, "ALL TERMINALS"),
            "⛩️ Susunan rahasia 111-2345678-999 satu warna (Nine Gates)": (12, 22, "NINE GATES"),
            "🌟 Keping ujung (1, 9, angin, naga) beda-beda semua (13 Orphans)": (15, 25, "13 ORPHANS"),
            "👼 Keping langsung menang dari pembagian awal (Bandar/Pemain)": (15, 25, "TIANHU / DI HU")
        }

    def hitung_skor(self, ciri_keping, jumlah_joker, bonus_lain, is_batal):
        if is_batal:
            return -30, "🚨 PENALTI! Karena poin kurang dari 3 atau salah panggil, Anda didenda 30 poin."

        data_hand = self.katalog_visual[ciri_keping]
        poin_joker, poin_murni, nama_resmi = data_hand[0], data_hand[1], data_hand[2]
        
        pakai_joker = jumlah_joker > 0
        skor = 0

        # Penentuan Poin Dasar
        if poin_joker != poin_murni:
            skor = poin_joker if pakai_joker else poin_murni
        else:
            skor = poin_joker
            if not pakai_joker:
                skor += 2  # Dapat bonus murni +2 jika tidak pakai joker di hand biasa

        # Tambah poin per keping joker
        skor += jumlah_joker
        
        # Tambah poin per bonus centang
        skor += bonus_lain

        return skor, nama_resmi

# --- TAMPILAN APLIKASI (UI) ---
st.set_page_config(page_title="Kalkulator Mahjong Pemula", layout="centered")
st.title("🀄 Kalkulator Mahjong (Bebas Pusing)")
st.markdown("Tidak perlu hafal istilah Mahjong. Cukup jawab pertanyaan tentang bentuk ubin pemenang di bawah ini!")

app = KalkulatorPemulaJ2()

# -- KOTAK 1: BENTUK KEPING --
st.success("### TAHAP 1: Ciri-ciri Keping Anda")
ciri_pilihan = st.selectbox(
    "Pilih deskripsi yang paling cocok dengan 14 keping pemenang (Pilih yang nilainya paling sulit jika memenuhi 2 syarat):", 
    list(app.katalog_visual.keys())
)

# -- KOTAK 2: PENGGUNAAN JOKER & MENANG --
st.info("### TAHAP 2: Bantuan & Status")
col1, col2 = st.columns(2)
with col1:
    jumlah_joker = st.number_input("Berapa keping Joker yang dipakai?", 0, 4, 0)
with col2:
    cara_menang = st.radio("Dapat keping terakhir dari mana?", ["RON (Buangan teman)", "ZIMO (Ambil sendiri)"])

# -- KOTAK 3: BONUS MUDAH --
st.warning("### TAHAP 3: Tambahan Poin (Boleh dilewati)")
st.write("Centang jika keping Anda memiliki unsur ini:")

bonus_total = 0

if st.checkbox("Mempunyai set 3-kembar tulisan NAGA (+1/set)"): bonus_total += 1
if st.checkbox("Mempunyai set 3-kembar tulisan ANGIN yang sesuai meja/kursi (+1)"): bonus_total += 1
if st.checkbox("Dua keping penutup (Mata) adalah keping angka 2 atau 8 (+1)"): bonus_total += 1
if st.checkbox("Punya Bunga Merah/Hitam yang cocok dengan kursi (+2 atau +1)"): bonus_total += 1
if st.checkbox("Punya FULL SET 4 Bunga (+5 / +7)"): bonus_total += 5

is_batal = st.checkbox("🚨 Batal Menang (Ketahuan salah susun / Poin kurang dari 3)")

st.divider()

# -- HASIL --
if st.button("🧮 HITUNG PEMBAYARAN", type="primary", use_container_width=True):
    skor_akhir, nama_kombinasi = app.hitung_skor(ciri_pilihan, jumlah_joker, bonus_total, is_batal)
    
    if is_batal:
        st.error(nama_kombinasi) # Ini akan menampilkan pesan penalti
    elif skor_akhir < 3:
        st.error(f"Skor total Anda cuma: **{skor_akhir} Poin**.\n\n❌ **GAGAL MENANG!** Aturan J2 mewajibkan minimal 3 poin (termasuk bonus) agar sah untuk teriak menang. Anda terkena penalti False Hu.")
    else:
        st.balloons()
        st.success(f"# SKOR SAH: {skor_akhir} POIN")
        st.markdown(f"*(Sistem mendeteksi kombinasi Anda sebagai: **{nama_kombinasi}**)*")
        
        st.markdown("### 💰 TAGIHAN PEMBAYARAN CIP:")
        if cara_menang == "RON (Buangan teman)":
            st.write(f"😡 **Teman yang membuang keping terakhir** harus bayar **{skor_akhir * 2} Cip** (Kena denda 2x lipat).")
            st.write(f"😰 **Dua teman lainnya** masing-masing cukup bayar **{skor_akhir} Cip**.")
        else:
            st.write(f"😭 Karena Anda ambil sendiri dari tumpukan, **KETIGA TEMAN ANDA** masing-masing wajib bayar **{skor_akhir * 2} Cip** (Kena denda 2x lipat semua).")