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
# نفترض أن العدد الإجمالي للكوبونات هو 480 ومنشور اليوم يعتمد على 16 كوبون
# إذن المنشوارات للشهر: 16 منشور يومياً * 30 يومًا = 480 منشور (يمكن تعديل الحساب إذا كان الشهر مختلفاً)
start_index = (day_of_month - 1) * 16
end_index = start_index + 16

# إذا انتهت القائمة (أي في حالة انتهاء شهر كامل)، نعيد الدورة من البداية
if start_index >= len(coupons):
    start_index = 0
    end_index = 16

today_coupons = coupons[start_index:end_index]

# --- نشر المنشورات على صفحة فيسبوك ---
# وظيفة للنشر على فيسبوك باستخدام Graph API
def post_on_facebook(message, image_url=None):
    post_url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    # يمكنك التوسع لاضافة الصور بطريقة أخرى عبر خاصية attachments أو عن طريق تحميل الصورة أولاً
    if image_url:
        payload["link"] = image_url  # إما استخدام الرابط كمرفق أو تضمينه في الرسالة
    
    response = requests.post(post_url, data=payload)
    if response.status_code == 200:
        print("تم النشر بنجاح:", message)
    else:
        print("خطأ في النشر:", response.text)

# --- نشر كوبون كل مرة ---
for coupon in today_coupons:
    # تكوين رسالة المنشور
    message = f"{coupon['coupon_title']}\n{coupon['coupon_description']}\nللحصول على الكوبون اضغط: {coupon['url']}"
    post_on_facebook(message, image_url=coupon.get("image_url"))

