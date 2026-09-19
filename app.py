import streamlit as st
import os
import base64

# --- DATABASE SEMENTARA (ROOM & SALDO) ---
@st.cache_resource
def get_room_database():
    return {}

db_room = get_room_database()

# --- INISIALISASI SESSION PEMAIN ---
if "room" not in st.session_state: st.session_state.room = None
if "kursi" not in st.session_state: st.session_state.kursi = None
if "nama" not in st.session_state: st.session_state.nama = None

# --- FUNGSI BACA GAMBAR (LOKAL + CADANGAN INTERNET) ---
def get_local_tile(nama_file, width=35):
    filepath = f"assets/{nama_file}.svg"
    if os.path.exists(filepath):
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"<img src='data:image/svg+xml;base64,{encoded_string}' width='{width}' style='vertical-align: middle; border-radius: 4px; box-shadow: 1px 2px 4px rgba(0,0,0,0.3); margin-right: 3px;'>"
    else:
        url = f"https://raw.githubusercontent.com/FluffyStuff/mahjong-tiles/master/svg/{nama_file}.svg"
        return f"<img src='{url}' width='{width}' style='vertical-align: middle; border-radius: 4px; box-shadow: 1px 2px 4px rgba(0,0,0,0.3); margin-right: 3px;'>"

def render_formasi(simbol_list):
    html = "<div style='display: flex; align-items: center; flex-wrap: wrap; background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ddd;'>"
    for item in simbol_list:
        if item == ' ': html += "<div style='width: 10px;'></div>"
        elif item == '+': html += "<div style='margin: 0 10px; font-weight: bold; font-size: 24px; color: #555;'>+</div>"
        elif item.startswith("Teks:"): html += f"<span style='font-size: 16px; margin-left: 10px; font-weight:bold;'>{item.replace('Teks:', '')}</span>"
        else: html += get_local_tile(item)
    html += "</div>"
    return html

