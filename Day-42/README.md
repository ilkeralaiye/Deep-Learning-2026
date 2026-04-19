# 📷 YOLO Webcam Nesne Tespiti

Webcam görüntüsü üzerinde **Ultralytics YOLO11** kullanarak gerçek zamanlı nesne tespiti yapan basit bir Python projesi.

---

## 🚀 Kurulum

```bash
pip install -r requirements.txt
```

---

## ▶️ Çalıştırma

```bash
python webcam_detection.py
```

İlk çalıştırmada model ağırlıkları (~6 MB) otomatik indirilir.

---

## ⚙️ Ayarlar (`webcam_detection.py` içinde)

| Değişken | Açıklama | Varsayılan |
|---|---|---|
| `MODEL_NAME` | Kullanılacak YOLO modeli | `yolo11n.pt` (en hızlı) |
| `CONFIDENCE` | Minimum güven skoru | `0.40` |
| `CAMERA_INDEX` | Kamera numarası | `0` |
| `PRINT_EVERY` | Konsola yazma sıklığı (sn) | `1.0` |

### Kullanılabilir Modeller (hız ↔ doğruluk dengesi)

| Model | Boyut | Hız |
|---|---|---|
| `yolo11n.pt` | ~6 MB | En hızlı |
| `yolo11s.pt` | ~22 MB | Hızlı |
| `yolo11m.pt` | ~52 MB | Orta |
| `yolo11l.pt` | ~87 MB | Yavaş |
| `yolo11x.pt` | ~136 MB | En yavaş / en doğru |

---

## 🖥️ Çıktı Örneği

```
[16:20:01] Tespit edilenler: person, cell phone, cup (2)
[16:20:02] Tespit edilenler: person, laptop
[16:20:03] Nesne tespit edilmedi.
```

---

## ⌨️ Kontroller

- **`q`** → Programı kapat
