import streamlit as st

# --- FUNGSI HELPER UNTUK GAMBAR BERWARNA ---
def get_tile(tile_code, width=45):
    """Mengambil gambar keping satuan yang berwarna dan tajam"""
    base_url = "https://cdn.jsdelivr.net/gh/FluffyStuff/mahjong-tiles@master/svg/"
    return f"<img src='{base_url}{tile_code}.svg' width='{width}' style='vertical-align: middle; border-radius: 4px; box-shadow: 1px 2px 4px rgba(0,0,0,0.3); margin-right: 5px;'>"

def render_row(items):
    """Merapikan baris gambar dan teks agar teksnya berukuran normal"""
    html = "<div style='margin-bottom: 15px; display: flex; align-items: center;'>"
    for code, text in items:
        html += f"<div style='margin-right: 20px;'>{get_tile(code)} <span style='font-size: 16px; font-weight: bold; vertical-align: middle;'>= {text}</span></div>"
    html += "</div>"
    return html

def tampilkan_kombinasi(teks_simbol):
    """Mengubah simbol di formasi menjadi gambar berwarna untuk preview"""
    TILE_URLS = {
        '🀙': 'Pin1', '🀚': 'Pin2', '🀛': 'Pin3', '🀜': 'Pin4', '🀝': 'Pin5', '🀞': 'Pin6', '🀟': 'Pin7', '🀠': 'Pin8', '🀡': 'Pin9',
        '🀐': 'Sou1', '🀑': 'Sou2', '🀒': 'Sou3', '🀓': 'Sou4', '🀔': 'Sou5', '🀕': 'Sou6', '🀖': 'Sou7', '🀗': 'Sou8', '🀘': 'Sou9',
        '🀇': 'Man1', '🀈': 'Man2', '🀉': 'Man3', '🀊': 'Man4', '🀋': 'Man5', '🀌': 'Man6', '🀍': 'Man7', '🀎': 'Man8', '🀏': 'Man9',
        '🀀': 'Ton', '🀁': 'Nan', '🀂': 'Sha', '🀃': 'Pei',
        '🀄': 'Chun', '🀅': 'Hatsu', '🀆': 'Haku'
    }
    
    html = "<div style='display: flex; align-items: center; flex-wrap: wrap; background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ddd;'>"
    for char in teks_simbol:
        if char in TILE_URLS:
            html += get_tile(TILE_URLS[char], width=35)
        elif char == ' ':
            html += "<div style='width: 10px;'></div>"
        elif char == '+':
            html += "<div style='margin: 0 10px; font-weight: bold; font-size: 20px; color: #555;'>+</div>"
        else:
            html += f"<span style='font-size: 16px; margin-left: 10px;'>{char}</span>"
    html += "</div>"
    return html

