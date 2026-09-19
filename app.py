import streamlit as st

# --- SERVER MEMORY (DATABASE SEMENTARA) ---
@st.cache_resource
def get_room_database():
    return {}

db_room = get_room_database()

# --- FUNGSI 1: GAMBAR DARI SERVER ALTERNATIF (ANTI BLOKIR) ---
def get_tile(tile_code, width=45):
    # Menggunakan raw.github yang lebih stabil daripada jsdelivr
    base_url = "https://raw.githubusercontent.com/FluffyStuff/mahjong-tiles/master/svg/"
    return f"<img src='{base_url}{tile_code}.svg' width='{width}' style='vertical-align: middle; border-radius: 4px; box-shadow: 1px 2px 4px rgba(0,0,0,0.3); margin-right: 5px;'>"

# --- FUNGSI 2: KEPING DIGITAL CSS (100% OFFLINE, WARNA JELAS) ---
def css_tile(char, color="#111", bottom_text=""):
    """Menciptakan kotak keping Mahjong murni dari kode tanpa perlu donwload gambar"""
    sub_html = f"<div style='color: #c0392b; font-size: 11px; margin-top: 1px;'>{bottom_text}</div>" if bottom_text else ""
    return f"""
    <div style='display:inline-flex; flex-direction: column; align-items: center; justify-content: center; border: 1px solid #aaa; border-radius: 5px; background: linear-gradient(180deg, #ffffff 0%, #e6e6e6 100%); padding: 4px 8px; box-shadow: 1px 2px 4px rgba(0,0,0,0.3); min-width: 32px; vertical-align: middle;'>
        <span style='color: {color}; font-size: 24px; font-weight: bold; line-height: 1.1; font-family: "Microsoft YaHei", "PingFang SC", sans-serif;'>{char}</span>
        {sub_html}
    </div>
    """

def render_css_row(items):
    html = "<div style='margin-bottom: 12px; display: flex; align-items: center;'>"
    for tile_html, text in items:
        html += f"<div style='margin-right: 15px; display: flex; align-items: center;'>{tile_html} <span style='font-size: 16px; font-weight: bold; margin-left: 8px;'>= {text}</span></div>"
    html += "</div>"
    return html

def tampilkan_kombinasi(teks_simbol):
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
            return -30, "🚨 PENALTI FALSE HU! Denda 30 poin karena poin kurang/salah."
        data_hand = self.katalog_visual[ciri_keping]
        poin_joker, poin_murni, nama_resmi = data_hand[0], data_hand[1], data_hand[2]
        pakai_joker = jumlah_joker > 0
        skor = poin_joker if (poin_joker != poin_murni and pakai_joker) else poin_murni
        if poin_joker == poin_murni and not pakai_joker:
            skor += 2 
        return skor + jumlah_joker + bonus_lain, nama_resmi

# --- TAMPILAN APLIKASI (UI) ---
st.set_page_config(page_title="Kasir Mahjong J2", layout="centered", page_icon="🀄")

# --- SIDEBAR: KAMUS (MENGGUNAKAN CSS DIGITAL TILES) ---
with st.sidebar:
    st.header("📖 Kamus Contekan")
    
    st.markdown("**Angka Kanji (Karakter)**")
    st.markdown(render_css_row([
        (css_tile("一", bottom_text="萬"), "1"), 
        (css_tile("二", bottom_text="萬"), "2"), 
        (css_tile("三", bottom_text="萬"), "3")
    ]), unsafe_allow_html=True)
    st.markdown(render_css_row([
        (css_tile("四", bottom_text="萬"), "4"), 
        (css_tile("五", bottom_text="萬"), "5"), 
        (css_tile("六", bottom_text="萬"), "6")
    ]), unsafe_allow_html=True)
    st.markdown(render_css_row([
        (css_tile("七", bottom_text="萬"), "7"), 
        (css_tile("八", bottom_text="萬"), "8"), 
        (css_tile("九", bottom_text="萬"), "9")
    ]), unsafe_allow_html=True)
    
    st.divider()
    st.markdown("**Arah Angin**")
    st.markdown(render_css_row([
        (css_tile("東", "#2c3e50"), "Timur"), 
        (css_tile("南", "#2c3e50"), "Selatan")
    ]), unsafe_allow_html=True)
    st.markdown(render_css_row([
        (css_tile("西", "#2c3e50"), "Barat"), 
        (css_tile("北", "#2c3e50"), "Utara")
    ]), unsafe_allow_html=True)
    
    st.divider()
    st.markdown("**Naga (Dragon)**")
    # Teks langsung diwarnai merah dan hijau sesuai karakter aslinya
    st.markdown(render_css_row([
        (css_tile("中", color="#c0392b"), "Merah"), 
        (css_tile("發", color="#27ae60"), "Hijau")
    ]), unsafe_allow_html=True)
    st.markdown(render_css_row([
        (css_tile("白", color="#2980b9"), "Putih")
    ]), unsafe_allow_html=True)


