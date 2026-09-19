import streamlit as st
import os

# --- DATABASE SEMENTARA (ROOM, SALDO, & STATISTIK MENANG) ---
@st.cache_resource
def get_room_database():
    return {}

db_room = get_room_database()

# --- INISIALISASI SESSION PEMAIN ---
if "room" not in st.session_state: st.session_state.room = None
if "kursi" not in st.session_state: st.session_state.kursi = None
if "nama" not in st.session_state: st.session_state.nama = None

# --- FUNGSI PREVIEW VISUAL (SUPER CEPAT BERBASIS TEKS) ---
def preview_keping(teks):
    return f"<div style='font-size: 38px; text-align: center; background-color: #f8f9fa; padding: 10px; border-radius: 10px; letter-spacing: 2px; color: #1f1f1f; border: 1px solid #ddd;'>{teks}</div>"

class KalkulatorPemulaJ2:
    def __init__(self):
        self.katalog_visual = {
            "🔀 Campur aduk (Ada seri, ada kembar, beda warna)": (0, 0, "CHICKEN HAND", "🀙🀚🀛 🀔🀔🀔 🀝🀞🀟 🀇🀈🀉 + 🀀🀀"),
            "🔢 Semuanya berupa susunan SERI BERURUTAN (Chow)": (2, 2, "ALL SEQUENCES", "🀙🀚🀛 🀔🀕🀖 🀝🀞🀟 🀇🀈🀉 + 🀀🀀"),
            "🀄 Semuanya berupa 3-KEMBAR (Pong)": (3, 3, "ALL TRIPLETS", "🀙🀙🀙 🀔🀔🀔 🀄🀄🀄 🀇🀇🀇 + 🀀🀀"),
            "🧱 Semuanya berupa 4-KEMBAR (Kong)": (15, 25, "ALL QUADRUPLETS", "🀙🀙🀙🀙 🀔🀔🀔🀔 🀄🀄🀄🀄 🀇🀇🀇🀇 + 🀀🀀"),
            "🎨 Warnanya MURNI SATU JENIS saja (Tanpa huruf)": (10, 20, "FULL COLOUR", "🀙🀚🀛 🀙🀙🀙 🀝🀞🀟 🀡🀡🀡 + 🀠🀠"),
            "🖌️ Satu warna dasar, TAPI dicampur tulisan Naga/Angin": (4, 4, "MIXED / SEMI FLUSH", "🀙🀚🀛 🀙🀙🀙 🀝🀞🀟 🀄🀄🀄 + 🀀🀀"),
            "👑 Murni hanya keping tulisan NAGA dan ANGIN saja": (10, 20, "ALL HONOURS", "🀀🀀🀀 🀁🀁🀁 🀄🀄🀄 🀆🀆🀆 + 🀅🀅"),
            "🐉 Ada 3 set kembar Naga komplit (Merah, Hijau, Putih)": (10, 20, "3 SCHOLARS (BIG 3 DRAGONS)", "🀄🀄🀄 🀅🀅🀅 🀆🀆🀆 🀙🀚🀛 + 🀀🀀"),
            "🐲 Ada 2 set kembar Naga + 1 pasang (Pair) Naga": (5, 5, "SMALL THREE DRAGONS", "🀄🀄🀄 🀅🀅🀅 🀙🀚🀛 🀔🀔🀔 + 🀆🀆"),
            "🌬️ Ada 4 set kembar Angin lengkap (T, S, B, U)": (12, 22, "4 BLESSINGS (BIG 4 WINDS)", "🀀🀀🀀 🀁🀁🀁 🀂🀂🀂 🀃🀃🀃 + 🀄🀄"),
            "🌪️ Ada 3 set kembar Angin + 1 pasang (Pair) Angin": (10, 20, "SMALL FOUR WINDS", "🀀🀀🀀 🀁🀁🀁 🀂🀂🀂 🀙🀚🀛 + 🀃🀃"),
            "👯 Terdiri dari 7 pasang keping yang berbeda (7 Pair)": (10, 20, "SEVEN PAIRS", "🀙🀙 🀔🀔 🀝🀝 🀇🀇 🀀🀀 🀄🀄 🀁🀁"),
            "🛑 Isinya HANYA angka 1, angka 9, dan tulisan huruf saja": (3, 3, "MIXED TERMINALS", "🀙🀙🀙 🀡🀡🀡 🀀🀀🀀 🀄🀄🀄 + 🀁🀁"),
            "⛔ Isinya MURNI hanya angka 1 dan angka 9 (tanpa huruf)": (10, 20, "ALL TERMINALS", "🀙🀙🀙 🀡🀡🀡 🀐🀐🀐 🀘🀘🀘 + 🀇🀇"),
            "⛩️ Formasi rahasia 111-2345678-999 satu warna": (12, 22, "NINE GATES", "🀙🀙🀙 🀚🀛🀜 🀝🀞🀟 🀠 🀡🀡🀡 + 🀚"),
            "🌟 Keping ujung beda-beda semua (13 Orphans)": (15, 25, "13 ORPHANS", "🀙 🀡 🀐 🀘 🀇 🀏 🀀 🀁 🀂 🀃 🀄 🀅 🀆 + 🀄"),
            "👼 Keping langsung menang dari pembagian awal": (15, 25, "TIANHU / DI HU", "✨ (Menang Instan dari Bandar) ✨")
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

# --- SIDEBAR: KAMUS MENGGUNAKAN TILES.JPG & HONORS.JPG ---
with st.sidebar:
    st.header("📖 Kamus Contekan")
    if os.path.exists("tiles.jpg"): 
        st.image("tiles.jpg", caption="Keping Angka", use_container_width=True)
    else: 
        st.warning("⚠️ File 'tiles.jpg' belum ada di folder.")
        
    if os.path.exists("honors.jpg"): 
        st.image("honors.jpg", caption="Keping Tulisan", use_container_width=True)
    else: 
        st.warning("⚠️ File 'honors.jpg' belum ada di folder.")

# --- FASE 1: HALAMAN LOBI (LOGIN & RESET) ---
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

        if reset_btn:
            if input_room:
                db_room[input_room] = {
                    "Timur": {"nama": None, "saldo": 1000, "menang": 0},
                    "Selatan": {"nama": None, "saldo": 1000, "menang": 0},
                    "Barat": {"nama": None, "saldo": 1000, "menang": 0},
                    "Utara": {"nama": None, "saldo": 1000, "menang": 0}
                }
                st.success(f"✅ Data meja '{input_room}' berhasil dikosongkan dan di-reset ke 1.000 cip!")
            else:
                st.error("Isi Kode Meja terlebih dahulu untuk mereset meja tersebut!")

        if submit_btn:
            if not input_room or not input_nama:
                st.error("Kode Meja dan Nama wajib diisi!")
            else:
                if input_room not in db_room:
                    db_room[input_room] = {
                        "Timur": {"nama": None, "saldo": 1000, "menang": 0},
                        "Selatan": {"nama": None, "saldo": 1000, "menang": 0},
                        "Barat": {"nama": None, "saldo": 1000, "menang": 0},
                        "Utara": {"nama": None, "saldo": 1000, "menang": 0}
                    }
                
                kursi_saat_ini = db_room[input_room][input_kursi]["nama"]
                if kursi_saat_ini is not None and kursi_saat_ini != input_nama and not paksa_masuk:
                    st.error(f"❌ Kursi {input_kursi} sudah diklaim oleh {kursi_saat_ini}! Centang 'Paksa ambil alih' di atas jika Anda ingin menimpanya.")
                else:
                    db_room[input_room][input_kursi]["nama"] = input_nama
                    st.session_state.room = input_room
                    st.session_state.nama = input_nama
                    st.session_state.kursi = input_kursi
                    st.rerun()

# --- FASE 2: HALAMAN MEJA (LAYOUT MEJA MAHJONG & KALKULATOR) ---
else:
    room = st.session_state.room
    data_room = db_room[room]
    
    col_hdr1, col_hdr2 = st.columns([3,1])
    col_hdr1.title(f"🀄 Meja: {room}")
    if col_hdr2.button("🚪 Keluar Meja"):
        db_room[room][st.session_state.kursi]["nama"] = None
        st.session_state.room = None
        st.session_state.nama = None
        st.session_state.kursi = None
        st.rerun()

    pemain_terisi = [k for k, v in data_room.items() if v["nama"] is not None]
    st.info(f"👥 **Status Meja: {len(pemain_terisi)}/4 Kursi Terisi**")
    
    with st.expander("🛠️ Pengaturan Kursi (Tendang Pemain AFK)"):
        st.markdown("Kosongkan kursi jika ada pemain yang *error* atau lupa *logout* (saldo tetap aman).")
        for k_seat in ["Timur", "Selatan", "Barat", "Utara"]:
            nama_seat = data_room[k_seat]["nama"]
            if nama_seat:
                col_t1, col_t2 = st.columns([3, 1])
                col_t1.markdown(f"**{k_seat}**: {nama_seat}")
                if col_t2.button(f"🥾 Kosongkan {k_seat}", key=f"kick_{k_seat}"):
                    db_room[room][k_seat]["nama"] = None
                    if st.session_state.kursi == k_seat:
                        st.session_state.room = None
                        st.session_state.nama = None
                        st.session_state.kursi = None
                    st.rerun()
            else:
                st.markdown(f"**{k_seat}**: *(Kosong)*")

    st.divider()

    # --- LAYOUT FISIK MEJA MAHJONG (POSISI 4 ARAH ANGIN) ---
    st.markdown("### 🀄 Layout Meja & Saldo Player")
    
    # Fungsi pembantu info player di meja
    def info_meja(arah):
        p = data_room[arah]
        nm = p["nama"] if p["nama"] else "(Kosong)"
        return nm, p["saldo"], p.get("menang", 0)

    # Posisi Atas (Utara)
    t_nama, t_saldo, t_menang = info_meja("Utara")
    col_u1, col_u2, col_u3 = st.columns([1, 2, 1])
    with col_u2:
        with st.container(border=True):
            st.markdown(f"<div style='text-align: center;'><b>⬆️ UTARA</b><br><b>{t_nama}</b><br><span style='color: #2e7d32; font-weight: bold;'>💰 {t_saldo} Cip</span><br><span style='font-size: 12px; color: #666;'>Menang: {t_menang}x</span></div>", unsafe_allow_html=True)

    # Posisi Tengah (Barat & Timur berdampingan)
    b_nama, b_saldo, b_menang = info_meja("Barat")
    tm_nama, tm_saldo, tm_menang = info_meja("Timur")
    
    col_m1, col_tengah, col_m3 = st.columns([2, 1, 2])
    with col_m1:
        with st.container(border=True):
            st.markdown(f"<div style='text-align: center;'><b>⬅️ BARAT</b><br><b>{b_nama}</b><br><span style='color: #2e7d32; font-weight: bold;'>💰 {b_saldo} Cip</span><br><span style='font-size: 12px; color: #666;'>Menang: {b_menang}x</span></div>", unsafe_allow_html=True)
    with col_tengah:
        st.markdown("<div style='text-align: center; padding-top: 15px; font-size: 24px;'>🀄</div>", unsafe_allow_html=True)
    with col_m3:
        with st.container(border=True):
            st.markdown(f"<div style='text-align: center;'><b>TIMUR ➡️</b><br><b>{tm_nama}</b><br><span style='color: #2e7d32; font-weight: bold;'>💰 {tm_saldo} Cip</span><br><span style='font-size: 12px; color: #666;'>Menang: {tm_menang}x</span></div>", unsafe_allow_html=True)

    # Posisi Bawah (Selatan)
    s_nama, s_saldo, s_menang = info_meja("Selatan")
    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        with st.container(border=True):
            st.markdown(f"<div style='text-align: center;'><b>⬇️ SELATAN</b><br><b>{s_nama}</b><br><span style='color: #2e7d32; font-weight: bold;'>💰 {s_saldo} Cip</span><br><span style='font-size: 12px; color: #666;'>Menang: {s_menang}x</span></div>", unsafe_allow_html=True)

    if st.button("🔄 Segarkan Status Meja"): st.rerun()
    st.divider()

    def format_nama(k):
        nm = data_room[k]["nama"]
        return f"{nm} ({k})" if nm else f"Kosong ({k})"

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
    st.markdown(preview_keping(app.katalog_visual[ciri_pilihan][3]), unsafe_allow_html=True)
    
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
            data_room[pemenang]["menang"] = data_room[pemenang].get("menang", 0) + 1
            
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