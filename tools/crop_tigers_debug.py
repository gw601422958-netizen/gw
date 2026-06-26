#!/usr/bin/env python3
"""调试：把 7 段全部裁出来，确认每个男生的实际位置。"""
from PIL import Image, ImageDraw
from pathlib import Path

src = Path("/Users/guanwu/Desktop/Shanyangwuhu/images/team.jpg")
debug_dir = Path("/tmp/tiger-debug")
debug_dir.mkdir(exist_ok=True)

img = Image.open(src).convert("RGB")
W, H = img.size

# 在原图上画 7 等分参考线 + 标号
annotated = img.copy()
draw = ImageDraw.Draw(annotated)
seg = W // 7
for i in range(1, 7):
    x = i * seg
    draw.line([(x, 0), (x, H)], fill="red", width=2)
for i in range(7):
    cx = i * seg + seg // 2
    draw.text((cx - 10, 20), str(i + 1), fill="yellow")
annotated.save(debug_dir / "annotated.jpg", "JPEG", quality=85)
print(f"参考线已画到 {debug_dir / 'annotated.jpg'}")

# 7 段都裁出来（y 范围宽一些）
crop_w = 130
y0, y1 = 260, 410
for i in range(7):
    cx = i * seg + seg // 2
    half = crop_w // 2
    box = (cx - half, y0, cx + half, y1)
    img.crop(box).resize((240, 240), Image.LANCZOS).save(
        debug_dir / f"person-{i + 1}.jpg", "JPEG", quality=92
    )
print(f"7 段头像已存到 {debug_dir}/")