class KalkulatorPemulaJ2:
    def __init__(self):
        # Format: "Bahasa Awam": (Poin Joker, Poin Murni, "Nama Resmi", "KODE TEKS UNTUK DIUBAH JADI GAMBAR")
        self.katalog_visual = {
            "🔀 Campur aduk (Ada seri, ada kembar, beda warna)": (0, 0, "CHICKEN HAND", "🀙🀚🀛  🀔🀔🀔  🀝🀞🀟  🀇🀈🀉  +  🀀🀀"),
            "🔢 Semuanya berupa susunan SERI BERURUTAN (Chow)": (2, 2, "ALL SEQUENCES", "🀙🀚🀛  🀔🀕🀖  🀝🀞🀟  🀇🀈🀉  +  🀀🀀"),
            "🀄 Semuanya berupa 3-KEMBAR (Pong)": (3, 3, "ALL TRIPLETS", "🀙🀙🀙  🀔🀔🀔  🀄🀄🀄  🀇🀇🀇  +  🀀🀀"),
            "🧱 Semuanya berupa 4-KEMBAR (Kong)": (15, 25, "ALL QUADRUPLETS", "🀙🀙🀙🀙  🀔🀔🀔🀔  🀄🀄🀄🀄  🀇🀇🀇🀇  +  🀀🀀"),
            "🎨 Warnanya MURNI SATU JENIS saja (Tanpa huruf)": (10, 20, "FULL COLOUR", "🀙🀚🀛  🀙🀙🀙  🀝🀞🀟  🀡🀡🀡  +  🀠🀠"),
            "🖌️ Satu warna dasar, TAPI dicampur tulisan Naga/Angin": (4, 4, "MIXED / SEMI FLUSH", "🀙🀚🀛  🀙🀙🀙  🀝🀞🀟  🀄🀄🀄  +  🀀🀀"),
            "👑 Murni hanya keping tulisan NAGA dan ANGIN saja": (10, 20, "ALL HONOURS", "🀀🀀🀀  🀁🀁🀁  🀄🀄🀄  🀆🀆🀆  +  🀅🀅"),
            "🐉 Ada 3 set kembar Naga komplit (Merah, Hijau, Putih)": (10, 20, "3 SCHOLARS (BIG 3 DRAGONS)", "🀄🀄🀄  🀅🀅🀅  🀆🀆🀆  🀙🀚🀛  +  🀀🀀"),
            "🐲 Ada 2 set kembar Naga + 1 pasang (Pair) Naga": (5, 5, "SMALL THREE DRAGONS", "🀄🀄🀄  🀅🀅🀅  🀙🀚🀛  🀔🀔🀔  +  🀆🀆"),
            "🌬️ Ada 4 set kembar Angin lengkap (T, S, B, U)": (12, 22, "4 BLESSINGS (BIG 4 WINDS)", "🀀🀀🀀  🀁🀁🀁  🀂🀂🀂  🀃🀃🀃  +  🀄🀄"),
            "🌪️ Ada 3 set kembar Angin + 1 pasang (Pair) Angin": (10, 20, "SMALL FOUR WINDS", "🀀🀀🀀  🀁🀁🀁  🀂🀂🀂  🀙🀚🀛  +  🀃🀃"),
            "👯 Terdiri dari 7 pasang keping yang berbeda (7 Pair)": (10, 20, "SEVEN PAIRS", "🀙🀙  🀔🀔  🀝🀝  🀇🀇  🀀🀀  🀄🀄  🀁🀁"),
            "🛑 Isinya HANYA angka 1, angka 9, dan tulisan huruf saja": (3, 3, "MIXED TERMINALS", "🀙🀙🀙  🀡🀡🀡  🀀🀀🀀  🀄🀄🀄  +  🀁🀁"),
            "⛔ Isinya MURNI hanya angka 1 dan angka 9 (tanpa huruf)": (10, 20, "ALL TERMINALS", "🀙🀙🀙  🀡🀡🀡  🀐🀐🀐  🀘🀘🀘  +  🀇🀇"),
            "⛩️ Formasi rahasia 111-2345678-999 satu warna": (12, 22, "NINE GATES", "🀙🀙🀙 🀚🀛🀜 🀝🀞🀟 🀠 🀡🀡🀡  +  🀚"),
            "🌟 Keping ujung beda-beda semua (13 Orphans)": (15, 25, "13 ORPHANS", "🀙 🀡 🀐 🀘 🀇 🀏 🀀 🀁 🀂 🀃 🀄 🀅 🀆  +  🀄"),
            "👼 Keping langsung menang dari pembagian awal": (15, 25, "TIANHU / DI HU", "(Menang Instan dari Bandar)")
        }

    def hitung_skor(self, ciri_keping, jumlah_joker, bonus_lain, is_batal):
        if is_batal:
            return -30, "🚨 PENALTI FALSE HU! Anda didenda 30 poin karena poin kurang dari 3 atau batal menang."
        data_hand = self.katalog_visual[ciri_keping]
        poin_joker, poin_murni, nama_resmi = data_hand[0], data_hand[1], data_hand[2]
        pakai_joker = jumlah_joker > 0
        skor = poin_joker if (poin_joker != poin_murni and pakai_joker) else poin_murni
        if poin_joker == poin_murni and not pakai_joker:
            skor += 2 
        return skor + jumlah_joker + bonus_lain, nama_resmi

