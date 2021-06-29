import httpx
import numpy as np
from PIL import ImageGrab
import cv2
import colorsys


def mostFrequent(List):
    counter = 0
    num = List[0] 

    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 

    return num 

def make_request(hue, sat, bri):
    data = '{"numberOfLights": 1,"lights": [{"on": 1,"hue":' + f'{float(hue)},"saturation":' + f'{float(sat)},"brightness":' + f'{float(bri)},"temperature": 0' + '}]}'
    httpx.put("http://10.0.0.43:9123/elgato/lights", data=data)


step = 25
num_pixel = 1080//step * 1920//step
count = 0
while True:
    img = ImageGrab.grab()
    imgNP = np.array(img)

    im_arr = np.frombuffer(img.tobytes(), dtype=np.uint8)
    im_arr = im_arr.reshape((img.size[1], img.size[0], 3))
    r = g = b = 0
    pixelArray = []
    for y in range(0, 1080, step):
        for x in range(0, 1920, step):
            px = im_arr[y][x]
            
            pixelArray.append([px[0], px[1], px[2]])

    mostFrequentColor = mostFrequent(pixelArray)
    # hue = 0.0
    red, green, blue = mostFrequentColor[2], mostFrequentColor[1], mostFrequentColor[0]
    # max_index = mostFrequentColor.index(max(mostFrequentColor))
    # min_index = mostFrequentColor.index(min(mostFrequentColor))
    # if max_index == 0:
    #     hue = (green - blue) * (max(mostFrequentColor) - min(mostFrequentColor))
    # elif max_index == 1:
    #     hue = 2.0 + (blue - red) / (max(mostFrequentColor) - min(mostFrequentColor))
    # elif max_index == 2:
    #     hue = 4.0 + (red - green) / (max(mostFrequentColor) - min(mostFrequentColor))
    # # hue = hue * 60
    # if hue < 0:
    #     hue += 360
    red, green, blue = [x / 255.0 for x in mostFrequentColor]
    hue, bri, sat = colorsys.rgb_to_hls(red, green, blue)
    # bri = (max(mostFrequentColor) + min(mostFrequentColor)) / 2
    # delta = (max(mostFrequentColor) - min(mostFrequentColor))
    # sat = (delta) / (max(mostFrequentColor) + min(mostFrequentColor)) * 100
    # (1 - (abs(2*bri - 1)))
    print(mostFrequentColor, hue*100, bri*100, sat*100)
    make_request(hue*100, sat*100, bri*100)
    count += 1

    # print(count)


r = httpx.get("http://10.0.0.43:9123/elgato/lights")
print(r.status_code)
print(r.json())

