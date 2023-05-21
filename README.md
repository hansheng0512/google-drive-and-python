# Google Drive Downloader

A python scripts that uses Google Drive API to download folders or files.
## Demo



![demo](https://github.com/egemengulpinar/google-drive-and-python/assets/71253469/a03edddc-1483-4afa-825d-07c653caeb78)

## Installation 
1. Git clone this repo:
```
git clone https://github.com/Techyhans/google-api-scraping.git
```
2. Create an Python 3.8.5 >= environment:
```
conda create -n gdrive-api python=3.10.9
conda activate gdrive-api
```
3. Install required dependencies:
```
pip install -r requirements.txt
```

## Get client_secret.json from Google API
Open [Google Console](https://console.cloud.google.com) and write **Google Drive API** to search bar. Click **Create Credentials / OAuth Client ID** then create your project. After download your *client_secretXXX.json* file and save it as "client_secret.json"

## Download using Google Drive API
You may state two arguments to run the `download.py`.
- '-l' or '--link': One or more files or folders sharable link you would like to download (Must be given)
- '-i' or '--id': One or more files or folders ID you would like to download (Must be given)
- '-n' or '--name': One or more folder names you would like to search and download in given parent folder ID (Optional)."

For example:
### CASE 1: Download folders or files with their sharable links
- To download a folder with all items it contains, specifying its sharable links as below:
```
python download.py -l https://drive.google.com/file/d/1ZKWjVjYAgjKbLYviQFCwT0HfuDwGweCq/view?usp=share_link
```

- To download multiple folders:
```
python download.py -i DRIVE_LINK1 DRIVE_LINK2 ...
```
- If you want to download a file only. Also, you only have to provide the ID.

### CASE 2: Download specifically named folders with the given parent folder sharable link
- To search folder with folder name `folder_1` under the parent folder with given ID:
```
python download.py -i DRIVE_LINK -n folder_1
```
This would only download the `folder_1` folder with all its content. You may specific multiple IDs and names.

## Authors

- [@hansheng0512](https://www.github.com/hansheng0512)
- [@egemengulpinar](https://www.github.com/egemengulpinar)

