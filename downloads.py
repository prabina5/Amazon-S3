# for Multiple And Single Downloads
def get(self):
        bucket_name = S3_BUCKET
        directory = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"], "images")
        os.chdir(directory)
        os.mkdir("downloads")
        data = ["beauty.jpg"]
        try:
            for o in data:
                # check if file exists
                if s3.head_object(Bucket=bucket_name, Key=o) is None:
                    return ("get_file_download", "file-not-found"), 400
                else:
                    # download file
                    s3.download_file(bucket_name, o, directory + "/" + o)
                    # do not zip file
                    with zipfile.ZipFile(directory + "/" + o + ".zip", "w") as zip:
                        zip.write(directory + "/" + o)
                    # delete file
                    os.remove(directory + "/" + o)
                    # return file
                    return send_file(
                        directory + "/" + o + ".zip",
                        mimetype="document/zip",
                        attachment_filename=o + ".zip",
                    )
except Exception as e:
            return ("something wrong happened", str(e)), 400

