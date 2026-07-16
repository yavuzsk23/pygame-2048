import pygame
import random
import sys

# ============================================================
# AYARLAR
# ============================================================
GENISLIK = 400
OYUN_ALANI_YUKSEKLIK = 400
SKOR_BAR_YUKSEKLIK = 90
PENCERE_YUKSEKLIK = OYUN_ALANI_YUKSEKLIK + SKOR_BAR_YUKSEKLIK
IZGARA_BOYUTU = 4
HUCRE_BOYUTU = GENISLIK // IZGARA_BOYUTU
UST_BOSLUK = SKOR_BAR_YUKSEKLIK  # oyun tahtası bu kadar aşağıdan başlıyor (skor barı için yer)

ANIMASYON_SURESI_MS = 130  # kaydırma animasyonunun süresi
KAZANMA_DEGERI = 2048

# Renk Paleti (2048 Klasik Renkleri)
RENKLER = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

KONFETI_RENKLERI = [
    (255, 89, 94), (255, 202, 58), (138, 201, 38),
    (25, 130, 196), (106, 76, 147), (255, 158, 0),
]


class Oyun2048:
    def __init__(self):
        pygame.init()
        self.ekran = pygame.display.set_mode((GENISLIK, PENCERE_YUKSEKLIK))
        pygame.display.set_caption("Cyberia 2048")
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.ui_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.overlay_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.overlay_font_kucuk = pygame.font.SysFont("Arial", 18)

        self.en_yuksek_skor = 0  # program açık kaldığı sürece hafızada tutulur
        self.yeni_oyun()

    # --------------------------------------------------------
    # OYUN DURUMU YÖNETİMİ
    # --------------------------------------------------------
    def yeni_oyun(self):
        self.izgara = [[0] * IZGARA_BOYUTU for _ in range(IZGARA_BOYUTU)]
        self.skor = 0
        self.oyun_durumu = "oynaniyor"  # oynaniyor | animasyon | oyun_bitti | kazandi
        self.kazandi_gosterildi = False
        self.animasyonlar = []
        self.animasyon_baslangic = 0
        self._kazanildi_bu_hamlede = False
        self.confetti = []
        self.yeni_sayi_ekle()
        self.yeni_sayi_ekle()

    def yeni_sayi_ekle(self):
        bos_hucreler = [
            (r, c) for r in range(IZGARA_BOYUTU) for c in range(IZGARA_BOYUTU)
            if self.izgara[r][c] == 0
        ]
        if bos_hucreler:
            r, c = random.choice(bos_hucreler)
            self.izgara[r][c] = 2 if random.random() < 0.9 else 4

    def oyun_bitti_mi(self):
        """Tahta dolu VE hiçbir komşu hücre birleşemiyorsa oyun biter."""
        for r in range(IZGARA_BOYUTU):
            for c in range(IZGARA_BOYUTU):
                if self.izgara[r][c] == 0:
                    return False
        for r in range(IZGARA_BOYUTU):
            for c in range(IZGARA_BOYUTU):
                v = self.izgara[r][c]
                if c + 1 < IZGARA_BOYUTU and self.izgara[r][c + 1] == v:
                    return False
                if r + 1 < IZGARA_BOYUTU and self.izgara[r + 1][c] == v:
                    return False
        return True

    # --------------------------------------------------------
    # HAREKET MANTIĞI (kaydırma + birleştirme + animasyon verisi)
    # --------------------------------------------------------
    def satir_hareket_detay(self, satir):
        """
        Bir satır/sütunu kaydırıp birleştirir.
        Döndürür: (yeni_satir, hareketler)
        hareketler -> [(orijinal_index, deger, hedef_index, sonuc_deger, gorunur), ...]
        gorunur=False olan taşlar birleşmede "yutulan" taşlardır (animasyonda hedefe kayıp kaybolur).
        """
        items = [(i, v) for i, v in enumerate(satir) if v != 0]
        hareketler = []
        yeni_satir = [0] * IZGARA_BOYUTU
        write_idx = 0
        i = 0
        n = len(items)
        while i < n:
            orig_i, val_i = items[i]
            if i + 1 < n and items[i + 1][1] == val_i:
                orig_j, val_j = items[i + 1]
                sonuc = val_i * 2
                hareketler.append((orig_i, val_i, write_idx, sonuc, True))
                hareketler.append((orig_j, val_j, write_idx, sonuc, False))
                yeni_satir[write_idx] = sonuc
                write_idx += 1
                i += 2
            else:
                hareketler.append((orig_i, val_i, write_idx, val_i, True))
                yeni_satir[write_idx] = val_i
                write_idx += 1
                i += 1
        return yeni_satir, hareketler

    def hucre_merkezi(self, r, c):
        x = c * HUCRE_BOYUTU + HUCRE_BOYUTU // 2
        y = UST_BOSLUK + r * HUCRE_BOYUTU + HUCRE_BOYUTU // 2
        return x, y

    def hareket_et(self, yon):
        if self.oyun_durumu != "oynaniyor":
            return

        yeni_izgara = [satir[:] for satir in self.izgara]
        tum_hareketler = []
        puan_kazanc = 0
        kazanildi_bu_hamlede = False
        satirlar_mi = yon in ("SOL", "SAG")

        for sabit in range(IZGARA_BOYUTU):
            if satirlar_mi:
                temel = self.izgara[sabit][:]
            else:
                temel = [self.izgara[r][sabit] for r in range(IZGARA_BOYUTU)]

            line = temel[::-1] if yon in ("SAG", "ASAGI") else temel[:]
            yeni_line, hareketler = self.satir_hareket_detay(line)

            def idx_to_cell(line_idx, sabit=sabit, yon=yon):
                if yon == "SOL":
                    return (sabit, line_idx)
                elif yon == "SAG":
                    return (sabit, IZGARA_BOYUTU - 1 - line_idx)
                elif yon == "YUKARI":
                    return (line_idx, sabit)
                else:  # ASAGI
                    return (IZGARA_BOYUTU - 1 - line_idx, sabit)

            for orig_idx, deger, hedef_idx, sonuc_deger, gorunur in hareketler:
                bas_r, bas_c = idx_to_cell(orig_idx)
                bit_r, bit_c = idx_to_cell(hedef_idx)
                tum_hareketler.append({
                    "baslangic": self.hucre_merkezi(bas_r, bas_c),
                    "bitis": self.hucre_merkezi(bit_r, bit_c),
                    "deger": deger,
                })
                if gorunur and sonuc_deger != deger:
                    puan_kazanc += sonuc_deger
                    if sonuc_deger == KAZANMA_DEGERI:
                        kazanildi_bu_hamlede = True

            for line_idx, v in enumerate(yeni_line):
                r, c = idx_to_cell(line_idx)
                yeni_izgara[r][c] = v

        if yeni_izgara == self.izgara:
            return  # hiçbir şey değişmedi, hamle geçersiz

        self.izgara = yeni_izgara
        self.skor += puan_kazanc
        self.en_yuksek_skor = max(self.en_yuksek_skor, self.skor)
        self.animasyonlar = tum_hareketler
        self.animasyon_baslangic = pygame.time.get_ticks()
        self.oyun_durumu = "animasyon"
        self._kazanildi_bu_hamlede = kazanildi_bu_hamlede

    def animasyonu_guncelle(self):
        if self.oyun_durumu != "animasyon":
            return
        gecen = pygame.time.get_ticks() - self.animasyon_baslangic
        if gecen >= ANIMASYON_SURESI_MS:
            self.animasyonlar = []
            self.yeni_sayi_ekle()
            if self._kazanildi_bu_hamlede and not self.kazandi_gosterildi:
                self.oyun_durumu = "kazandi"
                self.kazandi_gosterildi = True
                self._confetti_olustur()
            elif self.oyun_bitti_mi():
                self.oyun_durumu = "oyun_bitti"
            else:
                self.oyun_durumu = "oynaniyor"

    # --------------------------------------------------------
    # KONFETİ
    # --------------------------------------------------------
    def _confetti_olustur(self):
        self.confetti = [
            {
                "x": random.randint(0, GENISLIK),
                "y": random.randint(-PENCERE_YUKSEKLIK, 0),
                "vx": random.uniform(-1.2, 1.2),
                "vy": random.uniform(2.5, 5.5),
                "renk": random.choice(KONFETI_RENKLERI),
                "boyut": random.randint(4, 9),
            }
            for _ in range(90)
        ]

    def _confetti_guncelle_ciz(self):
        for p in self.confetti:
            p["y"] += p["vy"]
            p["x"] += p["vx"]
            if p["y"] > PENCERE_YUKSEKLIK:
                p["y"] = random.randint(-40, -10)
                p["x"] = random.randint(0, GENISLIK)
            pygame.draw.rect(self.ekran, p["renk"], (p["x"], p["y"], p["boyut"], p["boyut"]))

    # --------------------------------------------------------
    # ÇİZİM
    # --------------------------------------------------------
    def _tas_ciz(self, merkez_x, merkez_y, deger):
        renk = RENKLER.get(deger, (60, 58, 50))
        rect = pygame.Rect(0, 0, HUCRE_BOYUTU - 10, HUCRE_BOYUTU - 10)
        rect.center = (merkez_x, merkez_y)
        pygame.draw.rect(self.ekran, renk, rect, border_radius=8)
        metin_renk = (119, 110, 101) if deger <= 4 else (249, 246, 242)
        metin = self.font.render(str(deger), True, metin_renk)
        metin_rect = metin.get_rect(center=(merkez_x, merkez_y))
        self.ekran.blit(metin, metin_rect)

    def _skor_barini_ciz(self):
        pygame.draw.rect(self.ekran, (250, 248, 239), (0, 0, GENISLIK, SKOR_BAR_YUKSEKLIK))
        skor_metni = self.ui_font.render(f"SKOR: {self.skor}", True, (60, 58, 50))
        rekor_metni = self.ui_font.render(f"EN YÜKSEK: {self.en_yuksek_skor}", True, (60, 58, 50))
        ipucu = self.overlay_font_kucuk.render("R: Yeniden Başla", True, (120, 110, 100))
        self.ekran.blit(skor_metni, (12, 10))
        self.ekran.blit(rekor_metni, (12, 38))
        self.ekran.blit(ipucu, (GENISLIK - ipucu.get_width() - 12, 30))

    def _oyun_alani_arka_plani_ciz(self):
        pygame.draw.rect(self.ekran, (187, 173, 160), (0, UST_BOSLUK, GENISLIK, OYUN_ALANI_YUKSEKLIK))
        for r in range(IZGARA_BOYUTU):
            for c in range(IZGARA_BOYUTU):
                x, y = self.hucre_merkezi(r, c)
                self._tas_ciz(x, y, 0)

    def _statik_taslari_ciz(self):
        for r in range(IZGARA_BOYUTU):
            for c in range(IZGARA_BOYUTU):
                deger = self.izgara[r][c]
                if deger != 0:
                    x, y = self.hucre_merkezi(r, c)
                    self._tas_ciz(x, y, deger)

    def _animasyonlu_taslari_ciz(self):
        gecen = pygame.time.get_ticks() - self.animasyon_baslangic
        t = max(0.0, min(gecen / ANIMASYON_SURESI_MS, 1.0))
        for h in self.animasyonlar:
            bx0, by0 = h["baslangic"]
            bx1, by1 = h["bitis"]
            x = bx0 + (bx1 - bx0) * t
            y = by0 + (by1 - by0) * t
            self._tas_ciz(x, y, h["deger"])

    def _overlay_ciz(self, baslik, alt_yazi, renk_arka=(0, 0, 0, 160)):
        overlay = pygame.Surface((GENISLIK, OYUN_ALANI_YUKSEKLIK), pygame.SRCALPHA)
        overlay.fill(renk_arka)
        self.ekran.blit(overlay, (0, UST_BOSLUK))

        baslik_metin = self.overlay_font.render(baslik, True, (255, 255, 255))
        alt_metin = self.overlay_font_kucuk.render(alt_yazi, True, (230, 230, 230))
        baslik_rect = baslik_metin.get_rect(center=(GENISLIK // 2, UST_BOSLUK + OYUN_ALANI_YUKSEKLIK // 2 - 15))
        alt_rect = alt_metin.get_rect(center=(GENISLIK // 2, UST_BOSLUK + OYUN_ALANI_YUKSEKLIK // 2 + 25))
        self.ekran.blit(baslik_metin, baslik_rect)
        self.ekran.blit(alt_metin, alt_rect)

    def ciz(self):
        self._skor_barini_ciz()
        self._oyun_alani_arka_plani_ciz()

        if self.oyun_durumu == "animasyon":
            self._animasyonlu_taslari_ciz()
        else:
            self._statik_taslari_ciz()

        if self.oyun_durumu == "kazandi":
            self._confetti_guncelle_ciz()
            self._overlay_ciz("🎉 Tebrikler! 2048'e ulaştın!", "SPACE: Devam Et   |   R: Yeniden Başla")
        elif self.oyun_durumu == "oyun_bitti":
            self._overlay_ciz("Oyun Bitti", f"Skor: {self.skor}   |   R: Yeniden Başla")

        pygame.display.flip()

    # --------------------------------------------------------
    # ANA DÖNGÜ
    # --------------------------------------------------------
    def calistir(self):
        saat = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.yeni_oyun()
                    elif self.oyun_durumu == "kazandi" and event.key == pygame.K_SPACE:
                        self.oyun_durumu = "oynaniyor"
                    elif self.oyun_durumu == "oynaniyor":
                        if event.key == pygame.K_LEFT:
                            self.hareket_et("SOL")
                        elif event.key == pygame.K_RIGHT:
                            self.hareket_et("SAG")
                        elif event.key == pygame.K_UP:
                            self.hareket_et("YUKARI")
                        elif event.key == pygame.K_DOWN:
                            self.hareket_et("ASAGI")

            self.animasyonu_guncelle()
            self.ciz()
            saat.tick(60)


if __name__ == "__main__":
    Oyun2048().calistir()

