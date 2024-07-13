import cv2
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))



def Mod1(directory):
    
    lk_params = dict(winSize  = (15, 15),
                    maxLevel = 2,
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    
    feature_params = dict(maxCorners = 20,
                        qualityLevel = 0.3,
                        minDistance = 10,
                        blockSize = 7 )
    
    
    trajectory_len = 20
    detect_interval = 5
    trajectories = []
    frame_idx = 0
    cap=cv2.VideoCapture(directory)
    
    while True:
        #acil durum bilgisini ardiniodan al
    
        #acil durum butonu kontrol
        #if emergency_button==True:
        #    break
        #else:
        #    pass
        #
        
        ret,img_bgr =cap.read()
        if ret==0:
            break
        img_bgr=cv2.resize(img_bgr,(640,480))
        frame_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV_FULL)
    
        # Düşük doygunluk değerlerini filtrele (arkaplanda büyük ölçüde gri tonlu pikseller)
        bgd_mask = cv2.inRange(img_hsv, np.array([0, 0, 0]), np.array([255, 30, 255]))
    
        black_maske = cv2.inRange(img_bgr, np.array([0, 0, 0]), np.array([70, 70, 70]))
    
        white_maske = cv2.inRange(img_bgr, np.array([230, 230, 230]), np.array([255, 255, 255]))
    
        final_mask = cv2.max(bgd_mask, black_maske)
        final_mask = cv2.min(final_mask, ~white_maske)
        final_mask = ~final_mask
    
        final_mask = cv2.erode(final_mask, np.ones((3, 3), dtype=np.uint8))
        final_mask = cv2.dilate(final_mask, np.ones((5,5), dtype=np.uint8))
        
    
        # Konturları bul
        contours, hierarchy = cv2.findContours(final_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
        final_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 200:
                final_contours.append(contour)
    
        # Konturları alanlarına göre sırala
        final_contours.sort(key=cv2.contourArea, reverse=True)
        
    
        # Her kontur için numaralandırma ve yazı ekleme
        kontur_sayaci=0
        dosya = open("kontur_bilgileri.txt", "w")
    
        for i, contour in enumerate(final_contours):
            kontur_sayaci += 1
            
            area = cv2.contourArea(contour)
            (x,y,w,h) = cv2.boundingRect(contour) 
            cv2.rectangle(img_bgr,(x,y),(x+w, y+h),(255,0,0),3)  
            # Konturun merkez koordinatlarını bul
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Konturun rengini al
            renk = img_bgr[cY, cX]
            # Konturun etrafına numara, rengi ve alanı yaz
            cv2.putText(img_bgr, f"{1 if kontur_sayaci == 1 else kontur_sayaci}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
            cv2.putText(img_bgr, f"Area: {area}", (cX, cY + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(img_bgr, f"Color: {renk}", (cX, cY + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            # Kontur bilgilerini dosyaya yaz
    
            dosya.write(f"Kontur ID: {kontur_sayaci}, Renk: {renk}, Konum: ({cX}, {cY}), Alan: {area} , Merkeze uzaklik: ({cX-320},{cY-200})\n")
        dosya.close()
    
        debug_img = img_bgr
        
        cv2.drawContours(debug_img,final_contours,-1, (0, 255, 0), 3)
    
        #cv2.imshow("final_mask", final_mask)
        #cv2.imshow("white_maske", white_maske)
        #cv2.imshow("black_maske", black_maske)
        #cv2.imshow("bgd_mask", bgd_mask)
        #BURDAN SONRASI DENEME
        if len(trajectories) > 0:
            img0, img1 = prev_gray, frame_gray
            p0 = np.float32([trajectory[-1] for trajectory in trajectories]).reshape(-1, 1, 2)
            p1, _st, _err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
            p0r, _st, _err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
            d = abs(p0-p0r).reshape(-1, 2).max(-1)
            good = d < 1
    
            new_trajectories = []
    
            # Get all the trajectories
            for trajectory, (x, y), good_flag in zip(trajectories, p1.reshape(-1, 2), good):
                if not good_flag:
                    continue
                trajectory.append((x, y))
                if len(trajectory) > trajectory_len:
                    del trajectory[0]
                new_trajectories.append(trajectory)
                # Newest detected point
    
            trajectories = new_trajectories
        
        if frame_idx % detect_interval == 0:
            mask = np.zeros_like(frame_gray)
            mask[:] = 255
    
            # Lastest point in latest trajectory
            for x, y in [np.int32(trajectory[-1]) for trajectory in trajectories]:
                cv2.circle(mask, (x, y), 5, 0, -1)
    
            # Detect the good features to track
            p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
            if p is not None:
                # If good features can be tracked - add that to the trajectories
                for x, y in np.float32(p).reshape(-1, 2):
                    trajectories.append([(x, y)])
    
    
        frame_idx += 1
        prev_gray = frame_gray
    
        
        # Show Results
        cv2.imshow('Mask', mask)
        cv2.imshow("debug_img", debug_img)
        cv2.imshow("bgd",bgd_mask) 
        cv2.imshow("b",black_maske )
        cv2.imshow("w", white_maske )
        cv2.imshow("f", final_mask)
        out.write(debug_img)
        out.write(debug_img)
        out.write(debug_img)

        if cv2.waitKey(100) & 0xFF==ord("q"):
            break

    # Dosyayı kapat
    cv2.destroyAllWindows()
    out.release()

        
    #640 genişlik 400 uzunluk
    #640/180 
    #400/180
    #merkez (320,200)
    # Dosyaya yazma modunda dosyayı aç
    