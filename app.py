import streamlit as st
import os

# --- DATABASE SEMENTARA ---
@st.cache_resource
def get_room_database():
    return {}

db_room = get_room_database()

# --- FUNGSI PREVIEW VISUAL (TEKS CEPAT UNTUK KALKULATOR) ---
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
        if is_batal:
            return -30, "🚨 PENALTI FALSE HU!"
        data_hand = self.katalog_visual[ciri_keping]
        poin_joker, poin_murni, nama_resmi = data_hand[0], data_hand[1], data_hand[2]
        pakai_joker = jumlah_joker > 0
        skor = poin_joker if (poin_joker != poin_murni and pakai_joker) else poin_murni
        if poin_joker == poin_murni and not pakai_joker: skor += 2 
        return skor + jumlah_joker + bonus_lain, nama_resmi


# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kasir Mahjong (Fast)", layout="centered", page_icon="🀄")

# --- SIDEBAR: KAMUS MENGGUNAKAN GAMBAR LOKAL ---
with st.sidebar:
    st.header("📖 Kamus Contekan")
    st.write("Intip panduan keping di bawah ini:")
    
    # Cek apakah file gambar tersedia untuk menghindari error
    if os.path.exists("Tiles.jpg"):
        st.image("Tiles.jpg", caption="Keping Angka (Suit Tiles)", use_container_width=True)
    else:
        st.warning("⚠️ Gambar 'Tiles.jpg' tidak ditemukan di folder.")
        
    st.divider()
    
    if os.path.exists("honors.jpg"):
        st.image("honors.jpg", caption="Keping Tulisan (Honors)", use_container_width=True)
    else:
        st.warning("⚠️ Gambar 'honors.jpg' tidak ditemukan di folder.")


# --- SISTEM LOGIN ROOM & BUKU KAS ---
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
    
    if st.button("🔄 Segarkan Saldo"):
        st.rerun()

    st.divider()

    # --- KALKULATOR UTAMA ---
    app = KalkulatorPemulaJ2()

    st.markdown("### 🧮 Hitung Kemenangan")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        pemenang = st.selectbox("👑 Pemenang:", ["Timur", "Selatan", "Barat", "Utara"])
    with col_p2:
        cara_menang = st.radio("⚔️ Cara Menang:", ["RON (Buangan lawan)", "ZIMO (Ambil sendiri)"])

    if cara_menang == "RON (Buangan lawan)":
        opsi_kalah = ["Timur", "Selatan", "Barat", "Utara"]
        opsi_kalah.remove(pemenang)
        pembuang = st.selectbox("🎯 Siapa pembuang keping terakhir? (Denda 2x)", opsi_kalah)

    st.write("")
    ciri_pilihan = st.selectbox("Formasi Pemenang:", list(app.katalog_visual.keys()))
    st.markdown(preview_keping(app.katalog_visual[ciri_pilihan][3]), unsafe_allow_html=True)
    
    st.write("")
    col_j, col_b = st.columns(2)
    with col_j:
        jumlah_joker = st.number_input("Jumlah Joker dipakai:", 0, 4, 0)
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
    with col_btn1:
        cek_btn = st.button("🔍 CEK POIN", use_container_width=True)
    with col_btn2:
        hitung_btn = st.button("🧮 SAH! POTONG SALDO", type="primary", use_container_width=True)

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