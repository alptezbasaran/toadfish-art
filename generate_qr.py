import qrcode
import qrcode.image.svg

factory = qrcode.image.svg.SvgPathImage
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=12,
    border=0,
)
qr.add_data('https://alptezbasaran.github.io/toadfish-art/')
qr.make(fit=True)
img = qr.make_image(image_factory=factory)
img.save('/app/assets/qr.svg')
print("QR code saved to assets/qr.svg")
