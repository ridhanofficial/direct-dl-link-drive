import io
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from urllib.parse import urlparse, unquote

# ANSI escape codes for bold text
BOLD = '\033[1m'
END = '\033[0m'

# Authenticate and create the PyDrive client
def authenticate_drive():
    gauth = GoogleAuth()
    try:
        gauth.LoadCredentialsFile("my_credentials.json")
    except:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile("my_credentials.json")
    return GoogleDrive(gauth)

# Find or create the "Uploader" folder in Google Drive
def get_or_create_uploader_folder(drive):
    file_list = drive.ListFile({'q': "title='Uploader' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    if file_list:
        return file_list[0]['id']  # Folder already exists
    else:
        folder_metadata = {
            'title': 'Uploader',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder['id']

# Upload a file to Google Drive from in-memory
def upload_file_in_memory(file_stream, file_name, destination_folder_id):
    drive = authenticate_drive()
    file_drive = drive.CreateFile({'title': file_name, 'parents': [{'id': destination_folder_id}]})
    file_drive.Upload(file_stream)
    print(f"File '{file_name}' uploaded successfully to 'Uploader' folder!")

def download_file_to_memory(url):
    """Download file directly to memory."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return None

def format_file_size(size):
    """Helper function to format file size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

try:
    while True:
        try:
            print(f"{BOLD}\n\n\nWelcome to the In-Memory Video Downloader 🙏🏻 \n\n{END}")
            print("Type 'exit' to quit the program.\n")
            user_input = input("Enter the download link 🔗: ").strip()
        except KeyboardInterrupt:
            print(f"{BOLD}\nKeyboard interrupt detected. Exiting the program.{END}")
            break

        if user_input.lower() == 'exit':
            print(f"{BOLD}Exiting the program.{END}")
            break

        try:
            response = requests.head(user_input, allow_redirects=True)
            response.raise_for_status()
        except requests.exceptions.MissingSchema:
            print(f"{BOLD}Invalid URL. Please enter a valid download link.\n{END}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"{BOLD}Error fetching the URL: {e}. Please try again.\n{END}")
            continue

        file_size = int(response.headers.get('content-length', 0))
        file_size_str = format_file_size(file_size)

        parsed_url = urlparse(user_input)
        file_name = unquote(os.path.basename(parsed_url.path))

        print(f"{BOLD}\nThe file '{file_name}' is {file_size_str} in size.{END}")

        start_time = time.time()

        # Download file to memory
        file_stream = download_file_to_memory(user_input)

        if file_stream is None:
            print(f"{BOLD}Failed to download the file.{END}")
            continue

        end_time = time.time()
        total_time = end_time - start_time

        print()
        print(f"{BOLD}File name:{END} {file_name}")
        print(f"{BOLD}File size:{END} {file_size_str}")
        print(f"{BOLD}Total Time:{END} {total_time:.2f} seconds")

        # Upload the file to Google Drive
        drive = authenticate_drive()
        uploader_folder_id = get_or_create_uploader_folder(drive)
        upload_file_in_memory(file_stream, file_name, uploader_folder_id)

except Exception as e:
    print(f"{BOLD}An unexpected error occurred:{END} {str(e)}")
    print(f"{BOLD}Exiting the program.{END}")
