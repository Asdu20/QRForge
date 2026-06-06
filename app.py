from flask import Flask, render_template, request
import qrcode
import os
from PIL import Image

app = Flask(__name__)

QR_FOLDER = "static/qr_codes"
LOGO_FOLDER = "static/uploads"

os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs(LOGO_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():

    qr_file = None

    if request.method == "POST":

        data = request.form["data"]
        qr_color = request.form["qr_color"]

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=qr_color,
            back_color="white"
        ).convert("RGB")

        logo = request.files.get("logo")

        if logo and logo.filename:

            logo_path = os.path.join(
                LOGO_FOLDER,
                logo.filename
            )

            logo.save(logo_path)

            logo_img = Image.open(
                logo_path
            ).convert("RGBA")

            qr_width, qr_height = img.size

            logo_size = qr_width // 5

            logo_img = logo_img.resize(
                (logo_size, logo_size)
            )

            pos = (
                (qr_width - logo_size) // 2,
                (qr_height - logo_size) // 2
            )

            img = img.convert("RGBA")

            img.paste(
                logo_img,
                pos,
                logo_img
            )

        qr_file = "generated_qr.png"

        img.save(
            os.path.join(
                QR_FOLDER,
                qr_file
            )
        )

    return render_template(
        "index.html",
        qr_file=qr_file
    )

if __name__ == "__main__":
    app.run(debug=True)