class KalkulatorPemulaJ2:
    def __init__(self):
        self.katalog_visual = {
            "🔀 Campur aduk (Ada seri, ada kembar, beda warna)": (0, 0, "CHICKEN HAND", ['Pin1','Pin2','Pin3',' ','Sou5','Sou5','Sou5',' ','Pin5','Pin6','Pin7',' ','Man1','Man2','Man3','+','Ton','Ton']),
            "🔢 Semuanya berupa susunan SERI BERURUTAN (Chow)": (2, 2, "ALL SEQUENCES", ['Pin1','Pin2','Pin3',' ','Sou4','Sou5','Sou6',' ','Pin5','Pin6','Pin7',' ','Man1','Man2','Man3','+','Ton','Ton']),
            "🀄 Semuanya berupa 3-KEMBAR (Pong)": (3, 3, "ALL TRIPLETS", ['Pin1','Pin1','Pin1',' ','Sou5','Sou5','Sou5',' ','Chun','Chun','Chun',' ','Man1','Man1','Man1','+','Ton','Ton']),
            "🧱 Semuanya berupa 4-KEMBAR (Kong)": (15, 25, "ALL QUADRUPLETS", ['Pin1','Pin1','Pin1','Pin1',' ','Sou5','Sou5','Sou5','Sou5',' ','Chun','Chun','Chun','Chun',' ','Man1','Man1','Man1','Man1','+','Ton','Ton']),
            "🎨 Warnanya MURNI SATU JENIS saja (Tanpa huruf)": (10, 20, "FULL COLOUR", ['Pin1','Pin2','Pin3',' ','Pin1','Pin1','Pin1',' ','Pin5','Pin6','Pin7',' ','Pin9','Pin9','Pin9','+','Pin8','Pin8']),
            "🖌️ Satu warna dasar, TAPI dicampur tulisan Naga/Angin": (4, 4, "MIXED / SEMI FLUSH", ['Pin1','Pin2','Pin3',' ','Pin1','Pin1','Pin1',' ','Pin5','Pin6','Pin7',' ','Chun','Chun','Chun','+','Ton','Ton']),
            "👑 Murni hanya keping tulisan NAGA dan ANGIN saja": (10, 20, "ALL HONOURS", ['Ton','Ton','Ton',' ','Nan','Nan','Nan',' ','Chun','Chun','Chun',' ','Haku','Haku','Haku','+','Hatsu','Hatsu']),
            "🐉 Ada 3 set kembar Naga komplit (Merah, Hijau, Putih)": (10, 20, "3 SCHOLARS (BIG 3 DRAGONS)", ['Chun','Chun','Chun',' ','Hatsu','Hatsu','Hatsu',' ','Haku','Haku','Haku',' ','Pin1','Pin2','Pin3','+','Ton','Ton']),
            "🐲 Ada 2 set kembar Naga + 1 pasang (Pair) Naga": (5, 5, "SMALL THREE DRAGONS", ['Chun','Chun','Chun',' ','Hatsu','Hatsu','Hatsu',' ','Pin1','Pin2','Pin3',' ','Sou5','Sou5','Sou5','+','Haku','Haku']),
            "🌬️ Ada 4 set kembar Angin lengkap (T, S, B, U)": (12, 22, "4 BLESSINGS (BIG 4 WINDS)", ['Ton','Ton','Ton',' ','Nan','Nan','Nan',' ','Sha','Sha','Sha',' ','Pei','Pei','Pei','+','Chun','Chun']),
            "🌪️ Ada 3 set kembar Angin + 1 pasang (Pair) Angin": (10, 20, "SMALL FOUR WINDS", ['Ton','Ton','Ton',' ','Nan','Nan','Nan',' ','Sha','Sha','Sha',' ','Pin1','Pin2','Pin3','+','Pei','Pei']),
            "👯 Terdiri dari 7 pasang keping yang berbeda (7 Pair)": (10, 20, "SEVEN PAIRS", ['Pin1','Pin1',' ','Sou5','Sou5',' ','Pin5','Pin5',' ','Man1','Man1',' ','Ton','Ton',' ','Chun','Chun',' ','Nan','Nan']),
            "🛑 HANYA angka 1, angka 9, dan tulisan huruf saja": (3, 3, "MIXED TERMINALS", ['Pin1','Pin1','Pin1',' ','Pin9','Pin9','Pin9',' ','Ton','Ton','Ton',' ','Chun','Chun','Chun','+','Nan','Nan']),
            "⛔ MURNI hanya angka 1 dan angka 9 (tanpa huruf)": (10, 20, "ALL TERMINALS", ['Pin1','Pin1','Pin1',' ','Pin9','Pin9','Pin9',' ','Sou1','Sou1','Sou1',' ','Sou9','Sou9','Sou9','+','Man1','Man1']),
            "⛩️ Formasi rahasia 111-2345678-999 satu warna": (12, 22, "NINE GATES", ['Pin1','Pin1','Pin1',' ','Pin2','Pin3','Pin4','Pin5','Pin6','Pin7','Pin8',' ','Pin9','Pin9','Pin9','+','Pin2']),
            "🌟 Keping ujung beda-beda semua (13 Orphans)": (15, 25, "13 ORPHANS", ['Pin1','Pin9','Sou1','Sou9','Man1','Man9','Ton','Nan','Sha','Pei','Chun','Hatsu','Haku','+','Chun']),
            "👼 Keping langsung menang dari pembagian awal": (15, 25, "TIANHU / DI HU", ['Teks:✨ MENANG INSTAN DARI BANDAR ✨'])
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
st.set_page_config(page_title="Kasir Mahjong J2", layout="centered", page_icon="🀄")

# --- SIDEBAR: KAMUS LOKAL ---
with st.sidebar:
    st.header("📖 Kamus Contekan")
    if os.path.exists("Tiles_2.jpg"): st.image("Tiles_2.jpg", use_container_width=True)
    if os.path.exists("honors_2.jpg"): st.image("honors_2.jpg", use_container_width=True)

# --- FASE 1: HALAMAN LOBI (LOGIN DENGAN RESET & TAKEOVER) ---
if not st.session_state.room:
    st.title("🀄 Lobi Mahjong J2")
    st.markdown("Daftar untuk menempati kursi, atau reset data meja jika ada pemain yang keluar tanpa *logout*.")
    
    with st.form("form_login"):
        input_room = st.text_input("🔑 Kode Meja (Contoh: VIP1):").upper()
        input_nama = st.text_input("👤 Nama Panggilan Anda:")
        input_kursi = st.selectbox("🪑 Pilih Kursi:", ["Timur", "Selatan", "Barat", "Utara"])
        paksa_masuk = st.checkbox("⚠️ Paksa ambil alih kursi (Jika data sebelumnya nyangkut)")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit_btn = st.form_submit_button("Masuk ke Meja", type="primary")
        with col_btn2:
            reset_btn = st.form_submit_button("🧹 Reset Total Meja")

        # LOGIKA TOMBOL RESET (Hati-hati, ini mereset saldo ke 1000)
        if reset_btn:
            if input_room:
                db_room[input_room] = {
                    "Timur": {"nama": None, "saldo": 1000},
                    "Selatan": {"nama": None, "saldo": 1000},
                    "Barat": {"nama": None, "saldo": 1000},
                    "Utara": {"nama": None, "saldo": 1000}
                }
                st.success(f"✅ Data meja '{input_room}' berhasil dikosongkan dan di-reset ke 1.000 cip!")
            else:
                st.error("Isi Kode Meja terlebih dahulu untuk mereset meja tersebut!")

        # LOGIKA TOMBOL MASUK
        if submit_btn:
            if not input_room or not input_nama:
                st.error("Kode Meja dan Nama wajib diisi!")
            else:
                if input_room not in db_room:
                    db_room[input_room] = {
                        "Timur": {"nama": None, "saldo": 1000},
                        "Selatan": {"nama": None, "saldo": 1000},
                        "Barat": {"nama": None, "saldo": 1000},
                        "Utara": {"nama": None, "saldo": 1000}
                    }
                
                kursi_saat_ini = db_room[input_room][input_kursi]["nama"]
                
                if kursi_saat_ini is not None and kursi_saat_ini != input_nama and not paksa_masuk:
                    st.error(f"❌ Kursi {input_kursi} sudah diklaim oleh {kursi_saat_ini}! Centang 'Paksa ambil alih kursi' di atas jika Anda ingin menimpanya.")
                else:
                    db_room[input_room][input_kursi]["nama"] = input_nama
                    st.session_state.room = input_room
                    st.session_state.nama = input_nama
                    st.session_state.kursi = input_kursi
                    st.rerun()

# --- FASE 2: HALAMAN MEJA (KALKULATOR) ---
else:
    room = st.session_state.room
    data_room = db_room[room]
    
    col_hdr1, col_hdr2 = st.columns([3,1])
    col_hdr1.title("🀄 Kasir Mahjong J2")
    if col_hdr2.button("🚪 Keluar Meja"):
        db_room[room][st.session_state.kursi]["nama"] = None
        st.session_state.room = None
        st.session_state.nama = None
        st.session_state.kursi = None
        st.rerun()

    pemain_terisi = [k for k, v in data_room.items() if v["nama"] is not None]
    st.info(f"👥 **Room: {room} | Terisi: {len(pemain_terisi)}/4 Kursi**")
    
    # --- FITUR BARU: MANAJEMEN KURSI (TENDANG PEMAIN AFK) ---
    with st.expander("🛠️ Pengaturan Kursi (Tendang Pemain AFK)"):
        st.markdown("Jika ada teman yang aplikasinya *error* atau lupa *logout*, kosongkan kursinya di sini **tanpa menghapus saldo cipnya**.")
        
        for k_seat in ["Timur", "Selatan", "Barat", "Utara"]:
            nama_seat = data_room[k_seat]["nama"]
            if nama_seat:
                col_t1, col_t2 = st.columns([3, 1])
                col_t1.markdown(f"**{k_seat}**: {nama_seat}")
                if col_t2.button(f"🥾 Kosongkan {k_seat}", key=f"kick_{k_seat}"):
                    # Hapus nama saja, saldo tetap aman
                    db_room[room][k_seat]["nama"] = None
                    
                    # Jika yang ditendang adalah dirinya sendiri, keluarkan dari sesi
                    if st.session_state.kursi == k_seat:
                        st.session_state.room = None
                        st.session_state.nama = None
                        st.session_state.kursi = None
                    st.rerun()
            else:
                st.markdown(f"**{k_seat}**: *(Kosong)*")

    st.divider()

    # --- PAPAN SALDO ---
    st.markdown("### 🏦 Saldo Cip Meja")
    c1, c2, c3, c4 = st.columns(4)
    
    def format_nama(k):
        nm = data_room[k]["nama"]
        return f"{nm} ({k})" if nm else f"Kosong ({k})"

    c1.metric(format_nama("Timur"), data_room["Timur"]["saldo"])
    c2.metric(format_nama("Selatan"), data_room["Selatan"]["saldo"])
    c3.metric(format_nama("Barat"), data_room["Barat"]["saldo"])
    c4.metric(format_nama("Utara"), data_room["Utara"]["saldo"])
    
    if st.button("🔄 Segarkan Saldo Papan"): st.rerun()
    st.divider()

    app = KalkulatorPemulaJ2()
    st.markdown("### 🧮 Hitung Kemenangan")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1: pemenang = st.selectbox("👑 Pemenang:", ["Timur", "Selatan", "Barat", "Utara"], format_func=format_nama)
    with col_p2: cara_menang = st.radio("⚔️ Cara Menang:", ["RON (Buangan lawan)", "ZIMO (Ambil sendiri)"])

    if cara_menang == "RON (Buangan lawan)":
        opsi_kalah = ["Timur", "Selatan", "Barat", "Utara"]
        opsi_kalah.remove(pemenang)
        pembuang = st.selectbox("🎯 Siapa pembuang keping terakhir? (Denda 2x)", opsi_kalah, format_func=format_nama)

    st.write("")
    ciri_pilihan = st.selectbox("Formasi Pemenang:", list(app.katalog_visual.keys()))
    
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
            st.error(f"❌ TIDAK SAH! Poin cuma {skor}. Penalti -30 poin dijatuhkan ke {format_nama(pemenang)}.")
            for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                if kursi == pemenang: data_room[kursi]["saldo"] -= 30
                else: data_room[kursi]["saldo"] += 10
            st.rerun()
        else:
            if cara_menang == "RON (Buangan lawan)":
                for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                    if kursi == pemenang: data_room[kursi]["saldo"] += (skor * 4)
                    elif kursi == pembuang: data_room[kursi]["saldo"] -= (skor * 2) 
                    else: data_room[kursi]["saldo"] -= skor 
            else: 
                for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                    if kursi == pemenang: data_room[kursi]["saldo"] += (skor * 6)
                    else: data_room[kursi]["saldo"] -= (skor * 2) 
            st.rerun()