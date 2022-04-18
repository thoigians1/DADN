import requests
import time


def IOlisten():
    old_data = None 
    print("Start")
    while True:
        req = requests.get("https://io.adafruit.com/api/v2/duongthanhthuong/feeds/people/data/retain", 
            params={'X-AIO' : 'aio_Lwrn39sWCZsxUO5oi5AIwdBrHZa9'}
        )
        new_data = req.text.split(',')[0]
        if (new_data != old_data):
            print(new_data)
            old_data = new_data
            
        time.sleep(5)

IOlisten()
