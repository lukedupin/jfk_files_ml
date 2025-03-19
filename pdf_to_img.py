import io
from pdf2image import convert_from_path


def pdf_to_png_bytes(pdf_path, dpi=300) -> list[io.BytesIO]:
    """
    Convert a PDF file to PNG images and return them as bytes objects.
    
    Parameters:
        pdf_path (str): Path to the PDF file
        dpi (int, optional): Resolution in dots per inch
        
    Returns:
        list: List of bytes objects containing PNG image data
    """
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi)
    
    # Convert each image to PNG bytes
    png_bytes_list = []
    for i, image in enumerate(images):
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)  # Move to the beginning of BytesIO object
        png_bytes_list.append(img_byte_arr)
    
    print(f"Converted {len(images)} pages to PNG bytes objects")
    return png_bytes_list

# Example usage
if __name__ == "__main__":
    # Get the bytes objects
    png_bytes = pdf_to_png_bytes("example.pdf")
    
    # Example: Save the first page to a file
    with open("page_1.png", "wb") as f:
        f.write(png_bytes[0].getvalue())
    
    # Example: Use the bytes directly (e.g., for web response)
    # response.content = png_bytes[0].getvalue()
