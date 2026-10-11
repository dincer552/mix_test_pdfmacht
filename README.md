# MIX TEST PDFMATCH

Birleşik AHU Match + Test Kontrol Windows masaüstü uygulaması.

## Mimari

- `desktop_grouped_app.py`: AHU Match PDF analiz arayüzü
- `test_kontrol/`: TEST KONTROL arayüzü ve yardımcı modülleri
- `launcher.py`: İki uygulama işlevine tek pencereden erişim sağlayan başlangıç arayüzü

Mevcut uygulamaların davranışlarını korumak için kodlar ayrı klasörlerde tutulur. Birleşik başlangıç ekranı her iki işlevi de tek paketten açar.

## Build

Windows Python 3.11 kullanın. Bağımlılıklar kök `requirements.txt` dosyasında birleştirilir.

> Bu ilk depo iskeletidir. Birleşik EXE üretimi, import yolu uyarlamaları ve regresyon testleri CI üzerinden doğrulanmalıdır.
