# MIX TEST PDFMATCH

Tek Windows uygulaması içinde **AHU Match (PDF Match)** ve **TEST KONTROL**.

## Kullanım
1. Programı açın.
2. Ana ekrandan **PDF MATCH** veya **TEST KONTROL** seçin.
3. Seçilen uygulama kendi ekranı ve işlevleriyle açılır.

## Depo yapısı
- `pdf_match/`: PDF/AHU/motor eşleştirme uygulaması, testleri ve varlıkları
- `test_kontrol/`: C600, fan, damper, filtre, modül, sensör ve rapor araçları
- `launcher.py`: Ana seçim ekranı
- `unified_updater.py`: Her iki uygulamanın kullandığı tek güncelleme altyapısı
- `.github/workflows/build-windows.yml`: İki uygulamayı test eden ve tek EXE yayımlayan ortak akış

## Tek EXE ve tek güncelleme
GitHub Actions iki uygulamanın testlerini çalıştırır, tek `Mix_Test_PDFMatch` EXE'sini üretir ve aynı `latest` GitHub Release'e yayımlar. Ana ekran ve iki modül ortak güncelleme altyapısını kullanır.

## Kaynak projeler
- PDF Match: https://github.com/dincer552/pdf_kw_selector
- TEST KONTROL: https://github.com/dincer552/test-kontrol-pa

Büyük örnek PDF dosyaları API aktarım sınırı nedeniyle bu depoda yinelenmedi; ortak Windows workflow regression testlerinden önce kaynak depodan indirir.