# --- SISTEM LOGIN ROOM ---
st.title("🀄 Mahjong J2 - Digital Ledger")

room_input = st.text_input("🔑 Masukkan Kode Meja (Contoh: VIP-1, MEJA-A):", "").upper()

if not room_input:
    st.info("Silakan buat atau masukkan kode meja untuk mulai mencatat skor.")
else:
    if room_input not in db_room:
        db_room[room_input] = {"Timur": 1000, "Selatan": 1000, "Barat": 1000, "Utara": 1000}
    
    st.success(f"Berada di Room: **{room_input}**")
    
    st.markdown("### 🏦 Saldo Cip Meja")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Timur", db_room[room_input]["Timur"])
    c2.metric("Selatan", db_room[room_input]["Selatan"])
    c3.metric("Barat", db_room[room_input]["Barat"])
    c4.metric("Utara", db_room[room_input]["Utara"])
    
    if st.button("🔄 Segarkan Saldo Papan (Sync)"):
        st.rerun()

    st.divider()

    # --- KALKULATOR UTAMA ---
    app = KalkulatorPemulaJ2()

    st.markdown("### 🧮 Kalkulator Kemenangan")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        pemenang = st.selectbox("👑 Siapa yang menang?", ["Timur", "Selatan", "Barat", "Utara"])
    with col_p2:
        cara_menang = st.radio("⚔️ Menang dari mana?", ["RON (Buangan lawan)", "ZIMO (Ambil sendiri)"])

    if cara_menang == "RON (Buangan lawan)":
        opsi_kalah = ["Timur", "Selatan", "Barat", "Utara"]
        opsi_kalah.remove(pemenang)
        pembuang = st.selectbox("🎯 Siapa pembuang keping terakhir? (Kena 2x Lipat)", opsi_kalah)

    st.write("")
    ciri_pilihan = st.selectbox("Ciri-ciri kombinasi keping pemenang:", list(app.katalog_visual.keys()))
    st.markdown(tampilkan_kombinasi(app.katalog_visual[ciri_pilihan][3]), unsafe_allow_html=True)
    
    st.write("")
    col_j, col_b = st.columns(2)
    with col_j:
        jumlah_joker = st.number_input("Jumlah Joker dipakai:", 0, 4, 0)
    with col_b:
        bonus_total = 0
        if st.checkbox("Set 3-kembar NAGA (+1)"): bonus_total += 1
        if st.checkbox("Set 3-kembar ANGIN sesuai kursi (+1)"): bonus_total += 1
        if st.checkbox("Penutup Mata angka 2 atau 8 (+1)"): bonus_total += 1
        if st.checkbox("Bunga sesuai kursi (+1/+2)"): bonus_total += 1
        if st.checkbox("FULL 4 Bunga (+5)"): bonus_total += 5

    is_batal = st.checkbox("🚨 Batal Menang (Penalti False Hu)")

    st.divider()

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        cek_btn = st.button("🔍 CEK AMAN NGGAK?", use_container_width=True)
    with col_btn2:
        hitung_btn = st.button("🧮 SAH! POTONG SALDO", type="primary", use_container_width=True)

    if cek_btn:
        skor, nama = app.hitung_skor(ciri_pilihan, jumlah_joker, bonus_total, is_batal)
        if skor < 3: st.error(f"🛑 Jangan teriak menang! Poin baru {skor}.")
        else: st.success(f"✅ Aman! Poin mencapai {skor}.")

    if hitung_btn:
        skor, nama = app.hitung_skor(ciri_pilihan, jumlah_joker, bonus_total, is_batal)
        
        if is_batal or skor < 3:
            st.error(f"❌ TIDAK SAH! Poin cuma {skor}. Penalti False Hu -30 poin dijatuhkan ke {pemenang}.")
            for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                if kursi == pemenang:
                    db_room[room_input][kursi] -= 30
                else:
                    db_room[room_input][kursi] += 10
            st.rerun()

        else:
            st.balloons()
            st.success(f"🎉 {pemenang} MENANG! ({nama}: {skor} Poin)")
            
            if cara_menang == "RON (Buangan lawan)":
                for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                    if kursi == pemenang:
                        db_room[room_input][kursi] += (skor * 2) + (skor * 1) + (skor * 1)
                    elif kursi == pembuang:
                        db_room[room_input][kursi] -= (skor * 2) 
                    else:
                        db_room[room_input][kursi] -= skor 
            else: 
                for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                    if kursi == pemenang:
                        db_room[room_input][kursi] += (skor * 2 * 3)
                    else:
                        db_room[room_input][kursi] -= (skor * 2) 
            
            st.rerun()