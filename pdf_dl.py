import os, sys
from fileinput import filename

import requests
import threading
from queue import Queue
from urllib.parse import urlparse
from tqdm import tqdm


def download_pdfs_threaded(urls, num_threads=16, timeout=30):
    """
    Download PDF files from multiple URLs concurrently using threading.
    Shows progress with tqdm progress bar.

    Parameters:
        urls (list): List of URLs pointing to PDF files
        output_dir (str): Directory to save downloaded files
        num_threads (int): Number of concurrent download threads
        timeout (int): Request timeout in seconds

    Returns:
        tuple: (successful_downloads, failed_downloads)
    """

    # Track successful and failed downloads
    successful = []
    failed = []
    lock = threading.Lock()  # For thread-safe list operations

    # Create a queue to hold all the URLs
    url_queue = Queue()
    for url in urls:
        url_queue.put(url)

    total_urls = len(urls)

    # Create a progress bar
    progress_bar = tqdm(total=total_urls, unit="file")

    def download_worker():
        while not url_queue.empty():
            # Get URL from queue
            url = url_queue.get()

            try:
                # Generate filename from URL or use a default pattern
                filename = os.path.basename(urlparse(url).path)
                if not filename.endswith('.pdf'):
                    filename = f"{filename}.pdf" if filename else f"document_{hash(url)}.pdf"

                filepath = filename

                # Download the file
                response = requests.get(url, stream=True, timeout=timeout)
                response.raise_for_status()  # Raise exception for HTTP errors

                # Check if it's actually a PDF
                content_type = response.headers.get('Content-Type', '').lower()
                if 'application/pdf' not in content_type and not url.lower().endswith(
                        '.pdf'):
                    print(f"URL does not point to a PDF file: {content_type}")
                    raise ValueError(
                        f"URL does not point to a PDF file: {content_type}")

                # Save the file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Record success
                with lock:
                    successful.append((url, filepath))

            except Exception as e:
                # Record failure
                with lock:
                    failed.append((url, str(e)))

            # Update progress bar
            with lock:
                progress_bar.update(1)

            # Mark task as done
            url_queue.task_done()

    # Create and start worker threads
    threads = []
    for _ in range(min(num_threads, total_urls)):
        thread = threading.Thread(target=download_worker, daemon=True)
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Close the progress bar
    progress_bar.close()

    print( f"Download complete. Success: {len(successful)}, Failed: {len(failed)}")
    return successful, failed


# Example usage
if __name__ == "__main__":
    # Example list of URLs
    with open(sys.argv[1]) as f:
        pdf_urls = [x.strip() for x in f.readlines()]

        successful, failed = download_pdfs_threaded(pdf_urls, num_threads=16)

        # Optionally, save failed URLs to retry later
        if failed:
            with open("failed_downloads.txt", "w") as f:
                for url, error in failed:
                    f.write(f"{url} | Error: {error}\n")