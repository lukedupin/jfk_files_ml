import os

def list_pdf_files(directory_path):
    """
    Lists all PDF files in the specified directory.
    
    Parameters:
        directory_path (str): Path to the directory to search
        
    Returns:
        list: Array of paths to PDF files
    """
    pdf_files = []
    
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: The directory '{directory_path}' does not exist.")
        return pdf_files
    
    # Walk through the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Check if it's a file and has a .pdf extension
        if os.path.isfile(file_path) and filename.lower().endswith('.pdf'):
            pdf_files.append(file_path)
    
    print(f"Found {len(pdf_files)} PDF files in '{directory_path}'")
    return pdf_files

# Example usage
if __name__ == "__main__":
    # Replace with your directory path
    pdfs = list_pdf_files("/path/to/your/pdfs")
    
    # Print the list of PDFs
    for pdf in pdfs:
        print(pdf)
