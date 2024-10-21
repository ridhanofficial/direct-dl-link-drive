# Direct DL Link To Google Drive Uploader

A Python-based tool that allows users to download files directly to their Google Drive using the `aria2` download manager for accelerated downloading. The tool offers features like a progress bar, file renaming, and the ability to cancel the download mid-process.

## Features

- **Accelerated Downloads:** Uses `aria2c` with up to 16 connections for faster file downloads.
- **Download Progress:** Displays a progress bar for the download process using `tqdm`.
- **Cancelable Downloads:** Users can cancel the download at any time, and incomplete files will be removed automatically.
- **File Renaming:** Allows users to rename the downloaded file before saving it.
- **Google Drive Integration:** Files are downloaded directly into your Google Drive, which is automatically mounted.

## Requirements

- Google Colab (for easy integration with Google Drive)
- `aria2` (installed via `apt-get`)
- Python Libraries:
  - `os`
  - `urllib.parse`
  - `requests`
  - `subprocess`
  - `threading`
  - `time`
  - `tqdm`

## Installation

1. **Set up Google Colab:**
   Open the notebook in Google Colab and ensure that your Google Drive is mounted.

2. **Install `aria2`:**
   Run the following command to install `aria2`:
   ```bash
   !apt-get install -y aria2

3. **Mount Google Drive**
   Mount Google Drive to store the downloaded files. The script automatically mounts Google Drive, but here is the command for reference:
   ```python
from google.colab import drive
drive.mount('/content/drive')

   
