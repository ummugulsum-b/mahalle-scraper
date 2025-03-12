# Mahalle Verisi İndirme ve İşleme Projesi

Bu proje, belirtilen [İçişleri Bakanlığı Mülki İdari Birimleri](https://www.e-icisleri.gov.tr/Anasayfa/MulkiIdariBolumleri.aspx) web sitesinden mahalle verilerini indirip işleyen bir Python uygulamasıdır. PDF dosyasından mahalle verilerini çıkarır ve JSON ve CSV formatlarında kaydeder. Ayrıca, bu işlemi her hafta bir kez otomatik olarak yapacak şekilde zamanlanmıştır.

## Özellikler
- Web sayfasından PDF dosyasını otomatik olarak indirir.
- PDF dosyasından mahalle bilgilerini çıkarır.
- Çıkarılan verileri JSON ve CSV formatlarında kaydeder.
- Her hafta otomatik olarak veri indirir ve işler.

## Gereksinimler
Projede kullanılan kütüphaneleri yüklemek için şu komutu çalıştırabilirsiniz:
```bash
pip install -r requirements.txt
```

## Veri Güncelleme

Bu proje, mahalle verilerini her hafta otomatik olarak günceller. Aşağıdaki adımlar ile veri güncellenir:

1. **Selenium** kullanılarak [İçişleri Bakanlığı Mülki İdari Birimleri](https://www.e-icisleri.gov.tr/Anasayfa/MulkiIdariBolumleri.aspx) web sitesinden güncel PDF dosyası indirilir.
2. **pdfplumber** ile PDF dosyasından mahalle bilgileri çıkarılır.
3. Çıkarılan veriler **CSV** ve **JSON** formatlarında kaydedilir.
4. **Schedule** kütüphanesi sayesinde bu işlem her hafta otomatik olarak tekrarlanır.

Veri güncellemelerini otomatik hale getirmek için **schedule** kütüphanesi arka planda çalışır ve belirli bir zaman diliminde (haftalık olarak) güncelleme işlemi yapılır. Bu sayede veriler her hafta yenilenir ve en güncel bilgiler elde edilir.
