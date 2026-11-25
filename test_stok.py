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


if __name__ == "__main__":
    unittest.main()
