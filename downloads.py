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
        
        
 def get(self):
        bucket_name = S3_BUCKET
        timestr = time.strftime("%Y%m%d-%H%M%S")
        fileName = "my_datadump{}.zip".format(timestr)
        memory_file = io.BytesIO()
        temp_folder = f"{uuid.uuid4().hex}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], "images", temp_folder)
        os.mkdir(file_path)
        data = ["icecream1.jpg", "double.jpg"]
        try:
            for o in data:
                # memory_file = io.BytesIO()
                with open(os.path.join(file_path, o), "wb") as f:
                    s3.download_fileobj(bucket_name, o, f)
            with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zipf:
                files = Path(file_path).glob("*")
                for file in files:
                    zipf.write(file)
            memory_file.seek(0)
            for op in data:
                os.remove(os.path.join(file_path, op))
            os.rmdir(file_path)
            return send_file(
                memory_file, attachment_filename=fileName, as_attachment=True
            )
        except Exception as e:
            return ("something wrong happened", str(e)), 400


