import qrcode
import io
from django.core.files.base import ContentFile
from PIL import Image, ImageFilter, ImageDraw, ImageFont


def create_qrcode_image(image, url):
    base_image = Image.open(image)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image = qr_image.convert('RGBA')
    background = Image.new('RGBA', (qr_image.size[0], qr_image.size[1] + 50), 'white')
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('fonts/roboto/Roboto-Medium.ttf', 25)
    _, _, w, h = draw.textbbox((0, 0), "Scan QR code for details", font=font)
    draw.text(
        (int((qr_image.size[0] - w) / 2), 20),
        "Scan QR code for details",
        'black',
        font=font
    )
    background.paste(qr_image, (0, 50))
    base_image = base_image.filter(ImageFilter.GaussianBlur(15))
    x = int((base_image.size[0] - qr_image.size[0]) / 2)
    y = int((base_image.size[1] - qr_image.size[1]) / 2)
    base_image.paste(background, (x, y), background)
    buffer = io.BytesIO()
    base_image.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())
