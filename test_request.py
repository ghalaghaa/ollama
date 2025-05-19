import requests

url = "http://127.0.0.1:5050/analyze"  # أو استخدمي 192.168... إذا بتجربين من جوال

payload = {
    "text": "أشعر بالحزن ولكن أحاول أن أكون إيجابيًا. مررت بيوم صعب لكنه انتهى بلحظة جميلة.",
    "health": "- عدد ساعات النوم: 6\n- عدد ساعات التعرض للشمس: 2.5\n- الحالة المزاجية: متقلبة"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("✅ الرد من الخادم:")
    data = response.json()
    print(data["analysis"])
else:
    print("❌ خطأ:")
    print(response.text)