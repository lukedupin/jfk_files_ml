from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import requests, sys

from pdf_to_img import pdf_to_png_bytes

# load image from the IAM database (actually this model is meant to be used on printed text)
for img in pdf_to_png_bytes(sys.argv[1]):
    image = Image.open(img).convert("RGB")

    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-printed')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-printed')
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    print( generated_text )

