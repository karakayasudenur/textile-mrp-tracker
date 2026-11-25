import os
import tempfile
import unittest

import stok_takip as s


class KartBirTesti(unittest.TestCase):
    def setUp(self):
        fd, self.dosya = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.dosya)

    def tearDown(self):
        if os.path.exists(self.dosya):
            os.remove(self.dosya)

    def test_gecerli_kayit_json_a_yazilir(self):
        s.hammadde_ekle("KMS01", "Pamuklu Kumaş", "m", 100, 20, self.dosya)
        stok = s.stok_yukle(self.dosya)
        self.assertEqual(len(stok), 1)
        self.assertEqual(stok[0]["kod"], "KMS01")
        self.assertEqual(stok[0]["miktar"], 100.0)

    def test_negatif_miktar_reddedilir(self):
        with self.assertRaises(ValueError):
            s.hammadde_ekle("KMS01", "Kumaş", "m", -5, 20, self.dosya)
        self.assertEqual(s.stok_yukle(self.dosya), [])

    def test_bos_kod_reddedilir(self):
        with self.assertRaises(ValueError):
            s.hammadde_ekle("  ", "Kumaş", "m", 10, 5, self.dosya)
        self.assertEqual(s.stok_yukle(self.dosya), [])

    def test_ayni_kod_tekrar_eklenemez(self):
        s.hammadde_ekle("IP01", "İplik", "adet", 50, 10, self.dosya)
        with self.assertRaises(ValueError):
            s.hammadde_ekle("ip01", "İplik 2", "adet", 5, 1, self.dosya)

    def test_veri_kalici(self):
        s.hammadde_ekle("DGM01", "Düğme", "adet", 500, 100, self.dosya)
        self.assertEqual(s.stok_yukle(self.dosya)[0]["ad"], "Düğme")


class KartIkiTesti(unittest.TestCase):
    def setUp(self):
        self.klasor = tempfile.TemporaryDirectory()
        self.addCleanup(self.klasor.cleanup)
        self.dosya = os.path.join(self.klasor.name, "stok.json")

    def test_tum_kritik_stoklar_ve_siparis_farki(self):
        s.hammadde_ekle("K1", "Kumaş", "m", 30, 100, self.dosya)
        s.hammadde_ekle("I1", "İplik", "kg", 50, 20, self.dosya)
        s.hammadde_ekle("D1", "Düğme", "adet", 100, 250, self.dosya)
        s.hammadde_ekle("F1", "Fermuar", "adet", 20, 20, self.dosya)
        sonuc = s.kritik_stok_kontrol(self.dosya)
        self.assertEqual([(h["kod"], h["siparis_miktari"]) for h in sonuc],
                         [("K1", 70), ("D1", 150)])

    def test_bos_stok(self):
        self.assertEqual(s.kritik_stok_kontrol(self.dosya), [])

    def test_esit_ve_yeterli_stok(self):
        s.hammadde_ekle("K1", "Kumaş", "m", 20, 20, self.dosya)
        s.hammadde_ekle("I1", "İplik", "kg", 30, 20, self.dosya)
        self.assertEqual(s.kritik_stok_kontrol(self.dosya), [])

    def test_uyari_ekran_ciktisi(self):
        from contextlib import redirect_stdout
        from io import StringIO
        s.hammadde_ekle("K1", "Kumaş", "m", 30, 100, self.dosya)
        cikti = StringIO()
        with redirect_stdout(cikti):
            s.kritik_stok_listele(self.dosya)
        self.assertIn("UYARI: Kumaş (K1)", cikti.getvalue())
        self.assertIn("Minimum sipariş miktarı: 70.00 m", cikti.getvalue())

    def test_sonlu_olmayan_miktar_reddedilir(self):
        for miktar in ("nan", "inf", "-inf"):
            with self.assertRaises(ValueError):
                s.hammadde_ekle("K1", "Kumaş", "m", miktar, 20, self.dosya)
        self.assertEqual(s.stok_yukle(self.dosya), [])


if __name__ == "__main__":
    unittest.main()
