# Textile MRP Tracker (Tekstil Atölyesi Hammadde ve Emniyet Stoğu Takip Sistemi)

## Projenin Amacı ve Çözdüğü Problem
Küçük ve orta ölçekli tekstil atölyelerinde kumaş, iplik, düğme ve fermuar gibi hammaddelerin stok seviyeleri çoğunlukla manuel olarak takip edilmektedir. Bu durum, kritik seviyenin altına düşen malzemelerin geç fark edilmesine ve üretim hattında beklenmedik duruşlara yol açmaktadır. Bu proje, hammadde girişlerini kayıt altına alarak emniyet stoğunun altına düşen malzemeler için otomatik sipariş uyarısı üretir.

## Hedef Kitle
- Üretim planlama mühendisleri
- Tekstil atölyesi şefleri
- Depo ve malzeme sorumluları

## İş Takip Panosu
[GitHub Projects — İş Takip Panosu](https://github.com/users/karakayasudenur/projects/4)

## Proje kapsamı
- [Kart 1: Hammadde kayıt ve stok girişi](https://github.com/karakayasudenur/textile-mrp-tracker/issues/1): geliştirildi.
- [Kart 2: Kritik stok ve acil sipariş uyarısı](https://github.com/karakayasudenur/textile-mrp-tracker/issues/2): geliştirildi.
- [Kart 3: EOQ hesaplayıcı](https://github.com/karakayasudenur/textile-mrp-tracker/issues/3): planlandı.
- [Kart 4: BOM bazlı malzeme düşümü](https://github.com/karakayasudenur/textile-mrp-tracker/issues/4): planlandı.
- [Kart 5: Tedarik süresi ve termin takibi](https://github.com/karakayasudenur/textile-mrp-tracker/issues/5): planlandı.

## Kurulum ve Çalıştırma
Python 3 gereklidir. Harici Python paketi gerekmez.
Depoyu GitHub üzerinden Code > Download ZIP ile indirip açın veya Git kullanıyorsanız:

```bash
git clone https://github.com/karakayasudenur/textile-mrp-tracker.git
cd textile-mrp-tracker
```

Terminali proje klasöründe açın:

```bash
python stok_takip.py
```

Windows'ta `python` bulunamazsa `py`, macOS/Linux'ta gerekirse `python3` kullanın.

Menü:
- 1: Hammadde ekle
- 2: Stokları listele
- 3: Kritik stok ve sipariş uyarıları
- 0: Çıkış

Veriler çalışma klasöründeki `stok.json` dosyasına yazılır. Testler geçici dosyalar kullanır; gerçek stok verilerini değiştirmez.

## Özellik 1 — Hammadde kaydı ve kalıcılık testi
1. Menüde 1'i seçin. Sırasıyla `KMS01`, `Pamuklu Kumaş`, `m`, `30`, `100` girin. Beklenen: kayıt başarılı.
2. Menüde 2'yi seçin. Beklenen: KMS01, mevcut 30, emniyet 100 listelenir.
3. 0 ile çıkıp yeniden çalıştırın ve 2'yi seçin. Beklenen: kayıt korunur.
4. Farklı bir kodla negatif miktar girin; ayrıca boş kod ile kayıt deneyin. Beklenen: hata mesajı, yeni kayıt oluşmaması.

## Özellik 2 — Kritik stok ve minimum sipariş testi
Yukarıdaki KMS01 kaydına ek olarak menü 1 ile aşağıdaki kayıtları girin (temiz bir veri dosyasıyla deneyin veya benzersiz kodlar kullanın):

| Kod | Ad | Birim | Miktar | Emniyet stoğu |
|---|---|---|---:|---:|
| IP01 | İplik | kg | 50 | 20 |
| DGM01 | Düğme | adet | 100 | 250 |
| FRM01 | Fermuar | adet | 20 | 20 |

Menüde 3'ü seçin. Beklenen: yalnızca KMS01 ve DGM01 kritik olarak listelenir; sipariş miktarları sırasıyla 70 m ve 150 adet olur. Emniyet stoğuna eşit veya üzerinde olan malzemeler uyarıya dahil edilmez.

Minimum sipariş miktarı = emniyet stoğu − mevcut miktar (yalnızca mevcut miktar eşikten küçükse). Bu miktar EOQ değildir.

## Otomatik Testler

```bash
python -m unittest -v
```

10 test; geçerli kayıt, kalıcılık, boş kod, negatif miktar, yinelenen kod, boş stok, eşit/yeterli stok, kritik stokların seçimi ve sipariş farkı, rapor çıktısı ve sonlu olmayan miktarların reddini kapsar.
