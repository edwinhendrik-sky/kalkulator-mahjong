class J2MahjongCalculator:
    def __init__(self):
        # Database nilai Hand Dasar berdasarkan rulebook
        # Format: "Nama Hand": (Poin dengan Joker, Poin tanpa Joker) atau (Poin tetap)
        self.base_hands = {
            "CHICKEN HAND": (0, 0),
            "ALL SEQUENCES": (2, 2),
            "ALL TRIPLETS": (3, 3),
            "MIXED TERMINALS": (3, 3),
            "MIXED / SEMI FLUSH": (4, 4),
            "SMALL THREE DRAGONS": (5, 5),
            "SEVEN PAIRS": (10, 20),
            "FULL COLOUR": (10, 20),
            "3 SCHOLARS": (10, 20),
            "SMALL FOUR WINDS": (10, 20),
            "ALL CONCEALED TRIPLETS": (10, 20),
            "ALL HONOURS": (10, 20),
            "ALL TERMINALS": (10, 20),
            "NINE GATES": (12, 22),
            "4 BLESSINGS": (12, 22),
            "13 ORPHANS": (15, 25),
            "ALL QUADRUPLETS": (15, 25),
            "TIANHU": (15, 25),
            "DI HU": (15, 25)
        }
        
        self.current_hand = None
        self.has_joker = False
        self.joker_count = 0
        self.bonus_points = 0
        self.is_false_hu = False

    def set_hand(self, hand_name, joker_count=0):
        """Menentukan kombinasi dasar dan jumlah joker."""
        self.current_hand = hand_name.upper()
        self.joker_count = joker_count
        self.has_joker = joker_count > 0

    def add_bonus(self, bonus_type, count=1):
        """Menambahkan poin tambahan/bonus ke dalam total."""
        # Daftar bonus dari rulebook
        bonuses = {
            "NAGA": 1,                 # +1 per triplet
            "ANGIN PUTARAN/KURSI": 1,  # +1 (atau +2 jika keduanya)
            "PAIR 2/8": 1,             # +1
            "BUNGA HITAM SESUAI": 1,   # +1
            "BUNGA MERAH TIDAK SESUAI": 1, # +1
            "BUNGA MERAH SESUAI": 2,   # +2
            "SET BUNGA MERAH": 7,      # +7
            "SET BUNGA HITAM": 5,      # +5
            "HAND TERTUTUP": 1,        # +1
            "TANPA BUNGA, NAGA, ANGIN": 1, # +1
            "LAST TILE / DISCARD": 2,  # +2
            "MENCURI KONG": 1,         # +1
            "MENANG DARI BUNTUT": 1    # +1
        }
        if bonus_type in bonuses:
            self.bonus_points += bonuses[bonus_type] * count

    def calculate_total_points(self):
        """Menghitung total poin (Hand dasar + Bonus + Poin Joker)."""
        if self.is_false_hu:
            return -30  # Penalti Hu Palsu
            
        if not self.current_hand or self.current_hand not in self.base_hands:
            return 0

        # Ambil poin dasar
        base_scores = self.base_hands[self.current_hand]
        
        # Tentukan poin dasar berdasarkan penggunaan joker
        if base_scores[0] != base_scores[1]:
            # Ini adalah hand bernilai ganda (contoh: 10/20)
            score = base_scores[0] if self.has_joker else base_scores[1]
            # Bonus "tanpa joker" sudah termasuk di nilai keduanya, tidak ditambah +2 lagi.
        else:
            # Ini adalah hand reguler (contoh: Chicken Hand, All Sequences, dsb)
            score = base_scores[0]
            # Tambah bonus tanpa joker (+2) jika tidak ada joker
            if not self.has_joker:
                score += 2

        # Tambahkan poin per joker (1 poin per joker)
        score += (self.joker_count * 1)
        
        # Tambahkan poin bonus lainnya
        score += self.bonus_points
        
        return score

    def calculate_payout(self, win_type="RON"):
        """Menghitung siapa yang membayar poin."""
        total = self.calculate_total_points()
        
        if self.is_false_hu:
            return {"Penalti": -30, "Lawan 1": 10, "Lawan 2": 10, "Lawan 3": 10}
            
        if total < 3:
            return "Gagal: Hand harus bernilai minimal 3 poin untuk menang."
            
        if win_type.upper() == "RON":
            # Pembuang membayar 2x, pemain lain 1x
            return {"Pembuang": total * 2, "Pemain Lain 1": total * 1, "Pemain Lain 2": total * 1}
        elif win_type.upper() == "ZIMO":
            # Semua pemain kalah membayar 2x poin
            return {"Semua Lawan (Masing-masing)": total * 2}
            
    def instant_points(self, kong_type):
        """Menghitung poin instan dari Kong yang langsung dibayar saat itu juga."""
        kongs = {
            "KONG TERTUTUP": 6,  # Tiap lawan bayar 2
            "KONG BUANGAN": 3,   # Tiap lawan bayar 1
            "KONG TAMBAHAN": 3   # Tiap lawan bayar 1
        }
        return kongs.get(kong_type.upper(), 0)

    def instant_win(self, condition):
        """Deklarasi menang instan tanpa hitung poin normal."""
        if condition.upper() in ["7 BUNGA + SEASON", "4 JOKER"]:
            return "INSTANT WIN: 10 Poin Dasar"

# --- CONTOH PENGGUNAAN APLIKASI ---
app = J2MahjongCalculator()

# Kasus 1: Pemain menang "SEVEN PAIRS" dengan 1 Joker lewat ambilan lawan (RON)
app.set_hand("SEVEN PAIRS", joker_count=1) 
app.add_bonus("PAIR 2/8", count=1)
total_skor = app.calculate_total_points()
pembayaran = app.calculate_payout(win_type="RON")

print(f"Skor Total: {total_skor}")
print(f"Pembayaran: {pembayaran}")