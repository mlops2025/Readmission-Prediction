"""
Function to download and ingest the data file
"""
import os
import requests

DEFAULT_FILE_URL = "https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip"

def ingest_data(file_url=DEFAULT_FILE_URL):
    """
    Function to download file from URL
    Args:
        file_url: URL of the file, A default is used if not specified
    Returns:
        zipfile_path: The zipped file path to the data
    """
    # Send an HTTP GET request to the URL
    response = requests.get(file_url, timeout=30)

    print("Downloading Data")

    # Set the root directory variable using a relative path
    root_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    print(f"Root directory: {root_dir}")

    # Path to store the zipfile
    zipfile_path=os.path.join(root_dir, 'data','data.zip')
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save file to data
        with open(zipfile_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully. Zip file available under {zipfile_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

    return zipfile_path

if __name__ == "__main__":
    ZIPFILE_PATH = ingest_data("https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip")