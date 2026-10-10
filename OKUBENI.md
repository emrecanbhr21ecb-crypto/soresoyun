# Şoreş Oyuncak Atölyesi — v3 (tamamlandı)

Make More! tarzı idle oyun. Phaser 3 + Capacitor → Android APK.
Görseller Google Gemini (Nano Banana Pro) ile üretildi.

## Klasör yapısı
```
soresoyun/
├── www/index.html            ← OYUNUN TAMAMI (tek dosya)
├── www/art/                  ← Gemini görselleri (31 dosya, ~2 MB)
├── www/lib/phaser.min.js     ← Phaser 3.90 (yerel, internet gerekmez)
├── www/index-asama1-yedek.html ← v1 yedeği
├── art/                      ← görsel üretim/işleme araçları (APK'ya girmez)
│   ├── raw/                  ← Gemini'den inen ham JPEG'ler
│   ├── slice.py              ← yeşil fonu siler + sprite sayfasını böler
│   └── gen.py                ← API ile üretim (kota açıkken)
└── android/                  ← Capacitor'ın ürettiği Android projesi
```

## Oyunu tarayıcıda test etme
```bash
cd ~/Desktop/soresoyun/www && python3 -m http.server 8899
# tarayıcıda: http://localhost:8899
```
`www/index.html`'e çift tıklamak da çalışır.

## APK alma
```bash
cd ~/Desktop/soresoyun
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
export ANDROID_HOME="$HOME/Library/Android/sdk"
npx cap sync android
cd android && ./gradlew assembleDebug
cp app/build/outputs/apk/debug/app-debug.apk ~/Desktop/SoresFabrika.apk
```

## v3'te gelenler (6 promtluk rehber tamamlandı)
- **Robot İşçiler** — bir fabrikanın 9 masası da açık ve Sv.20 olunca PATRON
  panelinden satın alınır. Üretim ×5, patron seviyesine bakmadan her 1 sn'de
  oto-satış. Masalarda işçiler yerine robotlar görünür.
- **Prestij (Büyük Patron)** — PATRON panelinden şirketi satarsın.
  Kazanılan yıldız = `√(satılan ürün / 50.000)`. Her yıldız üretimi ve geliri
  **+%50** artırır, kalıcıdır. İki kez dokunma onayı ister.
  *Sıfırlanan:* nakit, fabrikalar, işçiler, masalar, patron seviyeleri.
  *Korunan:* yıldız, altın, rozetler, altınla alınan kalıcı güçler.
- **Koleksiyon (ROZET sekmesi)** — 12 karakter rozeti, altınla açılır, bonusları
  kalıcı: üretim +%5…+%20, satış geliri +%10…+%15, tıklama +%15/+%25,
  Noel rozeti hediyeyi 2 kat sık uçurur. **KUTU AÇ** (30 altın) rastgele
  kapalı rozet verir. Altınla alınabilir rozet varken sekmede kırmızı nokta çıkar.
- **Ses** — ses dosyası yok, tonlar WebAudio ile üretiliyor (tıklama, satış,
  satın alma, hata, hediye, büyük olay). AYARLAR'dan açılıp kapanır, kayda yazılır.
- Kupa sayısı 9'a çıktı, HUD'da yıldız çarpanı gösteriliyor.

## v2'de gelenler
- **5 fabrika**, yana kaydırarak veya HUD'daki oklarla geçiş
  | # | Fabrika | Patron | Ürün | Gelir | Açılış |
  |---|---------|--------|------|-------|--------|
  | 1 | Ahşap Atölyesi | Usta | Ahşap At | ×1 | — |
  | 2 | Boya Atölyesi | Hanım Patron | Boyalı Top | ×18 | 250K₺ |
  | 3 | Korsan Oyuncak | Korsan | Korsan Gemisi | ×320 | 25M₺ |
  | 4 | Sirk Fabrikası | Palyaço | Balon | ×6K | 3B₺ |
  | 5 | Robot Fabrikası | Sumo | Mini Robot | ×120K | 500B₺ |
- **İşçi seçme ekranı**: boş masaya dokun → 12 karakterden seç. Her birinin
  gücü (⚒ ×N) ve fiyatı farklı; güçlü işçi daha çok üretir, daha pahalıdır.
  Çalışan işçiye dokununca aynı ekran açılır, işçiyi değiştirebilirsin.
  Çırak ×1 → Sünger ×202. Fiyat masa sırasına ve fabrikaya göre de katlanır.
- **Patron zamanla büyüyor**: sattığın her ürün patrona XP verir.
  Seviye arttıkça patron büyür, satış fiyatı ×1.32 katlanır ve aksesuar kazanır
  (Sv.5 papyon → Sv.10 altın zincir → Sv.18 taç).
  **Sv.8'de oto-satış açılır** — patron kendi satmaya başlar.
- Yeni tasarım: "Sıcak Marangozhane" — SS'deki pembe-mor Make More görünümü yok.
- Ekran sarsıntısı, talaş parçacıkları, tıklama dalgası, uçan yazılar.

## Devam eden mekanikler (v1'den)
Masa kapasitesi 5→100, ekrana dokununca hızlanma, altınla kalıcı güçler,
uçan hediye, 6 kupa, LocalStorage otomatik kayıt, çevrimdışı üretim (maks 8 saat).

## Görselleri değiştirme / yenileme
1. Gemini'de aynı stil promptuyla üret, **fon düz yeşil #00FF00** iste.
2. İndir, `art/raw/` içine koy.
3. `python3 art/slice.py <dosya> <sütun> <satır> www/art "isim1,isim2,..."`
   — yeşili siler, kırpar, hepsini aynı ölçeğe getirir, şeffaf PNG yazar.
4. Dosya adları oyunun beklediği anahtarlar: `bg0..bg4.jpg`, `w0..w11.png`,
   `b0..b4.png`, `prod0..prod4.png`, `gift/desk/bossdesk/crate.png`.
5. Bir dosya eksikse oyun o parçayı kodla çizer — hiçbir zaman kırılmaz.

## Rehberdeki 6 aşamanın durumu
| Aşama | Konu | Durum |
|-------|------|-------|
| 1 | Temel döngü (1 işçi, patron, üretim, satış) | ✔ |
| 2 | 9 masalık grid, işçi alma, masa yükseltme | ✔ |
| 3 | İki para birimi, market, kalıcı/geçici güçler | ✔ |
| 4 | Uçan hediye, kostüm/koleksiyon | ✔ |
| 5 | Çoklu fabrika, robot işçiler, prestij | ✔ |
| 6 | Görsel cila, animasyon, ses, kayıt | ✔ |

## Denge ayarları nerede
Hepsi dosyanın üstünde tek yerde: `WORKERS` (güç/fiyat), `FACS` (gelir çarpanı,
açılış maliyeti), `DESK_MULT`, `BADGES`, `ROBOT_SPEED`, `STAR_BONUS`, `BOX_COST`
ve `G` nesnesindeki maliyet fonksiyonları.
