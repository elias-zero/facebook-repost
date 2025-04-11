import json
import os
import requests
from datetime import datetime

# إعدادات الصفحة
PAGE_ID = os.getenv("PAGE_ID")
ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

# تحميل بيانات الكوبونات
with open('coupons.json', 'r', encoding='utf-8') as f:
    coupons = json.load(f)

def get_next_index():
    try:
        with open('last_index.txt', 'r') as f:
            index = int(f.read())
    except:
        index = 0
    
    new_index = (index + 1) % len(coupons)
    with open('last_index.txt', 'w') as f:
        f.write(str(new_index))
    
    return index

def publish_post():
    index = get_next_index()
    coupon = coupons[index]
    
    message = f"{coupon['title']}\n{coupon['description']}\n{coupon['url']}"
    
    # نشر المنشور مع الصورة
    response = requests.post(
        f"https://graph.facebook.com/{PAGE_ID}/photos",
        params={
            "access_token": ACCESS_TOKEN,
            "url": coupon['image_url'],
            "message": message
        }
    )
    
    print(f"تم النشر: {response.json()}")

if __name__ == "__main__":
    publish_post()
