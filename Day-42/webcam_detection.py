"""
Webcam Object Detection using Ultralytics YOLO
================================================
Bu betik webcam'i açarak gerçek zamanlı nesne tespiti yapar.
Tespit edilen nesneler hem ekrana yazdırılır hem de görüntüde gösterilir.
"""

import cv2
from ultralytics import YOLO
from collections import Counter
import time


# ─────────────────────────────────────────────
# Ayarlar
# ─────────────────────────────────────────────
MODEL_NAME   = "yolo11n.pt"      # küçük & hızlı; alternatif: yolo11s.pt, yolo11m.pt
CONFIDENCE   = 0.40              # minimum güven skoru (0-1 arası)
CAMERA_INDEX = 0                 # varsayılan kamera (0 = built-in, 1 = harici)
PRINT_EVERY  = 1.0               # kaç saniyede bir konsola yazdır (saniye)


def draw_detections(frame, results):
    """Tespit kutularını ve etiketleri kare üzerine çizer."""
    annotated = results[0].plot()   # ultralytics'in kendi çizici metodu
    return annotated


def get_detected_labels(results, conf_threshold=CONFIDENCE):
    """Sonuçlardan güven skoru yeterli etiketleri döndürür."""
    labels = []
    for box in results[0].boxes:
        conf = float(box.conf[0])
        if conf >= conf_threshold:
            cls_id = int(box.cls[0])
            name   = results[0].names[cls_id]
            labels.append((name, conf))
    return labels


def main():
    print("=" * 50)
    print("  YOLO Webcam Nesne Tespiti Başlatılıyor...")
    print("=" * 50)

    # Model yükleme (ilk çalıştırmada otomatik indirilir)
    print(f"\n[INFO] Model yükleniyor: {MODEL_NAME}")
    model = YOLO(MODEL_NAME)
    print("[INFO] Model hazır!\n")

    # Kamera açma
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[HATA] Kamera açılamadı! Kamera bağlantısını kontrol edin.")
        return

    print("[INFO] Webcam açıldı. Çıkmak için 'q' tuşuna basın.\n")

    last_print_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[HATA] Kameradan görüntü alınamadı.")
            break

        # YOLO ile tahmin — verbose=False çünkü kendi çıktımızı yönetiyoruz
        results = model(frame, conf=CONFIDENCE, verbose=False)

        # Etiketleri al
        detected = get_detected_labels(results)

        # Belirli aralıklarla konsola yazdır
        now = time.time()
        if now - last_print_time >= PRINT_EVERY:
            if detected:
                counts = Counter(name for name, _ in detected)
                items  = ", ".join(
                    f"{k} ({v})" if v > 1 else k
                    for k, v in counts.items()
                )
                print(f"[{time.strftime('%H:%M:%S')}] Tespit edilenler: {items}")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Nesne tespit edilmedi.")
            last_print_time = now

        # Görüntüyü çiz ve göster
        annotated_frame = draw_detections(frame, results)
        cv2.imshow("YOLO - Webcam Nesne Tespiti  (q: çıkış)", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("\n[INFO] Kullanıcı 'q' tuşuna bastı. Çıkılıyor...")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Program sonlandı.")


if __name__ == "__main__":
    main()