# --- TAMPILAN APLIKASI (UI) ---
st.set_page_config(page_title="Kalkulator Mahjong", layout="centered", page_icon="🀄")

# --- SIDEBAR: ASISTEN PEMULA ---
with st.sidebar:
    st.header("📖 Kamus Contekan")
    st.write("Intip arti keping di sini:")
    
    st.markdown("**Angka Kanji (Karakter)**")
    st.markdown(render_row([('Man1', '1'), ('Man2', '2'), ('Man3', '3')]), unsafe_allow_html=True)
    st.markdown(render_row([('Man4', '4'), ('Man5', '5'), ('Man6', '6')]), unsafe_allow_html=True)
    st.markdown(render_row([('Man7', '7'), ('Man8', '8'), ('Man9', '9')]), unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("**Arah Angin**")
    st.markdown(render_row([('Ton', 'Timur'), ('Nan', 'Selatan')]), unsafe_allow_html=True)
    st.markdown(render_row([('Sha', 'Barat'), ('Pei', 'Utara')]), unsafe_allow_html=True)
    
    st.divider()

    st.markdown("**Naga (Dragon)**")
    st.markdown(render_row([('Chun', 'Merah'), ('Hatsu', 'Hijau')]), unsafe_allow_html=True)
    st.markdown(render_row([('Haku', 'Putih')]), unsafe_allow_html=True)


# --- MAIN CONTENT ---
st.title("🀄 Kalkulator Mahjong J2")
st.markdown("*(Asisten Visual Cerdas)*")

app = KalkulatorPemulaJ2()

# -- KOTAK 1: BENTUK KEPING & PREVIEW VISUAL --
st.success("### TAHAP 1: Ciri-ciri Keping Anda")
ciri_pilihan = st.selectbox(
    "Pilih deskripsi yang paling cocok dengan formasi di meja:", 
    list(app.katalog_visual.keys())
)

contoh_visual_teks = app.katalog_visual[ciri_pilihan][3]
st.markdown("💡 **Preview Bentuk Keping:**")
st.markdown(tampilkan_kombinasi(contoh_visual_teks), unsafe_allow_html=True)
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
bonus_total = 0
if st.checkbox("Punya set 3-kembar NAGA (+1/set)"): bonus_total += 1
if st.checkbox("Punya set 3-kembar ANGIN sesuai meja/kursi (+1)"): bonus_total += 1
if st.checkbox("Dua keping penutup (Mata) adalah keping angka 2 atau 8 (+1)"): bonus_total += 1
if st.checkbox("Punya Bunga Merah/Hitam yang cocok dengan kursi (+2 atau +1)"): bonus_total += 1
if st.checkbox("Punya FULL SET 4 Bunga (+5 / +7)"): bonus_total += 5

is_batal = st.checkbox("🚨 Kena Penalti (Batal Menang karena poin < 3)")
st.divider()

# -- FITUR TOMBOL GANDA --
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    cek_btn = st.button("🔍 CEK AMAN NGGAK?", use_container_width=True)
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
        st.markdown(f"*(Kombinasi Anda: **{nama_kombinasi}**)*")
        st.markdown("### 💰 TAGIHAN PEMBAYARAN CIP:")
        if cara_menang == "RON (Buangan teman)":
            st.info(f"😡 **Teman yang membuang keping terakhir** bayar **{skor_akhir * 2} Cip** (Denda 2x).")
            st.info(f"😰 **Dua teman lainnya** bayar **{skor_akhir} Cip**.")
        else:
            st.info(f"😭 Karena Anda ambil sendiri dari tumpukan (Zimo), **KETIGA TEMAN ANDA** bayar **{skor_akhir * 2} Cip**.")