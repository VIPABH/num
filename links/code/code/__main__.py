import os

# اسم الملف لتخزين النقاط
POINTS_FILE = "points.txt"

# دالة لجلب النقاط المحفوظة من الملف
def get_points():
    if os.path.exists(POINTS_FILE):
        with open(POINTS_FILE, "r") as file:
            content = file.read().strip()
            return int(content) if content.isdigit() else 0
    return 0

# دالة لحفظ النقاط في الملف
def save_points(points):
    with open(POINTS_FILE, "w") as file:
        file.write(str(points))

# دالة لزيادة النقاط عند الفوز
def add_win():
    points = get_points()  # جلب النقاط الحالية
    points += 1  # زيادة نقطة واحدة عند الفوز
    save_points(points)  # حفظ النقاط الجديدة
    print(f"🎉 تهانينا! لديك الآن {points} نقاط.")

# دالة لعرض النقاط الحالية
def show_points():
    points = get_points()
    print(f"📊 عدد النقاط الحالية: {points}")

# تجربة الكود
if __name__ == "__main__":
    while True:
        choice = input("اختر: [1] فوز 🎯 | [2] عرض النقاط 📊 | [3] خروج ❌\n")
        if choice == "1":
            add_win()
        elif choice == "2":
            show_points()
        elif choice == "3":
            print("👋 إلى اللقاء!")
            break
        else:
            print("❌ خيار غير صحيح، حاول مرة أخرى.")
