import boto3
from boto3.s3.transfer import S3Transfer
from botocore.exceptions import ClientError

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

import uuid

import os
import sys

from werkzeug.wrappers import Response

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    folder_path = 'folder'
    bucket_name = 'bucket'

    if request.method == 'POST':

        if not request.files.get('image_data', None):
            msg = 'the request contains no file'
            return render_template('exception.html', text=msg)

    file = request.files['image_data']
    folder_path = request.form.get('folderpath')
    bucket_name = request.form.get('bucketname')
    path = os.path.abspath(os.path.join(os.getcwd(), os.pardir, '/', secure_filename(file.filename)))
    filename, file_extension = os.path.splitext(path)
    filename_uuid = file.filename
    path_uuid = os.path.abspath(os.path.join(os.getcwd(), os.pardir, '', filename_uuid))
    file.save(path_uuid)

    # print("filename", type(file.filename))
    # print("filename1", type(secure_filename(file.filename)))
    # print("folderpath", folder_path)
    # print("bucket_name", bucket_name)

    client = boto3.client('s3', aws_access_key_id='~~~~~~', aws_secret_access_key='~~~~~~~~~~~')
    transfer = S3Transfer(client)
    # print('path_uuid', path_uuid)
    # print("imagename", secure_filename(file.filename))
    # print('filename', folder_path + "/" + secure_filename(file.filename))

    transfer.upload_file(path_uuid, bucket_name, folder_path + "/" + secure_filename(file.filename))
    response = client.put_object_acl(ACL='public_read', Bucket = bucket_name, Key = "%s/%s" % (folder_path, secure_filename(file.filename)))

    return 'sucess'

@app.route('/')
def index():
    """START PAGE."""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8001, debug = True)
