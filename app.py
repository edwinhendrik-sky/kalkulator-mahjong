import streamlit as st
import os

# --- DATABASE SEMENTARA (ROOM, SALDO, STATISTIK, & HISTORY) ---
@st.cache_resource
def get_room_database():
    return {}

@st.cache_resource
def get_history_database():
    return {}

db_room = get_room_database()
db_history = get_history_database()

# --- INISIALISASI SESSION PEMAIN ---
if "room" not in st.session_state: st.session_state.room = None
if "kursi" not in st.session_state: st.session_state.kursi = None
if "nama" not in st.session_state: st.session_state.nama = None

# --- FUNGSI PREVIEW VISUAL ---
def preview_keping(teks):
    return f"<div style='font-size: clamp(18px, 4vw, 26px); text-align: center; background-color: #f8f9fa; padding: 8px; border-radius: 6px; letter-spacing: 2px; color: #1f1f1f; border: 1px solid #ddd; word-break: break-all;'>{teks}</div>"

class KalkulatorPemulaJ2:
    def __init__(self):
        self.katalog_visual = {
            "🔀 Campur aduk (Seri/Kembar)": (0, 0, "CHICKEN HAND", "🀙🀚🀛 🀔🀔🀔 🀝🀞🀟 🀇🀈🀉 + 🀀🀀"),
            "🔢 Susunan Serian (Chow)": (2, 2, "ALL SEQUENCES", "🀙🀚🀛 🀔🀕🀖 🀝🀞🀟 🀇🀈🀉 + 🀀🀀"),
            "🀄 Semuanya 3-Kembar (Pong)": (3, 3, "ALL TRIPLETS", "🀙🀙🀙 🀔🀔🀔 🀄🀄🀄 🀇🀇🀇 + 🀀🀀"),
            "🧱 Semuanya 4-Kembar (Kong)": (15, 25, "ALL QUADRUPLETS", "🀙🀙🀙🀙 🀔🀔🀔🀔 🀄🀄🀄🀄 🀇🀇🀇🀇 + 🀀🀀"),
            "🎨 Murni Satu Warna": (10, 20, "FULL COLOUR", "🀙🀚🀛 🀙🀙🀙 🀝🀞🀟 🀡🀡🀡 + 🀠🀠"),
            "🖌️ Warna Dasar + Tulisan Naga/Angin": (4, 4, "MIXED FLUSH", "🀙🀚🀛 🀙🀙🀙 🀝🀞🀟 🀄🀄🀄 + 🀀🀀"),
            "👑 Murni Naga & Angin Saja": (10, 20, "ALL HONOURS", "🀀🀀🀀 🀁🀁🀁 🀄🀄🀄 🀆🀆🀆 + 🀅🀅"),
            "🐉 3 Set Naga Komplit": (10, 20, "BIG 3 DRAGONS", "🀄🀄🀄 🀅🀅🀅 🀆🀆🀆 🀙🀚🀛 + 🀀🀀"),
            "🌬️ 4 Set Angin Lengkap": (12, 22, "BIG 4 WINDS", "🀀🀀🀀 🀁🀁🀁 🀂🀂🀂 🀃🀃🀃 + 🀄🀄"),
            "👯 7 Pasang Keping (7 Pair)": (10, 20, "SEVEN PAIRS", "🀙🀙 🀔🀔 🀝🀝 🀇🀇 🀀🀀 🀄🀄 🀁🀁"),
            "🛑 Angka 1, 9 & Huruf Saja": (3, 3, "MIXED TERMINALS", "🀙🀙🀙 🀡🀡🀡 🀀🀀🀀 🀄🀄🀄 + 🀁🀁"),
            "⛔ Murni Angka 1 & 9 Saja": (10, 20, "ALL TERMINALS", "🀙🀙🀙 🀡🀡🀡 🀐🀐🀐 🀘🀘🀘 + 🀇🀇"),
            "⛩️ Nine Gates Satu Warna": (12, 22, "NINE GATES", "🀙🀙🀙 🀚🀛🀜 🀝🀞🀟 🀠 🀡🀡🀡 + 🀚"),
            "🌟 13 Orphans (Keping Ujung)": (15, 25, "13 ORPHANS", "🀙 🀡 🀐 🀘 🀇 🀏 🀀 🀁 🀂 🀃 🀄 🀅 🀆 + 🀄"),
            "👼 Menang Instan (Tianhu)": (15, 25, "TIANHU", "✨ (Menang Instan dari Bandar) ✨")
        }

    def hitung_skor(self, ciri_keping, jumlah_joker, bonus_lain, is_batal):
        if is_batal: return -30, "🚨 PENALTI FALSE HU!"
        data_hand = self.katalog_visual[ciri_keping]
        poin_joker, poin_murni, nama_resmi = data_hand[0], data_hand[1], data_hand[2]
        pakai_joker = jumlah_joker > 0
        skor = poin_joker if (poin_joker != poin_murni and pakai_joker) else poin_murni
        if poin_joker == poin_murni and not pakai_joker: skor += 2 
        return skor + jumlah_joker + bonus_lain, nama_resmi

