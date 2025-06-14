import argparse
import qrcode
from PIL import Image, ImageDraw, ImageFont

def create_vcard_qr(name, phone, email, org=None, title=None, website=None, logo_path=None, output_file=None):
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL;TYPE=CELL:{phone}
EMAIL:{email}"""
    
    if org:
        vcard += f"\nORG:{org}"
    if title:
        vcard += f"\nTITLE:{title}"
    if website:
        vcard += f"\nURL:{website}"

    vcard += "\nEND:VCARD"

    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Load and resize the logo
    if logo_path is not None:
        logo = Image.open(logo_path)
        qr_width = qr_img.width
        qr_height = qr_img.height
        logo_size = int(qr_width * 0.2)  # Logo covers 20% of QR width
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # Compute position and paste the logo
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

    # Prepare text
    text_lines = [name, title, org]
    font_size = 48
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default(font_size)

    text_padding = 8
    line_spacing = 10

    # Measure max width and total height
    dummy_img = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(dummy_img)
    text_height = 0
    max_line_width = 0

    for line in text_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        text_height += line_height + line_spacing
        max_line_width = max(max_line_width, line_width)
    text_height += text_padding * 2
    total_height = qr_height + text_height
    canvas_width = max(qr_width, max_line_width + text_padding * 2)

    # Create canvas
    canvas = Image.new("RGB", (canvas_width, total_height), "white")
    canvas.paste(qr_img, ((canvas_width - qr_width) // 2, 0))

    # Draw text
    draw = ImageDraw.Draw(canvas)
    y = qr_height + text_padding
    for i, line in enumerate(text_lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (qr_width - line_width) // 2
        y = (qr_height + text_padding + (i * font_size))
        draw.text((x, y), line, font=font, fill="black")

    # Save output
    canvas.save(output_file)
    print(f"QR code saved to {output_file}")

def main():

    # Parse the command line options.
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, action="store", default=None, help="The name for the card.", required=True)
    parser.add_argument("--phone", type=str, action="store", default=None, help="The phone number for the card.", required=True)
    parser.add_argument("--email", type=str, action="store", default=None, help="The email address for the card.", required=True)
    parser.add_argument("--org", type=str, action="store", default=None, help="The organizational name for the card.", required=False)
    parser.add_argument("--title", type=str, action="store", default=None, help="The individual's title for the card.", required=False)
    parser.add_argument("--website", type=str, action="store", default=None, help="A website for the card.", required=False)
    parser.add_argument("--logo_path", type=str, action="store", default=None, help="The logo to paste in the middle of the image.", required=False)
    parser.add_argument("--output", type=str, action="store", default="vcard_qr.png", help="The output file.", required=False)

    try:
        args = parser.parse_args()
    except IOError as e:
        parser.error(e)
        sys.exit(1)

    create_vcard_qr(args.name, args.phone, args.email, org=args.org, title=args.title, website=args.website, logo_path=args.logo_path, output_file=args.output)

if __name__=="__main__":
	main()
