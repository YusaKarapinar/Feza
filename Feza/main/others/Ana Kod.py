import cv2
import numpy as np
import mMod



    #mode =input("Hangi Modu kullanma istiyorsunuz:\n");
    #if(mode=="0"):
    #    break
directiory=input("Hangi Dosyayı Kullanmak isyiyorsunuz:\n");
directiory="src/video/vid"+directiory+".mp4"
print(directiory)
    
#if(mode=="1"):#şimdilik tek bir mod var o yüzden sormuyorum
mMod.Mod1(directiory)

    