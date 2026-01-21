from PIL import Image
import os

def convert(path):
    if os.path.exists(path):
        img = Image.open(path)
        img.save(path, 'PNG')
        print(f"✅ Converted {path} to real PNG")

# Paths to the icons
icon_path = 'mobile/assets/images/icon.png'
adaptive_path = 'mobile/assets/images/adaptive-icon.png'

convert(icon_path)
convert(adaptive_path)
