# Google Drive Downloader

A python scripts that uses Google Drive API to download folders or files.

## Installation 
1. Git clone this repo:
```
git clone https://github.com/Techyhans/google-api-scraping.git
```
2. Create an Python 3.8.5 (or higher) environment:
```
conda create -n gdrive-api python=3.8.5
conda activate gdrive-api
```
3. Install required dependencies:
```
pip install -r requirements.txt
```

## Download using Google Drive API
You may state two arguments to run the `download.py`.
- '-i' or '--id': One or more files or folders ID you would like to download (Must be given)
- '-n' or '--name': One or more folder names you would like to search and download in given parent folder ID (Optional)."

For example:
### CASE 1: Download folders or files with their ID
- To download a folder with all items it contains, specifying its ID as below:
```
python download.py -i 1ZyjCpwSb9EtkWYnWB6k_PerulHhBxkRA
```
- To download multiple folders:
```
python download.py -i 1ZyjCpwSb9EtkWYnWB6k_PerulHhBxkRA 1ZbWtRi1HqqzPzD8ldyE52LympemQ15Ze
```
- If you want to download a file only. Also, you only have to provide the ID.
```
python download.py -i 16Cyd8JMnO-U_t0hj2rFsitFRz07smIpk
```
### CASE 2: Download specifically named folders with the given parent folder ID
- To search folder with folder name `folder_1` under the parent folder with given ID:
```
python download.py -i 1ZyjCpwSb9EtkWYnWB6k_PerulHhBxkRA -n folder_1
```
This would only download the `folder_1` folder with all its content. You may specific multiple IDs and names.
