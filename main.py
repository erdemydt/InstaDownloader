import instaloader
import datetime
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


username = ""
def download_images(username, start_date, end_date):
    L = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' not found.")
        return

    for post in profile.get_posts():
        if start_date <= post.date <= end_date:
            L.download_post(post, target=profile.username)

if __name__ == "__main__":
    username = "username"  # Replace with the target Instagram username
    start_date = datetime.datetime(2023, 10, 28)  # Replace with your desired start date
    end_date = datetime.datetime(2023, 10, 30)  # Replace with your desired end date

    download_images(username, start_date, end_date)



def resize_and_convert_to_pdf(input_folder, output_pdf):
    image_files = [file for file in os.listdir(input_folder) if file.lower().endswith(".jpg")]

    if not image_files:
        print(f"No JPG files found in {input_folder}.")
        return

    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    pdf.setTitle("JPG to PDF")

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        img = Image.open(image_path)

        # Resize the image to fit the PDF page while preserving the aspect ratio
        img.thumbnail(letter)

        img_width, img_height = img.size
        pdf.drawImage(image_path, 0, 0, width=img_width, height=img_height)
        pdf.showPage()

    pdf.save()
    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    input_folder = "/" + username  # Replace with the path to your folder containing JPG files
    output_pdf = "output.pdf"  # Replace with the desired output PDF file name

    resize_and_convert_to_pdf(input_folder, output_pdf)