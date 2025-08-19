import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def make_qr_code(short_link: str) -> ContentFile:
    """
    Generate a QR code image for the given URL string and return
    a ContentFile ready to save to a Django FileField.
    """
    # 1. Create the QR code image
    img = qrcode.make(short_link)

    # 2. Dump it into an in-memory buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # 3. Derive a filename from the URL slug
    slug = short_link.rstrip("/").rsplit("/", 1)[-1]
    filename = f"qr_{slug}.png"

    # 4. Wrap the bytes in a Django ContentFile and return it
    return ContentFile(buffer.read(), name=filename)
