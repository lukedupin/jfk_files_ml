import torch, sys
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from pdf_to_img import pdf_to_png_bytes

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base", torch_dtype=torch.float16).to("cuda")

#img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
#raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

for img in pdf_to_png_bytes(sys.argv[1]):
    raw_image = Image.open(img).convert('RGB')

    # conditional image captioning
    #text = "a photography of"
    #inputs = processor(raw_image, text, return_tensors="pt").to("cuda", torch.float16)
    #out = model.generate(**inputs)
    #print(processor.decode(out[0], skip_special_tokens=True))

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt").to("cuda", torch.float16)
    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True))
