import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\aravi\Documents\tesseract.exe"

# Replace with an image path from your PDF if possible
image_path = r"C:\Users\aravi\Documents_Local\Documents\health_chatbot\backend\sample_image.png"
text = pytesseract.image_to_string(Image.open(image_path))

print("🧠 OCR Output:\n", text)
