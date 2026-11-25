"""Textile MRP Tracker - Kart 1 ve Kart 2: Hammadde kaydı ve kritik stok uyarısı."""
import json
import os
import math

STOK_DOSYASI = "stok.json"


def stok_yukle(dosya=STOK_DOSYASI):
    """stok.json dosyasını okur; dosya yoksa veya bozuksa boş liste döner."""
    if not os.path.exists(dosya):
        return []
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def stok_kaydet(stok, dosya=STOK_DOSYASI):
    """Stok listesini stok.json dosyasına kalıcı olarak yazar."""
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(stok, f, ensure_ascii=False, indent=2)


def hammadde_ekle(kod, ad, birim, miktar, emniyet_stogu, dosya=STOK_DOSYASI):
    """Yeni hammadde ekler. Geçersiz girişte ValueError fırlatır."""
    kod = str(kod).strip().upper()
    ad = str(ad).strip()
    birim = str(birim).strip()

    if not kod:
        raise ValueError("Malzeme kodu boş olamaz.")
    if not ad:
        raise ValueError("Malzeme adı boş olamaz.")
    if not birim:
        raise ValueError("Birim cinsi boş olamaz.")
    try:
        miktar = float(miktar)
        emniyet_stogu = float(emniyet_stogu)
    except (TypeError, ValueError):
        raise ValueError("Miktar ve emniyet stoğu sayı olmalıdır.")
    if not math.isfinite(miktar) or not math.isfinite(emniyet_stogu):
        raise ValueError("Miktarlar sonlu sayı olmalıdır.")
    if miktar < 0:
        raise ValueError("Miktar negatif olamaz.")
    if emniyet_stogu < 0:
        raise ValueError("Emniyet stoğu negatif olamaz.")

    stok = stok_yukle(dosya)
    if any(h["kod"] == kod for h in stok):
        raise ValueError(f"'{kod}' kodlu malzeme zaten kayıtlı.")

    hammadde = {
        "kod": kod,
        "ad": ad,
        "birim": birim,
        "miktar": miktar,
        "emniyet_stogu": emniyet_stogu,
    }
    stok.append(hammadde)
    stok_kaydet(stok, dosya)
    return hammadde


def stok_listele(dosya=STOK_DOSYASI):
    """Kayıtlı tüm hammaddeleri ekrana yazdırır."""
    stok = stok_yukle(dosya)
    if not stok:
        print("Kayıtlı hammadde yok.")
        return
    print(f"{'Kod':<10}{'Ad':<20}{'Birim':<8}{'Miktar':>10}{'Emniyet':>10}")
    print("-" * 58)
    for h in stok:
        print(f"{h['kod']:<10}{h['ad']:<20}{h['birim']:<8}"
              f"{h['miktar']:>10.2f}{h['emniyet_stogu']:>10.2f}")


def kritik_stok_kontrol(dosya=STOK_DOSYASI):
    """Emniyet stoğunun altındaki hammaddeleri ve sipariş ihtiyacını döndürür."""
    return [
        {**h, "siparis_miktari": h["emniyet_stogu"] - h["miktar"]}
        for h in stok_yukle(dosya)
        if h["miktar"] < h["emniyet_stogu"]
    ]


def kritik_stok_listele(dosya=STOK_DOSYASI):
    """Kritik hammaddeleri birimleriyle birlikte ekrana yazdırır."""
    kritik = kritik_stok_kontrol(dosya)
    print("\n=== KRİTİK STOK RAPORU ===")
    if not kritik:
        print("Kritik seviyede hammadde bulunmamaktadır.")
        return
    for h in kritik:
        print(f"UYARI: {h['ad']} ({h['kod']})")
        print(f"Mevcut stok: {h['miktar']:.2f} {h['birim']}")
        print(f"Emniyet stoğu: {h['emniyet_stogu']:.2f} {h['birim']}")
        print(f"Minimum sipariş miktarı: {h['siparis_miktari']:.2f} {h['birim']}")
    print(f"Toplam kritik hammadde: {len(kritik)}")


def menu():
    while True:
        print("\n=== Textile MRP Tracker ===")
        print("1) Hammadde ekle")
        print("2) Stokları listele")
        print("3) Kritik stok ve sipariş uyarıları")
        print("0) Çıkış")
        secim = input("Seçiminiz: ").strip()
        if secim == "1":
            try:
                h = hammadde_ekle(
                    input("Malzeme kodu: "),
                    input("Malzeme adı: "),
                    input("Birim cinsi (m, kg, adet): "),
                    input("Mevcut miktar: "),
                    input("Emniyet stoğu eşiği: "),
                )
                print(f"Kaydedildi: {h['kod']} - {h['ad']}")
            except ValueError as e:
                print(f"HATA: {e}")
        elif secim == "2":
            stok_listele()
        elif secim == "3":
            kritik_stok_listele()
        elif secim == "0":
            print("Çıkılıyor.")
            break
        else:
            print("Geçersiz seçim.")


if __name__ == "__main__":
    menu()
