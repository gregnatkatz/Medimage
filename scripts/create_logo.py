from PIL import Image, ImageDraw, ImageFont
import os

def create_azure_ai_logo():
    """Create a Microsoft/Azure AI themed logo"""
    img = Image.new('RGBA', (800, 200), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    for i in range(200):
        alpha = int(200 - i)
        draw.rectangle([(0, i), (800, i+1)], fill=(0, 120, 212, alpha))
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    text = "Azure AI Medical"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (800 - text_width) / 2
    y = (200 - text_height) / 2
    
    draw.text((x+2, y+2), text, fill=(0, 0, 0, 100), font=font)
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    output_dir = '/home/ubuntu/medical-ai-demo/frontend/public'
    os.makedirs(output_dir, exist_ok=True)
    img.save(os.path.join(output_dir, 'logo.png'))
    print(f"Logo created at {os.path.join(output_dir, 'logo.png')}")

if __name__ == "__main__":
    create_azure_ai_logo()
