from transformers import AutoProcessor, AutoModelForImageTextToText
import torch, sys, json, os
from PIL import Image
from tqdm import tqdm


from list_dir import list_pdf_files
from pdf_to_img import pdf_to_png_bytes

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForImageTextToText.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf", device_map=device)
processor = AutoProcessor.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf")

files = []
for line in sys.stdin.readlines():
    if line.startswith("#"):
        continue
    idx, filepath = json.loads(line.strip())
    if idx == int(sys.argv[1]):
        files.append(filepath)

if len(sys.argv) >= 3 and sys.argv[2] == "reverse":
    print("Reversing order of files")
    files = files[::-1]

#image = "https://huggingface.co/datasets/hf-internal-testing/fixtures_got_ocr/resolve/main/image_ocr.jpg"
for pdf_file in tqdm(files):
    #Remove the .pdf and swap with .txt
    txt_file = pdf_file.replace(".pdf", ".txt")
    # If the file exists, skip it
    if os.path.exists(txt_file):
        continue

    with open(txt_file, "w") as f:
        print()
        print(f"Processing {pdf_file}")
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