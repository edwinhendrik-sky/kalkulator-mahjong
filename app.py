import streamlit as st
import os
import base64

# --- DATABASE SEMENTARA ---
@st.cache_resource
def get_room_database():
    return {}

db_room = get_room_database()

# --- FUNGSI BACA GAMBAR LOKAL (SUPER CEPAT & OFFLINE) ---
def get_local_tile(nama_file, width=35):
    filepath = f"assets/{nama_file}.svg"
    if os.path.exists(filepath):
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"<img src='data:image/svg+xml;base64,{encoded_string}' width='{width}' style='vertical-align: middle; border-radius: 4px; box-shadow: 1px 2px 4px rgba(0,0,0,0.3); margin-right: 3px;'>"
    else:
        # Cadangan jika gambar gagal didownload
        return f"<div style='display:inline-block; width:{width}px; height:{(width*1.3)}px; border:1px solid #999; background:#eee; margin-right:3px;'></div>"

def render_formasi(simbol_list):
    html = "<div style='display: flex; align-items: center; flex-wrap: wrap; background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ddd;'>"
    for item in simbol_list:
        if item == ' ':
            html += "<div style='width: 10px;'></div>"
        elif item == '+':
            html += "<div style='margin: 0 10px; font-weight: bold; font-size: 24px; color: #555;'>+</div>"
        elif item.startswith("Teks:"):
            teks = item.replace("Teks:", "")
            html += f"<span style='font-size: 16px; margin-left: 10px; font-weight:bold;'>{teks}</span>"
        else:
            html += get_local_tile(item)
    html += "</div>"
    return html

