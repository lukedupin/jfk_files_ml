from transformers import AutoProcessor, AutoModelForImageTextToText

import requests
import torch, sys, json, os
from PIL import Image
from tqdm import tqdm


from list_dir import list_pdf_files
from pdf_to_img import pdf_to_png_bytes

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForImageTextToText.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf", device_map=device)
processor = AutoProcessor.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf")

while True:
    response = requests.get(sys.argv[1])
    if response.status_code != 200:
        print(f"Completed the run: {response.status_code}")
        break

    data = response.json()
    pdf_file = data['filename']

    #Remove the .pdf and swap with .txt
    txt_file = f'{sys.argv[2]}/{pdf_file.replace(".pdf", ".txt")}'
    with open(txt_file, "w") as f:
        print()
        print(f"Processing {txt_file}")
        print()
        pdf_pages = pdf_to_png_bytes( pdf_file )
        for img in tqdm(pdf_pages):
            raw_image = Image.open(img).convert('RGB')
            inputs = processor(raw_image, return_tensors="pt").to(device)

            generate_ids = model.generate(
                **inputs,
                do_sample=False,
                tokenizer=processor.tokenizer,
                stop_strings="<|im_end|>",
                max_new_tokens=4096,
            )

            f.write(processor.decode(generate_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True))
            f.write('\n\n\n')