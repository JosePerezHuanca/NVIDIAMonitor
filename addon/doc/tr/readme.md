# NVIDIA Monitörü

Bu eklenti, NVIDIA grafik kartlarının adı, kullanılan bellek, boş ve toplam bellek, güç tüketimi, sıcaklık ve daha fazlası gibi çeşitli parametrelerini izlemenizi sağlar.

## Kısayollar

Not: Bazı bilgi parametreleri, ekran kartına bağlı olarak uyumlu olmayabilir veya desteklenmeyebilir.
Aşağıdaki tüm kısayollar, girdi hareketleri/NVIDIA Monitörü kategorisinde özelleştirilebilir. Bir kısayola iki kez basmak, bilgiyi panoya kopyalar.

- NVDA + alt + g: GPU adını/modelini seslendirir.
- NVDA + alt + u: GPU UUID'sini seslendirir.
- NVDA + alt + v: Sürücü sürümünü seslendirir.
- NVDA + ctrl + alt + v: BIOS sürümünü seslendirir.
- NVDA + alt + 1: GPU yükünü seslendirir.
- NVDA + alt + 2: Bellek yükünü seslendirir.
- NVDA + alt + 3: Boş bellek boyutunu seslendirir.
- NVDA + alt + 4: Kullanılan bellek boyutunu seslendirir.
- NVDA + alt + 5: Toplam bellek boyutunu seslendirir.
- NVDA + alt + 6: GPU sıcaklığını seslendirir.
- NVDA + alt + 7: Güç tüketimini seslendirir.
- NVDA + alt + 8: Güç sınırını seslendirir.
- NVDA + alt + 9: CUDA süreçlerinin sayısını seslendirir.
- NVDA + alt + 0: İşlemler tarafından kullanılan bellek boyutunu seslendirir.
- NVDA + ctrl + alt + 1: Fan hızını seslendirir.
- NVDA + ctrl + alt + 2: GPU saat frekansını seslendirir.
- NVDA + ctrl + alt + 3: GPU'nun maksimum saat frekansını seslendirir.
- NVDA + ctrl + alt + 4: SM saat frekansını seslendirir.
- NVDA + ctrl + alt + 5: Maksimum SM saat frekansını seslendirir.
- NVDA + ctrl + alt + 6: Bellek saat frekansını seslendirir.
- NVDA + ctrl + alt + 7: Belleğin maksimum saat frekansını seslendirir.
- NVDA + ctrl + alt + 8: İletim hızını seslendirir.
- NVDA + ctrl + alt + 9: RX veri aktarım hızını seslendirir.
- NVDA + ctrl + alt + 0: Güç durumunu seslendirir.


## Değişiklik Günlüğü

### Sürüm 2.1

- Doğrudan pynvml çağrılarıyla ilgili bir sorun düzeltildi.

### Sürüm 2.0

- NVDA 2026.1 ile uyumlu.
- Bu sürümden itibaren, eklenti NVDA'nın en son sürümünde çalışırken harici bir araç kullanmak yerine doğrudan pynvml kütüphanesine çağrılar yapmaktadır.

### Sürüm 1.0

- Bilgi alma komut dosyasında çeşitli değişiklikler, düzeltmeler ve iyileştirmeler yapıldı.
- Hatalar artık NVDA yapılandırma klasöründe bulunan NVIDIAMonitor.log adlı bir dosyaya kaydediliyor.
- NVDA 2025.1 ile uyumlu.
- Bazı mevcut kısayollar yeniden atandı.
- Yeni kısayollar eklendi:
  - GPU UUID: NVDA + alt + u
  - Sürücü sürümü: NVDA + alt + v
  - BIOS sürümü: NVDA + ctrl + alt + v
  - Bellek yükü: NVDA + alt + 2
  - Güç sınırı: NVDA + alt + 8
  - İşlemler tarafından kullanılan bellek: NVDA + alt + 0
  - Maksimum GPU saat frekansı: NVDA + ctrl + alt + 3
  - SM saat frekansı: NVDA + ctrl + alt + 4
  - Maksimum SM saat frekansı: NVDA + ctrl + alt + 5
  - Bellek saat frekansı: NVDA + ctrl + alt + 6
  - Maksimum bellek saat frekansı: NVDA + ctrl + alt + 7
  - TX veri aralığı: NVDA + ctrl + alt + 8
  - RX veri hızı: NVDA + ctrl + alt + 9
  - Güç durumu: NVDA + ctrl + alt + 0

### Sürüm 0.2

- Artık kısayol tuşuna iki kez basıldığında bilgi panoya kopyalanıyor.
- Çeşitli iyileştirmeler ve optimizasyonlar.

### Sürüm 0.1

- Eklentinin ilk sürümü.
