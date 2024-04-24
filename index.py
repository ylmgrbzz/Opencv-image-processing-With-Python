import cv2
import numpy as np

def show_pixel_color(event, x, y, flags, param):
    global rgba_color_shown, labeled_image_copy

    if event == cv2.EVENT_MOUSEMOVE:
        bgr_color = labeled_image[y, x]
        rgba_color = np.append(bgr_color[::-1], 255)  # BGR'den RGB'ye dönüştürme ve alpha değerini ekleyerek RGBA oluşturma

        # Renk değerlerini 0-255 aralığından 0-20 aralığına dönüştürme
        new_rgba_color = np.clip((rgba_color / 255) * 20, 0, 20)
        new_rgba_color = new_rgba_color.astype(np.uint8)

        if rgba_color_shown is None or not np.array_equal(rgba_color, rgba_color_shown):
            print(f"Renk tonu (RGBA): {rgba_color} -> Yeni Renk Tonu: {new_rgba_color}")
            rgba_color_shown = rgba_color

        # Yeni renk tonunu resmin üzerine yazdırma
        labeled_image_copy = labeled_image.copy()  # Her seferinde temiz bir kopya oluştur
        cv2.putText(
            labeled_image_copy,
            str(new_rgba_color),
            (x, y),  # Metni fare imlecinin altına yerleştirme
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),  # Beyaz renkte yazma
            1,
            cv2.LINE_AA,
        )

        # Görüntüyü gösterme
        cv2.imshow("İşaretlenmiş Resim", labeled_image_copy)

# Yeni ton aralığı
new_min = 0
new_max = 20

def rescale_gray_image(gray_image, new_min, new_max):
    # Mevcut ton aralığını bulma
    current_min = np.min(gray_image)
    current_max = np.max(gray_image)

    # Yeniden ölçeklendirilmiş tonları hesaplama
    rescaled_image = ((gray_image - current_min) / (current_max - current_min)) * (new_max - new_min) + new_min

    return rescaled_image.astype(np.uint8)

# Resmi gri tonlamalı olarak okuma
image_path = "resim.jpg"  # Yerel dosyanın yolunu buraya koyun
gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Gri tonlamalı resmi yeniden ölçeklendirme
rescaled_gray_image = rescale_gray_image(gray_image, new_min, new_max)

# Resimdeki benzersiz tonları bulma
unique_tones = np.unique(gray_image)  # Rescaled değil, orijinal gri tonlamalı resmin tonlarını bul

# Tonları koyudan açığa doğru numaralandırma
tone_indices = {tone: idx for idx, tone in enumerate(sorted(unique_tones), start=1)}

# Resmi kopyalayarak üzerine tonları işaretleme
labeled_image = cv2.cvtColor(gray_image.copy(), cv2.COLOR_GRAY2BGR)
labeled_image_copy = labeled_image.copy()  # İşlem yapılacak kopya resim

# RGBA değerini göstermek için bir bayrak
rgba_color_shown = None

# Görüntüyü gösterme
cv2.imshow("İşaretlenmiş Resim", labeled_image)
cv2.setMouseCallback("İşaretlenmiş Resim", show_pixel_color)  # Mouse etkinliğini dinleme

cv2.waitKey(0)  # Bir tuşa basılana kadar bekletme
cv2.destroyAllWindows()  # Pencereleri kapatma