# --- KONFIGURASI HALAMAN RESPONSIF ---
st.set_page_config(page_title="Aplikasi Mahjong Taiwan", layout="wide", page_icon="🀄")

# --- CUSTOM CSS UNTUK TAMPILAN RESPONSIF HP & KOMPUTER ---
st.markdown(
    """
    <style>
        /* Mengatur padding halaman agar optimal di HP */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        /* Styling kartu podium agar fleksibel */
        .podium-card {
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #ddd;
            background: white;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR: KAMUS ---
with st.sidebar:
    st.header("📖 Kamus Contekan")
    if os.path.exists("tiles.jpg"): st.image("tiles.jpg", caption="Keping Angka", use_container_width=True)
    if os.path.exists("honors.jpg"): st.image("honors.jpg", caption="Keping Tulisan", use_container_width=True)

# --- FASE 1: LOBI ---
if not st.session_state.room:
    st.title("🀄 Lobi Utama Mahjong")
    
    col_lobi_kiri, col_lobi_kanan = st.columns(2, gap="medium")

    with col_lobi_kiri:
        st.subheader("📋 Room Tersedia")
        if len(db_room) == 0:
            st.info("Belum ada room aktif. Silakan buat room baru di sebelah kanan.")
        else:
            for r_name, r_data in db_room.items():
                jumlah_isi = sum(1 for k in r_data.values() if k["nama"] is not None)
                with st.container(border=True):
                    col_li1, col_li2 = st.columns([3, 1])
                    with col_li1:
                        st.markdown(f"**🏠 {r_name}** | 👥 {jumlah_isi}/4 Kursi")
                        kursi_terisi_str = ", ".join([f"{k}: {v['nama']}" for k, v in r_data.items() if v["nama"] is not None])
                        st.caption(f"{kursi_terisi_str if kursi_terisi_str else 'Kosong'}")
                    with col_li2:
                        if st.button("Masuk", key=f"btn_room_{r_name}", use_container_width=True):
                            st.session_state.selected_room_quick = r_name
                            st.rerun()

    with col_lobi_kanan:
        st.subheader("🚀 Masuk / Buat Room")
        default_room_val = st.session_state.get("selected_room_quick", "")

        with st.form("form_login_simple"):
            input_room = st.text_input("🏠 Nama Room Bermain:", value=default_room_val).upper().strip()
            input_nama = st.text_input("👤 Nama Panggilan Anda:")
            
            kursi_pilihan_default = ["Timur", "Selatan", "Barat", "Utara"]
            if input_room in db_room:
                kursi_pilihan_default = [k for k, v in db_room[input_room].items() if v["nama"] is None]
                if not kursi_pilihan_default:
                    kursi_pilihan_default = ["Timur", "Selatan", "Barat", "Utara"]

            input_kursi = st.selectbox("🪑 Pilih Kursi:", kursi_pilihan_default)
            paksa_masuk = st.checkbox("⚠️ Paksa ambil alih kursi")
            
            submit_btn = st.form_submit_button("Masuk ke Meja", type="primary", use_container_width=True)

            if submit_btn:
                if not input_room or not input_nama:
                    st.error("Nama Room & Nama wajib diisi!")
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
                        st.error(f"❌ Kursi {input_kursi} sudah diklaim {kursi_saat_ini}!")
                    else:
                        db_room[input_room][input_kursi]["nama"] = input_nama
                        st.session_state.room = input_room
                        st.session_state.nama = input_nama
                        st.session_state.kursi = input_kursi
                        if "selected_room_quick" in st.session_state:
                            del st.session_state.selected_room_quick
                        st.rerun()

# --- FASE 2: HALAMAN MEJA ---
else:
    room = st.session_state.room
    data_room = db_room[room]
    if room not in db_history:
        db_history[room] = []
    
    col_hdr1, col_hdr2 = st.columns([2, 1])
    with col_hdr1:
        st.markdown(f"### 🀄 Room: {room}")
        pemain_terisi = sum(1 for v in data_room.values() if v["nama"] is not None)
        st.caption(f"👥 Status Meja: {pemain_terisi}/4 Kursi Terisi")
        
    with col_hdr2:
        col_btn_a, col_btn_b = st.columns(2)
        with col_btn_a:
            @st.dialog("🥾 Kosongkan Kursi Player")
            def dialog_kosongkan_kursi():
                st.write("Pilih kursi pemain yang ingin dikosongkan:")
                kursi_terisi_list = [k for k, v in data_room.items() if v["nama"] is not None]
                if not kursi_terisi_list:
                    st.info("Semua kursi kosong.")
                else:
                    pilihan_kursi_kick = st.selectbox("Kursi:", kursi_terisi_list, format_func=lambda k: f"{k} ({data_room[k]['nama']})")
                    if st.button("Konfirmasi Kosongkan", type="primary"):
                        data_room[pilihan_kursi_kick]["nama"] = None
                        if st.session_state.kursi == pilihan_kursi_kick:
                            st.session_state.room = None
                            st.session_state.nama = None
                            st.session_state.kursi = None
                        st.rerun()

            if st.button("🥾 Kosong", use_container_width=True):
                dialog_kosongkan_kursi()
        with col_btn_b:
            if st.button("🚪 Keluar", use_container_width=True):
                db_room[room][st.session_state.kursi]["nama"] = None
                st.session_state.room = None
                st.session_state.nama = None
                st.session_state.kursi = None
                st.rerun()

    st.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

    # --- TANGGA PODIUM BERTINGKAT RESPONSIF ---
    data_klasemen = []
    for k in ["Timur", "Selatan", "Barat", "Utara"]:
        p_data = data_room[k]
        data_klasemen.append({
            "kursi": k, 
            "nama": p_data["nama"] if p_data["nama"] else "(Kosong)", 
            "saldo": p_data["saldo"], 
            "menang": p_data.get("menang", 0)
        })
    
    data_klasemen = sorted(data_klasemen, key=lambda x: x["saldo"], reverse=True)
    p1, p2, p3, p4 = data_klasemen[0], data_klasemen[1], data_klasemen[2], data_klasemen[3]

    podium_cols = st.columns(4)
    urutan_tangga = [
        (p2, "🥈 Peringkat 2", "margin-top: 10px; border-top: 3px solid #95a5a6;"),
        (p1, "🥇 Peringkat 1", "margin-top: 0px; border-top: 4px solid #f1c40f; background-color: #fffdf0;"),
        (p3, "🥉 Peringkat 3", "margin-top: 15px; border-top: 3px solid #cd7f32;"),
        (p4, "💩 Peringkat 4", "margin-top: 20px; border-top: 3px solid #e74c3c;")
    ]

    for idx, (p_item, label_peringkat, style_tangga) in enumerate(urutan_tangga):
        with podium_cols[idx]:
            st.markdown(f"""
            <div style="{style_tangga}" class="podium-card">
                <div style="font-size: 10px; font-weight: bold; color: #666;">{label_peringkat}</div>
                <div style="font-size: 11px; font-weight: bold; color: #111; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{p_item['nama']}</div>
                <div style="font-size: 12px; font-weight: bold; color: #2e7d32;">💰 {p_item['saldo']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 6px 0;'>", unsafe_allow_html=True)

    # --- LAYOUT KALKULATOR FLEKSIBEL ---
    app = KalkulatorPemulaJ2()
    col_calc_kiri, col_calc_kanan = st.columns(2, gap="medium")

    with col_calc_kiri:
        st.markdown("##### 🧮 Input Kemenangan")
        def format_nama(k):
            nm = data_room[k]["nama"]
            return f"{nm} ({k})" if nm else f"Kosong ({k})"

        pemenang = st.selectbox("👑 Pemenang:", ["Timur", "Selatan", "Barat", "Utara"], format_func=format_nama)
        cara_menang = st.radio("⚔️ Cara Menang:", ["RON (Buangan lawan)", "ZIMO (Ambil sendiri)"], horizontal=True)

        pembuang = None
        if cara_menang == "RON (Buangan lawan)":
            opsi_kalah = ["Timur", "Selatan", "Barat", "Utara"]
            opsi_kalah.remove(pemenang)
            pembuang = st.selectbox("🎯 Pembuang keping (Denda 2x):", opsi_kalah, format_func=format_nama)

        ciri_pilihan = st.selectbox("Formasi Pemenang:", list(app.katalog_visual.keys()))

    with col_calc_kanan:
        st.markdown("##### ⚙️ Preview & Eksekusi")
        st.markdown(preview_keping(app.katalog_visual[ciri_pilihan][3]), unsafe_allow_html=True)
        
        col_j, col_b = st.columns(2)
        with col_j: 
            jumlah_joker = st.number_input("Joker:", 0, 4, 0)
        with col_b:
            is_batal = st.checkbox("🚨 False Hu (-30)")

        bonus_total = 0
        with st.expander("🎁 Atur Bonus Poin"):
            if st.checkbox("Set Naga (+1)"): bonus_total += 1
            if st.checkbox("Set Angin Kursi (+1)"): bonus_total += 1
            if st.checkbox("Mata angka 2/8 (+1)"): bonus_total += 1
            if st.checkbox("Bunga Kursi (+1/+2)"): bonus_total += 1
            if st.checkbox("FULL 4 Bunga (+5)"): bonus_total += 5

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1: 
            cek_btn = st.button("🔍 Cek Poin", use_container_width=True)
        with col_btn2: 
            hitung_btn = st.button("🧮 Potong Saldo", type="primary", use_container_width=True)

    # --- LOGIKA EKSEKUSI & HISTORY ---
    if cek_btn:
        skor, nama = app.hitung_skor(ciri_pilihan, jumlah_joker, bonus_total, is_batal)
        if skor < 3: st.error(f"🛑 Poin baru {skor} (< 3 poin).")
        else: st.success(f"✅ Poin sah: {skor}.")

    if hitung_btn:
        skor, nama = app.hitung_skor(ciri_pilihan, jumlah_joker, bonus_total, is_batal)
        
        pemenang_nama_asli = data_room[pemenang]["nama"] or pemenang
        if is_batal or skor < 3:
            teks_history = f"❌ **FALSE HU**: {pemenang_nama_asli} kena Penalti -30 poin."
            for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                if kursi == pemenang: data_room[kursi]["saldo"] -= 30
                else: data_room[kursi]["saldo"] += 10
        else:
            data_room[pemenang]["menang"] = data_room[pemenang].get("menang", 0) + 1
            if cara_menang == "RON (Buangan lawan)":
                pembuang_nama_asli = data_room[pembuang]["nama"] or pembuang
                teks_history = f"⚔️ **RON**: {pemenang_nama_asli} (+{skor*4}) dari {pembuang_nama_asli} (-{skor*2})."
                for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                    if kursi == pemenang: data_room[kursi]["saldo"] += (skor * 4)
                    elif kursi == pembuang: data_room[kursi]["saldo"] -= (skor * 2) 
                    else: data_room[kursi]["saldo"] -= skor 
            else: 
                teks_history = f"🎯 **ZIMO**: {pemenang_nama_asli} menang sendiri (+{skor*6})."
                for kursi in ["Timur", "Selatan", "Barat", "Utara"]:
                    if kursi == pemenang: data_room[kursi]["saldo"] += (skor * 6)
                    else: data_room[kursi]["saldo"] -= (skor * 2) 
        
        db_history[room].insert(0, teks_history)
        st.rerun()

    # --- HISTORY GAMEPLAY ---
    with st.expander("📜 Riwayat Permainan (History Gameplay)"):
        if room in db_history and db_history[room]:
            for h in db_history[room]:
                st.markdown(f"- {h}")
        else:
            st.info("Belum ada riwayat permainan di room ini.")