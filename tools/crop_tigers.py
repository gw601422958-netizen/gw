#!/usr/bin/env python3
"""从团队合影中裁剪 5 位男生的头像区域。"""
from PIL import Image
from pathlib import Path

src = Path("/Users/guanwu/Desktop/Shanyangwuhu/images/team.jpg")
out_dir = Path("/Users/guanwu/Desktop/Shanyangwuhu/images")

img = Image.open(src)
W, H = img.size
print(f"原图: {W}x{H}")

# 7 段均匀分布，5 男对应段 2/3/4/5/6 中心
# 虎4 左偏 1/4 + 1/5 = 37 + 30 = 67
# 虎5 累加左偏 2 个 1/4（150/4 × 2 = 75）
male_centers = [137, 229, 320, 411 - 67, 503 - 75]

# 头部 y 范围（头顶到下巴+脖子）约 250-405，155 像素高
# 整体中心下移 1/4 头像宽度（150/4 = 37.5）→ y_top 从 250 升到 288
crop_size = 150
positions = [
    (137, 280),  # 虎1
    (229, 280),  # 虎2
    (320 - 20, 280),  # 虎3 中心左移 20
    (344 + 20, 280),  # 虎4 中心右移 20
    (428, 280),  # 虎5
]

for i, (cx, yt) in enumerate(positions, start=1):
    half = crop_size // 2
    box = (cx - half, yt, cx + half, yt + crop_size)
    cropped = img.crop(box)
    # resize 到 240x240，保留锐度
    resized = cropped.resize((240, 240), Image.LANCZOS)
    out_path = out_dir / f"tiger-{i}.jpg"
    resized.save(out_path, "JPEG", quality=92)
    print(f"虎{i}: {box} -> {out_path.name} ({out_path.stat().st_size // 1024}KB)")