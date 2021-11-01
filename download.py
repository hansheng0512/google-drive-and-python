import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import io
import argparse
from apiclient.http import MediaIoBaseDownload


# To connect to googel drive api
# If modifying these scopes, delete the file token.pickle
CLIENT_SECRET_FILE = "client_secret.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Create a Google Drive API service
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep="-")
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f"token_{API_SERVICE_NAME}_{API_VERSION}.pickle"

    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, "wb") as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME.capitalize(), "service created successfully.\n")
        return service
    except Exception as e:
        print("Unable to connect.")
        print(e)
        return None


# Download files
def downloadfiles(dowid, dfilespath, folder=None):
    request = service.files().get_media(fileId=dowid)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    if folder:
        with io.open(folder + "/" + dfilespath, "wb") as f:
            fh.seek(0)
            f.write(fh.read())
    else:
        with io.open(dfilespath, "wb") as f:
            fh.seek(0)
            f.write(fh.read())


# List files in folder until all files are found
def listfolders(filid, des):
    page_token = None
    while True:
        results = (
            service.files()
            .list(
                pageSize=1000,
                q="'" + filid + "'" + " in parents",
                fields="nextPageToken, files(id, name, mimeType)",
            )
            .execute()
        )
        page_token = results.get("nextPageToken", None)
        if page_token is None:
            folder = results.get("files", [])
            for item in folder:
                if str(item["mimeType"]) == str("application/vnd.google-apps.folder"):
                    if not os.path.isdir(des + "/" + item["name"]):
                        os.mkdir(path=des + "/" + item["name"])
                    listfolders(item["id"], des + "/" + item["name"])
                else:
                    downloadfiles(item["id"], item["name"], des)
                    print(item["name"])
        break
    return folder


# Download folders with files
def downloadfolders(folder_ids):
    for folder_id in folder_ids:
        folder = service.files().get(fileId=folder_id).execute()
        folder_name = folder.get("name")
        page_token = None
        while True:
            results = (
                service.files()
                .list(
                    q=f"'{folder_id}' in parents",
                    spaces="drive",
                    fields="nextPageToken, files(id, name, mimeType)",
                )
                .execute()
            )
            page_token = results.get("nextPageToken", None)
            if page_token is None:
                items = results.get("files", [])
                if not items:
                    # download files
                    downloadfiles(folder_id, folder_name) 
                    print(folder_name)
                else:
                    # download folders
                    print(f"Start downloading folder '{folder_name}'.")
                    for item in items:
                        if item["mimeType"] == "application/vnd.google-apps.folder":
                            if not os.path.isdir(folder_name):
                                os.mkdir(folder_name)
                            bfolderpath = os.path.join(os.getcwd(), folder_name)
                            if not os.path.isdir(
                                os.path.join(bfolderpath, item["name"])
                            ):
                                os.mkdir(os.path.join(bfolderpath, item["name"]))

                            folderpath = os.path.join(bfolderpath, item["name"])
                            listfolders(item["id"], folderpath)
                        else:
                            if not os.path.isdir(folder_name):
                                os.mkdir(folder_name)
                            bfolderpath = os.path.join(os.getcwd(), folder_name)

                            filepath = os.path.join(bfolderpath, item["name"])
                            downloadfiles(item["id"], filepath)
                            print(item["name"])
            break


# Search id of specific folder name under a parent folder id
def get_gdrive_id(folder_ids, folder_names):
    for folder_id in folder_ids:
        for folder_name in folder_names:
            print(folder_name)
            page_token = None
            while True:
                response = (
                    service.files()
                    .list(
                        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'and name = '{folder_name}'",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                for file in response.get("files", []):
                    print("Found file: %s (%s)\n" % (file.get("name"), file.get("id")))
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    downloadfolders([file.get("id")])
                    break


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--id",
        type=str,
        nargs="+",
        help="Specific files or folders ID you would like to download (Must have).",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        nargs="*",
        help="Specific folder names you would like to download (Optional).",
    )
    opt = parser.parse_args()
    return opt


def main(opt):
    if opt.name:
        get_gdrive_id(opt.id, opt.name)
    elif opt.id:
        downloadfolders(opt.id)
    else:
        print("Alert: Folder or Files ID to download must be provided.")


if __name__ == "__main__":
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    opt = parse_opt()
    main(opt)
