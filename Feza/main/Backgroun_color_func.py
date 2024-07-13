import sys                      # System bindings
import cv2                      # OpenCV bindings
import numpy as np
from collections import Counter


class BackgroundColorDetector():
    def __init__(self, imageLoc):
        self.img = imageLoc
        self.manual_count = {}
        self.w, self.h, self.channels = self.img.shape
        self.total_pixels = self.w * self.h

    def count(self):
        for y in range(0, self.h):
            for x in range(0, self.w):
                RGB = (self.img[x, y, 2], self.img[x, y, 1], self.img[x, y, 0])
                if RGB in self.manual_count:
                    self.manual_count[RGB] += 1
                else:
                    self.manual_count[RGB] = 1

    def average_colour(self):
        red = 0
        green = 0
        blue = 0
        sample = 10
        for top in range(0, sample):
            red += self.number_counter[top][0][0]
            green += self.number_counter[top][0][1]
            blue += self.number_counter[top][0][2]

        average_red = red / sample
        average_green = green / sample
        average_blue = blue / sample
        return [average_red, average_green, average_blue]  # Tuple yerine liste olarak döndür

    def twenty_most_common(self):
        self.count()
        self.number_counter = Counter(self.manual_count).most_common(20)

    def detect_background_color(self):
        self.twenty_most_common()
        self.percentage_of_first = (float(self.number_counter[0][1]) / self.total_pixels)
        if self.percentage_of_first > 0.5:
            return list(self.number_counter[0][0])  # Tuple yerine liste olarak döndür
        else:
            return self.average_colour()

def get_background_color(image):
    detector = BackgroundColorDetector(image)
    return detector.detect_background_color()

if __name__ == "__main__":
    if len(sys.argv) != 2:  # Checks if image was given as cli argument
        print("error: syntax is 'python main.py /example/image/location.jpg'")
    else:
        # Verilen image path'ini yükleyin
        image = cv2.imread(sys.argv[1], 1)
        background_color = get_background_color(image)
        print("Background color is: ", background_color)
