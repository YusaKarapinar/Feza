import cv2

# Kamerayı başlat (0, varsayılan kamerayı açar)
cap = cv2.VideoCapture(1)

# Video codec ve çıktı dosyası ayarları
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while(1):
    ret, frame = cap.read()
    if ret == True:
        # Çerçeveyi videoya yaz
        out.write(frame)

        # Ekranda çerçeveyi göster
        cv2.imshow('frame', frame)

        # 'q' tuşuna basılırsa kaydı durdur
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Her şeyi serbest bırak
cap.release()
out.release()
cv2.destroyAllWindows()
