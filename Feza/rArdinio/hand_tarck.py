import serial 
import time 
import cv2
import numpy as np

def nothing(int):
    pass

arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1) 

def write_read(y,x): 
    arduino.write(bytes(y+str(x), 'utf-8')) 
    time.sleep(0.05)

cv2.namedWindow("D")
cv2.createTrackbar("D", "D", 0, 180, nothing)
cv2.setTrackbarPos("D", "D", 90)

cap = cv2.VideoCapture(0)
Gonderilmis=0
old_x=0
old_y=0
print()
while True:
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)

    frame=cv2.medianBlur(frame,5)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Kırmızı rengin HSV aralığını tanımla
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Maske oluştur
    mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    # Maskeyi kullanarak kırmızı renkli nesneleri bul
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # En büyük konturu bul
    largest_contour = max(contours, key=cv2.contourArea, default=None)

    # En büyük kontur varsa ve yalnızca bir tane varsa
    if largest_contour is not None :
        # Konturun sınırlayıcı kutusunu al
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Konturun merkezini hesapla
        center_x = x + w // 2
        center_y=y+h//2

        # Sağa doğru hareket eden piksel sayısını hesapla
        movement1 = center_x - old_x
        movement2 = center_y - old_y

        # Ekrana hareket eden piksel sayısını yazdır

        # Yeni x konumunu güncelle
        old_x = center_x
        old_y=center_y
        if (movement1>10 or movement1<-10):
            write_read("x",movement1)
            print("Yatay:", movement1)

        
        if (movement2>10 or movement2<-10):
            write_read("y",movement2)
            print("Dikey:", movement2)

        
    if cv2.waitKey(24) & 0xFF == ord("q"):
        break
    cv2.imshow("D",frame)
    cv2.imshow("s",mask)

cap.release()
cv2.destroyAllWindows()
