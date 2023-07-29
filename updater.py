import os
from pathlib import Path
import requests

def download_from_github():
# GitHub repository and release tag
    repository = "yt-dlp/yt-dlp"
    release_tag = "latest"
    # GitHub API endpoint for releases
    url = f"https://api.github.com/repos/{repository}/releases/{release_tag}"
    # Send a GET request to the GitHub API
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        release_info = response.json()
        # Get the asset URL of the yt-dlp release
        for asset in release_info["assets"]:
            if asset["name"].endswith(".exe"):
                download_url = asset["browser_download_url"]
                break
        if download_url:
            # Path to save the downloaded executable
            output_path = Path("downloads")
            # Send a GET request to download the file
            response = requests.get(download_url)
            # Save the response content to a file
            with open(output_path, "wb") as f:
                f.write(response.content)
            print("yt-dlp downloaded successfully!")
        else:
            print("Unable to find the yt-dlp release asset.")
    else:
        print("Failed to retrieve release information from GitHub.")

def check_for_ytdlp():
    if Path("downloads/yt-dlp.exe").exists():
        print("Found yt-dlp.exe")
    else:
        download_from_github()

        

def update_ytdlp():
    # Path to save the downloaded executable
    output_path = Path("downloads")
    if Path("downloads/yt-dlp.exe").exists():
        os.remove(Path("downloads/yt-dlp.exe"))
    download_from_github()