class KalkulatorPemulaJ2:
    def __init__(self):
        # Format: "Bahasa Awam": (Poin Joker, Poin Murni, "Nama Resmi", [Daftar File Gambar Lokal])
        self.katalog_visual = {
            "🔀 Campur aduk (Ada seri, ada kembar, beda warna)": (0, 0, "CHICKEN HAND", 
                ['Pin1','Pin2','Pin3',' ','Sou5','Sou5','Sou5',' ','Pin5','Pin6','Pin7',' ','Man1','Man2','Man3','+','Ton','Ton']),
            "🔢 Semuanya berupa susunan SERI BERURUTAN (Chow)": (2, 2, "ALL SEQUENCES", 
                ['Pin1','Pin2','Pin3',' ','Sou4','Sou5','Sou6',' ','Pin5','Pin6','Pin7',' ','Man1','Man2','Man3','+','Ton','Ton']),
            "🀄 Semuanya berupa 3-KEMBAR (Pong)": (3, 3, "ALL TRIPLETS", 
                ['Pin1','Pin1','Pin1',' ','Sou5','Sou5','Sou5',' ','Chun','Chun','Chun',' ','Man1','Man1','Man1','+','Ton','Ton']),
            "🧱 Semuanya berupa 4-KEMBAR (Kong)": (15, 25, "ALL QUADRUPLETS", 
                ['Pin1','Pin1','Pin1','Pin1',' ','Sou5','Sou5','Sou5','Sou5',' ','Chun','Chun','Chun','Chun',' ','Man1','Man1','Man1','Man1','+','Ton','Ton']),
            "🎨 Warnanya MURNI SATU JENIS saja (Tanpa huruf)": (10, 20, "FULL COLOUR", 
                ['Pin1','Pin2','Pin3',' ','Pin1','Pin1','Pin1',' ','Pin5','Pin6','Pin7',' ','Pin9','Pin9','Pin9','+','Pin8','Pin8']),
            "🖌️ Satu warna dasar, TAPI dicampur tulisan Naga/Angin": (4, 4, "MIXED / SEMI FLUSH", 
                ['Pin1','Pin2','Pin3',' ','Pin1','Pin1','Pin1',' ','Pin5','Pin6','Pin7',' ','Chun','Chun','Chun','+','Ton','Ton']),
            "👑 Murni hanya keping tulisan NAGA dan ANGIN saja": (10, 20, "ALL HONOURS", 
                ['Ton','Ton','Ton',' ','Nan','Nan','Nan',' ','Chun','Chun','Chun',' ','Haku','Haku','Haku','+','Hatsu','Hatsu']),
            "🐉 Ada 3 set kembar Naga komplit (Merah, Hijau, Putih)": (10, 20, "3 SCHOLARS (BIG 3 DRAGONS)", 
                ['Chun','Chun','Chun',' ','Hatsu','Hatsu','Hatsu',' ','Haku','Haku','Haku',' ','Pin1','Pin2','Pin3','+','Ton','Ton']),
            "🐲 Ada 2 set kembar Naga + 1 pasang (Pair) Naga": (5, 5, "SMALL THREE DRAGONS", 
                ['Chun','Chun','Chun',' ','Hatsu','Hatsu','Hatsu',' ','Pin1','Pin2','Pin3',' ','Sou5','Sou5','Sou5','+','Haku','Haku']),
            "🌬️ Ada 4 set kembar Angin lengkap (T, S, B, U)": (12, 22, "4 BLESSINGS (BIG 4 WINDS)", 
                ['Ton','Ton','Ton',' ','Nan','Nan','Nan',' ','Sha','Sha','Sha',' ','Pei','Pei','Pei','+','Chun','Chun']),
            "🌪️ Ada 3 set kembar Angin + 1 pasang (Pair) Angin": (10, 20, "SMALL FOUR WINDS", 
                ['Ton','Ton','Ton',' ','Nan','Nan','Nan',' ','Sha','Sha','Sha',' ','Pin1','Pin2','Pin3','+','Pei','Pei']),
            "👯 Terdiri dari 7 pasang keping yang berbeda (7 Pair)": (10, 20, "SEVEN PAIRS", 
                ['Pin1','Pin1',' ','Sou5','Sou5',' ','Pin5','Pin5',' ','Man1','Man1',' ','Ton','Ton',' ','Chun','Chun',' ','Nan','Nan']),
            "🛑 HANYA angka 1, angka 9, dan tulisan huruf saja": (3, 3, "MIXED TERMINALS", 
                ['Pin1','Pin1','Pin1',' ','Pin9','Pin9','Pin9',' ','Ton','Ton','Ton',' ','Chun','Chun','Chun','+','Nan','Nan']),
            "⛔ MURNI hanya angka 1 dan angka 9 (tanpa huruf)": (10, 20, "ALL TERMINALS", 
                ['Pin1','Pin1','Pin1',' ','Pin9','Pin9','Pin9',' ','Sou1','Sou1','Sou1',' ','Sou9','Sou9','Sou9','+','Man1','Man1']),
            "⛩️ Formasi rahasia 111-2345678-999 satu warna": (12, 22, "NINE GATES", 
                ['Pin1','Pin1','Pin1',' ','Pin2','Pin3','Pin4','Pin5','Pin6','Pin7','Pin8',' ','Pin9','Pin9','Pin9','+','Pin2']),
            "🌟 Keping ujung beda-beda semua (13 Orphans)": (15, 25, "13 ORPHANS", 
                ['Pin1','Pin9','Sou1','Sou9','Man1','Man9','Ton','Nan','Sha','Pei','Chun','Hatsu','Haku','+','Chun']),
            "👼 Keping langsung menang dari pembagian awal": (15, 25, "TIANHU / DI HU", 
                ['Teks:✨ MENANG INSTAN DARI BANDAR ✨'])
        }

    def hitung_skor(self, ciri_keping, jumlah_joker, bonus_lain, is_batal):
        if is_batal: return -30, "🚨 PENALTI FALSE HU!"
        data_hand = self.katalog_visual[ciri_keping]
        poin_joker, poin_murni, nama_resmi = data_hand[0], data_hand[1], data_hand[2]
        pakai_joker = jumlah_joker > 0
        skor = poin_joker if (poin_joker != poin_murni and pakai_joker) else poin_murni
        if poin_joker == poin_murni and not pakai_joker: skor += 2 
        return skor + jumlah_joker + bonus_lain, nama_resmi

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kasir Mahjong (Offline Image)", layout="centered", page_icon="🀄")

# --- SIDEBAR: KAMUS LOKAL ---
with st.sidebar:
    st.header("📖 Kamus Contekan")
    if os.path.exists("Tiles_2.jpg"): st.image("Tiles_2.jpg", use_column_width=True)
    else: st.warning("Simpan gambar Tiles_2.jpg di folder yang sama untuk melihat kamus ini.")
    
    st.divider()
    
    if os.path.exists("honors_2.jpg"): st.image("honors_2.jpg", use_column_width=True)
    else: st.warning("Simpan gambar honors_2.jpg di folder yang sama untuk melihat kamus ini.")

