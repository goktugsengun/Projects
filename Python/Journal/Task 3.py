from __future__ import print_function

import PIL.Image
import httplib2
import os, io, pathlib

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaIoBaseDownload
from PIL import Image
from datetime import datetime


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'DAVPJournal'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def listfiles():
    """Shows basic usage of the Google Drive API.
    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)

    results = drive_service.files().list(
        pageSize=30, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

listfiles()


def get_download_link(file_id):
    """Gets download link of chosen file. Requires file ID."""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)

# Update Sharing Setting
    request_body = {
        'role': 'reader',
        'type': 'anyone'
        }
    response_permission = drive_service.permissions().create(
        fileId=file_id,
        body=request_body
    ).execute()

    print(response_permission)


# Print Sharing URL
    response_share_link = drive_service.files().get(
        fileId=file_id,
        fields='webViewLink'
    ).execute()

    print(response_share_link)

# Remove Sharing Permission
    drive_service.permissions().delete(
        fileId=file_id,
        permissionId='anyoneWithLink'
    ).execute()

get_download_link('1PSjgE8qqRgBRE9BLGYLA1suyFuml03Vt')


def download_file(file_id, filepath):
    """Download the selected file from the Drive API. Needs file ID."""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())

download_file ('1PSjgE8qqRgBRE9BLGYLA1suyFuml03Vt', 'photo 1.jpg')
download_file ('1XotcBG8Wi1KKu2DuDlFQBIxNATahHimH', 'photo 2.jpg')
download_file ('1FsMM-TPUpryoaLkrPU9ZzLkxYdqnil76', 'photo 3.jpg')


def resize_img(file_name):
    """Resize the chosen image's longest side to 1000 pxls while maintaining the aspect ratio. Need to specify the file name and its extension"""
    image = Image.open(file_name)
    if image.size[0] >= image.size[1]:
        basewidth = 1000
        widthpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1] * float(widthpercent))))
        image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        image.save(file_name)
    else:
        baseheight = 1000
        heightpercent = (baseheight / float(image.size[1]))
        wsize = int((float(image.size[0] * float(heightpercent))))
        image = image.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
        image.save(file_name)

resize_img('photo 1.jpg')
resize_img('photo 2.jpg')
resize_img('photo 3.jpg')


def unix2datetime(unix):
    """Turning the time data of an image to a readable one."""
    return datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d')


def rename_img():
    """Renaming the images in current directory to the defined format of [date taken]_[count]."""
    root_dir = '.'
    counter = 0
    for file in pathlib.Path(root_dir).iterdir():
        info = file.stat()
        ctime = info.st_ctime
        mtime = info.st_mtime
        if mtime <= ctime:
            date_created = unix2datetime(mtime)
        else:
            date_created = unix2datetime(ctime)
        file_name, file_extension = os.path.splitext(file)
        if file_extension != '.jpg':
            continue
        counter = counter + 1
        new_filename = date_created + '_' + str(counter) + file_extension
        os.rename(file, new_filename)
        print(file_name, '->', new_filename)
rename_img()