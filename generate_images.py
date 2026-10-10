from PIL import Image, ImageDraw, ImageFont

# 1. إنشاء صورة الشعار التعريفي (Intro Preview Image) - 400x400 بكسل
img_icon = Image.new("RGB", (400, 400), color=(30, 60, 114)) # لون خلفية متناسق مع هوية المنصة
draw_icon = ImageDraw.Draw(img_icon)
draw_icon.rectangle([20, 20, 380, 380], outline=(241, 196, 15), width=6)

# إضافة نص توضيحي للشعار
try:
    font = ImageFont.truetype("arial.ttf", 40)
except IOError:
    font = ImageFont.load_default()

draw_icon.text((120, 170), "OMNIVERSE", fill=(255, 255, 255), font=font)
img_icon.save("intro_icon_400x400.png")

# 2. إنشاء صورة لقطة الشاشة (Previews) - 750x1500 بكسل
img_preview = Image.new("RGB", (750, 1500), color=(247, 249, 252))
draw_preview = ImageDraw.Draw(img_preview)
draw_preview.rectangle([40, 40, 710, 1460], outline=(41, 128, 185), width=4)

draw_preview.text((220, 700), "Omniverse Hub\nSmart City Platform", fill=(44, 62, 80), font=font)
img_preview.save("preview_750x1500.png")

print("تم إنشاء صور المقاسات المطلوبة بنجاح وحفظها في مجلد المشروع.")