# --- SISTEM LOGIN & KALKULATOR UTAMA ---
st.title("🀄 Kasir Mahjong J2")

room_input = st.text_input("🔑 Masukkan Kode Meja (Contoh: VIP1):", "").upper()

if room_input:
    if room_input not in db_room:
        db_room[room_input] = {"Timur": 1000, "Selatan": 1000, "Barat": 1000, "Utara": 1000}
    
    st.success(f"Masuk ke Room: **{room_input}**")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Timur", db_room[room_input]["Timur"])
    c2.metric("Selatan", db_room[room_input]["Selatan"])
    c3.metric("Barat", db_room[room_input]["Barat"])
    c4.metric("Utara", db_room[room_input]["Utara"])
    
    if st.button("🔄 Segarkan Saldo"): st.rerun()

    st.divider()

    app = KalkulatorPemulaJ2()
    st.markdown("### 🧮 Hitung Kemenangan")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1: pemenang = st.selectbox("👑 Pemenang:", ["Timur", "Selatan", "Barat", "Utara"])
    with col_p2: cara_menang = st.radio("⚔️ Cara Menang:", ["RON (Buangan lawan)", "ZIMO (Ambil sendiri)"])

    if cara_menang == "RON (Buangan lawan)":
        opsi_kalah = ["Timur", "Selatan", "Barat", "Utara"]
        opsi_kalah.remove(pemenang)
        pembuang = st.selectbox("🎯 Siapa pembuang keping terakhir? (Denda 2x)", opsi_kalah)

    st.write("")
    ciri_pilihan = st.selectbox("Formasi Pemenang:", list(app.katalog_visual.keys()))
    
    # RENDER GAMBAR BERWARNA DARI ASET LOKAL
    st.markdown("💡 **Preview Bentuk Keping:**")
    st.markdown(render_formasi(app.katalog_visual[ciri_pilihan][3]), unsafe_allow_html=True)
    
    st.write("")
    col_j, col_b = st.columns(2)
    with col_j: jumlah_joker = st.number_input("Jumlah Joker dipakai:", 0, 4, 0)
    with col_b:
        bonus_total = 0
        if st.checkbox("Set Naga (+1)"): bonus_total += 1
        if st.checkbox("Set Angin Kursi (+1)"): bonus_total += 1
        if st.checkbox("Mata angka 2/8 (+1)"): bonus_total += 1
        if st.checkbox("Bunga Kursi (+1/+2)"): bonus_total += 1
        if st.checkbox("FULL 4 Bunga (+5)"): bonus_total += 5

    is_batal = st.checkbox("🚨 Kena Penalti False Hu (Salah Panggil)")
    st.divider()

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1: cek_btn = st.button("🔍 CEK POIN", use_container_width=True)
    with col_btn2: hitung_btn = st.button("🧮 SAH! POTONG SALDO", type="primary", use_container_width=True)

    if cek_btn:
        skor, nama = app.hitung_skor(ciri_pilihan, jumlah_joker, bonus_total, is_batal)
        if skor < 3: st.error(f"🛑 Jangan teriak menang! Poin baru {skor}.")
        else: st.success(f"✅ Aman! Poin Anda {skor}.")

    if hitung_btn:
        skor, nama = app.hitung_skor(ciri_pilihan, jumlah_joker, bonus_total, is_batal)
        if is_batal or skor < 3:
            st.error(f"❌ TIDAK SAH! Poin cuma {skor}. Penalti -30 poin dijatuhkan ke {pemenang}.")
            for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                if kursi == pemenang: db_room[room_input][kursi] -= 30
                else: db_room[room_input][kursi] += 10
            st.rerun()
        else:
            if cara_menang == "RON (Buangan lawan)":
                for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                    if kursi == pemenang: db_room[room_input][kursi] += (skor * 4)
                    elif kursi == pembuang: db_room[room_input][kursi] -= (skor * 2) 
                    else: db_room[room_input][kursi] -= skor 
            else: 
                for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                    if kursi == pemenang: db_room[room_input][kursi] += (skor * 6)
                    else: db_room[room_input][kursi] -= (skor * 2) 
            st.rerun()