#Tek Bantlı Turing Makinesi ile İkili Çarpma Hesaplayıcı

Bu proje, **Özdevinirler Kuramı (Theory of Computation)** dersi final ödevi kapsamında geliştirilmiş, Python tabanlı bir **Deterministik Turing Makinesi (DTM) Simülatörüdür**. 

Sistem, kullanıcıdan alınan iki adet binary (ikili) sayıyı aralarına `*` ve sonuna `=` sembollerini koyarak tek bir doğrusal şerit (bant) üzerinde birleştirir ve modern işlemcilerin çekirdeğinde yer alan **"Shift & Add" (Kaydır ve Topla)** algoritmasını durum geçişleriyle alt seviyede modeller.

---

#Sistemsel Özellikler & İsterler

- **Zorunlu Operand Ayrıştırma:** Girdiyi `Multiplicand * Multiplier =` formatına dönüştürerek `*` ve `=` sembolleriyle şerit üzerinde segment ve sınır yönetimi sağlar.
- **Güvenlik & Girdi Doğrulama:** Giriş alfabesi ($\Sigma$) dışındaki (`0` ve `1` harici) karakterleri simülasyona sokmadan doğrudan filtreler ve kullanıcıyı uyarır.
- **Anlık Loglama (Canlı Simülasyon):** Makine çalışırken her adımda; *mevcut durumu*, *okunan sembolü*, *yazılan sembolü*, *kafanın hareket yönünü (R/L/N)* ve *bandın anlık içeriğini* terminalde görselleştirir.

---

#Kurulum ve Çalıştırma

Projenin bilgisayarınızda çalıştırılması için herhangi bir harici kütüphaneye (dependencies) ihtiyaç yoktur. Standart Python 3 ortamı yeterlidir.

Depoyu yerel bilgisayarınıza clone ettikten sonra veya kaynak kodun bulunduğu dizinde terminal (CMD) açarak şu komutla simülasyonu başlatabilirsiniz:

```bash
python turing_calculator.py
