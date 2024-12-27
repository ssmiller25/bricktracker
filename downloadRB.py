import requests
import gzip
import shutil
import os
import sys
from urllib.parse import urlparse

def get_nil_images():
    image_urls = [
        "https://rebrickable.com/static/img/nil_mf.jpg",
        "https://rebrickable.com/static/img/nil.png",
        "https://docs.google.com/spreadsheets/d/1rlYfEXtNKxUOZt2Mfv0H17DvK7bj6Pe0CuYwq6ay8WA/gviz/tq?tqx=out:csv&sheet=Sorted%20by%20Retirement"
    ]
    static_folder = "static"
    
    # Create the static folder if it does not exist
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    for url in image_urls:
        # Extract the output filename from the URL
        parsed_url = urlparse(url)
        output_file = os.path.join(static_folder, os.path.basename(parsed_url.path))

        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for any request errors

        # Save the image to the static folder
        with open(output_file, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded {output_file}")

def get_retired_sets():

    urls = [
        "https://docs.google.com/spreadsheets/d/1rlYfEXtNKxUOZt2Mfv0H17DvK7bj6Pe0CuYwq6ay8WA/gviz/tq?tqx=out:csv&sheet=Sorted%20by%20Retirement%20Date"
    ]
    
    for url in urls:
        # Extract the output filename from the URL
        parsed_url = urlparse(url)
        output_file = os.path.basename(parsed_url.path)

        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for any request errors

        # Save the image to the static folder
        with open('retired_sets.csv', 'wb') as f:
            f.write(response.content)

        print(f"Downloaded {output_file}")


def download_and_unzip(url: str):
    # Extract the output filename from the URL
    parsed_url = urlparse(url)
    output_file = os.path.basename(parsed_url.path).replace('.gz', '')

    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Check for any request errors

    # Write the gzipped file to the local file system
    gz_file = output_file + '.gz'
    with open(gz_file, 'wb') as f:
        f.write(response.content)

    # Unzip the file
    with gzip.open(gz_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Optionally remove the .gz file after extraction
    os.remove(gz_file)

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 downloadRB.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    download_and_unzip(url)

