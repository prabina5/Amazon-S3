# For single file upload to S3
def post(self):
        if "user_file" not in request.files:
            return "No user_file key in request.files"
        file = request.files["user_file"]
        if file.filename == "":
            return "Please select a file"
        if file:
            mime_type, encoding = mimetypes.guess_type(file.filename)
            extension = mimetypes.guess_extension(mime_type)
            file.filename = "Sat" + extension
            file.filename = secure_filename(file.filename)
            #
            # temp_filename = f"{uuid.uuid4()}"
            output = upload_file_to_s3(file, S3_BUCKET)
            print(output)
            data = {"url": S3_LOCATION + file.filename}
            return ("get_file_uploaded", "file-uploaded-successfully", data)
        else:
            return " Not uploaded"


def upload_file_to_s3(file, bucket_name):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type  # Set appropriate content type.
            },
        )
    except Exception as e:
        return ("get_file_upload", str(e)), 400
        
    # for multiple file uploads in S#
    
    def post(self):
        if "user_file" not in request.files:
            return "No user_file key in request.files"
        files = request.files.getlist("user_file")
        data = []
        for file in files:
            file.filename = secure_filename(file.filename)
            output = upload_file_to_s3(file, S3_BUCKET)
            print(output)
            data.append(S3_LOCATION + file.filename)
        return ("get_file_uploaded", "file-uploaded-successfully", data)

    
