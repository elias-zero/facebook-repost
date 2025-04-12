import json
import os
import requests
from datetime import datetime

# --- إعداد المتغيرات البيئية ---
PAGE_ID = os.environ.get("PAGE_ID")
ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

if not PAGE_ID or not ACCESS_TOKEN:
    raise Exception("يجب تعيين PAGE_ID و PAGE_ACCESS_TOKEN في متغيرات البيئة")

# --- تحميل بيانات الكوبونات ---
with open('coupons.json', 'r', encoding='utf-8') as f:
    coupons = json.load(f)

# --- حساب اليوم في الشهر ---
today = datetime.now()
day_of_month = today.day
start_index = (day_of_month - 1) * 16
end_index = start_index + 16

if start_index >= len(coupons):
    start_index = 0
    end_index = 16

today_coupons = coupons[start_index:end_index]

# --- وظيفة النشر مع رفع الصورة ---
def post_on_facebook(message, image_url=None):
    if image_url:
        # رفع الصورة مباشرة إلى فيسبوك باستخدام الرابط
        post_url = f"https://graph.facebook.com/{PAGE_ID}/photos"
        payload = {
            "url": image_url,
            "message": message,
            "access_token": ACCESS_TOKEN
        }
    else:
        # نشر منشور نصي عادي
        post_url = f"https://graph.facebook.com/{PAGE_ID}/feed"
        payload = {
            "message": message,
            "access_token": ACCESS_TOKEN
        }
    
    response = requests.post(post_url, data=payload)
    if response.status_code == 200:
        print("تم النشر بنجاح!")
        print("الرسالة:", message)
        if image_url:
            print("الصورة:", image_url)
    else:
        print("خطأ في النشر:", response.text)

# --- نشر الكوبونات ---
for coupon in today_coupons:
    message = (
        f"{coupon['coupon_title']}\n"
        f"{coupon['coupon_description']}\n"
        f"للحصول على الكوبون اضغط: {coupon['url']}"
    )
    post_on_facebook(message, coupon.get("image_url"))
